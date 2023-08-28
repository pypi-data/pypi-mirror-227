import logging
from pathlib import Path

import cv2
import numpy as np
import pilgram2
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pydantic_extra_types.color import Color

from ...appconfig import TextStageConfig
from ...utils.exceptions import PipelineError

logger = logging.getLogger(__name__)
DATA_USER_PATH = "./data/user/"


def pilgram_stage(image: Image, filter: str) -> Image:
    """ """
    logger.info(f"pilgram filter stage {filter} to apply")
    try:
        algofun = getattr(pilgram2, filter)
    except Exception as exc:
        raise PipelineError(f"pilgram filter {filter} does not exist") from exc
    else:
        # apply filter
        filtered_image: Image = algofun(image.copy())

        if image.mode in ("RGBA", "P"):
            logger.debug("need to convert to rgba and readd transparency mask to filtered image")
            # get alpha from original image
            _, _, _, a = image.split()
            # get rgb from filtered image
            r, g, b = filtered_image.split()
            # and merge both
            filtered_transparent_image = Image.merge(image.mode, (r, g, b, a))

            return filtered_transparent_image

        return filtered_image


def text_stage(image: Image, textstageconfig: list[TextStageConfig]) -> Image:
    """ """
    logger.info("text stage to apply")

    for textconfig in textstageconfig:
        logger.debug(f"apply text: {textconfig=}")

        # check font is avail, otherwise send pipelineerror - so we can recover and continue
        # default font Roboto comes with app, fallback to that one if avail
        font_user_path = Path(DATA_USER_PATH, textconfig.font)
        font_assets_path = (
            Path(__file__)
            .parent.resolve()
            .joinpath(
                Path(
                    "assets",
                    "fonts",
                    textconfig.font,
                )
            )
        )
        font_path = font_user_path if font_user_path.is_file() else font_assets_path

        if not font_path.is_file():
            raise PipelineError(f"font {str(font_user_path)} not found!")

        img_font = ImageFont.truetype(
            font=str(font_path),
            size=textconfig.font_size,
        )

        img_draw = ImageDraw.Draw(image)
        img_draw.text(
            (textconfig.pos_x, textconfig.pos_y),
            textconfig.text,
            fill=textconfig.color.as_rgb_tuple(),
            font=img_font,
        )

    return image


def beauty_stage(image: Image) -> Image:
    """ """
    raise PipelineError("beauty_stage not implemented yet")


def frame_stage(image: Image) -> Image:
    """ """
    raise PipelineError("beauty_stage not implemented yet")


def rembg_stage(image: Image) -> Image:
    """ """
    raise PipelineError("rembg_stage not implemented yet")  # https://github.com/danielgatis/rembg


def removechromakey_stage(pil_image: Image, keycolor: int, tolerance: int) -> Image:
    """_summary_

    References:
        choose hsv parameters: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
        https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
        https://stackoverflow.com/questions/48109650/how-to-detect-two-different-colors-using-cv2-inrange-in-python-opencv
        https://www.geeksforgeeks.org/opencv-invert-mask/
        https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
        https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html

    Args:
        pil_image (Image): _description_

    Returns:
        Image: _description_
    """

    logger.info("removechromakey_stage to apply")

    # constants derived from parameters
    dilate_pixel = 4
    blur_pixel = 2
    keycolor_range_min_hsv = ((keycolor) / 2 - tolerance, 50, 50)
    keycolor_range_max_hsv = ((keycolor) / 2 + tolerance, 255, 255)

    def convert_from_cv2_to_image(img: np.ndarray) -> Image:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))

    def convert_from_image_to_cv2(img: Image) -> np.ndarray:
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    frame = convert_from_image_to_cv2(pil_image)
    ## convert to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask of green
    mask = cv2.inRange(hsv, np.array(keycolor_range_min_hsv), np.array(keycolor_range_max_hsv))
    # remove noise/false positives within people area
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((dilate_pixel, dilate_pixel), np.uint8))
    # dilate mask a bit to remove bit more when blurred
    mask = cv2.dilate(mask, np.ones((dilate_pixel, dilate_pixel), np.uint8), iterations=1)

    # Inverting the mask
    mask_inverted = cv2.bitwise_not(mask)

    # enhance edges by blur# blur threshold image
    blur = cv2.GaussianBlur(mask_inverted, (0, 0), sigmaX=blur_pixel, sigmaY=blur_pixel, borderType=cv2.BORDER_DEFAULT)

    # actually remove the background (so if transparency is ignored later in processing,
    # the removed parts are black instead just return)
    result = cv2.bitwise_and(frame, frame, mask=blur)
    # create result with transparent channel
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = blur  # add mask to image as alpha channel

    return convert_from_cv2_to_image(result)


def image_fill_background_stage(image: Image, color: Color) -> Image:
    """ """

    logger.info("image_fill_background_stage to apply")

    background_img = Image.new(mode=image.mode, size=image.size, color=color.as_rgb_tuple())
    background_img.paste(image, mask=image)

    return background_img


def image_img_background_stage(image: Image, background_file: Path) -> Image:
    """ """
    logger.info("image_img_background_stage to apply")

    if image.mode not in ("RGBA", "P"):
        logger.warning("no transparency in image, background stage makes no sense to apply!")
        return image

    # check image is avail, otherwise send pipelineerror - so we can recover and continue
    # default font Roboto comes with app, fallback to that one if avail
    background_img_user_path = Path(DATA_USER_PATH, background_file)
    background_img_assets_path = (
        Path(__file__)
        .parent.resolve()
        .joinpath(
            Path(
                "assets",
                "backgrounds",
                background_file,
            )
        )
    )
    background_img_path = background_img_user_path if background_img_user_path.is_file() else background_img_assets_path
    if not background_img_path.is_file():
        raise PipelineError(f"image {str(background_img_user_path)} not found!")

    background_img = Image.open(background_img_path)

    # fit background image to actual image size
    # this might crop the background but fills the image fully. automatic centered.
    background_img_adjusted = ImageOps.fit(background_img, image.size)

    # paste the actual image to the background
    background_img_adjusted.paste(image, mask=image)

    return background_img_adjusted
