"""
_summary_
"""
import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from threading import Thread

from pymitter import EventEmitter
from statemachine import State, StateMachine

from ..appconfig import AppConfig
from ..utils.exceptions import ProcessMachineOccupiedError
from .aquisitionservice import AquisitionService
from .mediacollection.mediaitem import MediaItem, MediaItemTypes, get_new_filename
from .mediacollectionservice import (
    MediacollectionService,
)
from .mediaprocessingservice import MediaprocessingService

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3


class ProcessingService(StateMachine):
    """
    use it:
        machine.thrill()
        machine.shoot()
    """

    @dataclass
    class Stateinfo:
        """_summary_"""

        state: str
        countdown: float = 0

    ## STATES

    idle = State(initial=True)
    thrilled = State()
    counting = State()
    capture_still = State()
    postprocess_still = State()

    ## TRANSITIONS

    thrill = idle.to(thrilled)
    countdown = thrilled.to(counting)
    shoot = idle.to(capture_still) | thrilled.to(capture_still) | counting.to(capture_still)
    postprocess = capture_still.to(postprocess_still)
    finalize = postprocess_still.to(idle)

    _reset = idle.to(idle) | thrilled.to(idle) | counting.to(idle) | capture_still.to(idle) | postprocess_still.to(idle)

    def __init__(
        self,
        evtbus: EventEmitter,
        config: AppConfig,
        aquisition_service: AquisitionService,
        mediacollection_service: MediacollectionService,
        mediaprocessing_service: MediaprocessingService,
    ):
        self._evtbus: EventEmitter = evtbus
        self._config: AppConfig = config
        self._aquisition_service: AquisitionService = aquisition_service
        self._mediacollection_service: MediacollectionService = mediacollection_service
        self._mediaprocessing_service: MediaprocessingService = mediaprocessing_service

        self.timer: Thread = None
        self.timer_countdown = 0
        # filepath of the captured image that is processed in this run:
        self._filepath_originalimage_processing: str = None

        super().__init__()

        # register to send initial data SSE
        self._evtbus.on("publishSSE/initial", self._sse_initial_processinfo)

    # general on_ events
    def before_transition(self, event, state):
        """_summary_"""
        pass
        # logger.info(f"Before '{event}', on the '{state.id}' state.")

    def on_transition(self, event, state):
        """_summary_"""
        pass
        # logger.info(f"On '{event}', on the '{state.id}' state.")

    def on_exit_state(self, event, state):
        """_summary_"""
        pass
        # logger.info(f"Exiting '{state.id}' state from '{event}' event.")

    def on_enter_state(self, event, state):
        """_summary_"""
        # logger.info(f"Entering '{state.id}' state from '{event}' event.")
        logger.info(f"on_enter_state '{self.current_state.id=}' ")

        # always send current state on enter so UI can react (display texts, wait message on postproc, ...)
        self._sse_processinfo(
            __class__.Stateinfo(
                state=self.current_state.id,
                countdown=self.timer_countdown,
            )
        )

    def after_transition(self, event, state):
        """_summary_"""
        pass
        # logger.info(f"After '{event}', on the '{state.id}' state.")

    ## specific on_ transition actions:

    def on_thrill(self):
        """_summary_"""
        logger.info("on_thrill")
        self._evtbus.emit("statemachine/on_thrill")

    def on_shoot(self):
        """_summary_"""

    def on_enter_postprocess_still(self):
        # create JPGs and add to db
        logger.info("on_enter_postprocess_still")

        # TODO: collage: separate postprocessing step 2 mount collage and create a new original.

        # create mediaitem for further processing
        mediaitem = MediaItem(os.path.basename(self._filepath_originalimage_processing))

        # always create unprocessed versions for later usage
        tms = time.time()
        self._mediaprocessing_service.create_scaled_unprocessed_repr(mediaitem)
        logger.info(f"-- process time: {round((time.time() - tms), 2)}s to create scaled images")

        # apply 1pic pipeline:
        tms = time.time()
        self._mediaprocessing_service.apply_pipeline_1pic(mediaitem)
        logger.info(f"-- process time: {round((time.time() - tms), 2)}s to apply pipeline")

        # add result to db
        _ = self._mediacollection_service.db_add_item(mediaitem)

        logger.info(f"capture {mediaitem=} successful")

        # to inform frontend about new image to display
        self._evtbus.emit(
            "publishSSE",
            sse_event="imagedb/newarrival",
            sse_data=json.dumps(mediaitem.asdict()),
        )

    ## specific on_state actions:

    def on_enter_idle(self):
        """_summary_"""
        logger.info("on_enter_idle")
        # always remove old reference
        self._filepath_originalimage_processing = None

    def on_enter_counting(self):
        """_summary_"""
        logger.info("on_enter_counting")
        self.timer_countdown = (
            self._config.common.PROCESS_COUNTDOWN_TIMER + self._config.common.PROCESS_COUNTDOWN_OFFSET
        )
        logger.info(f"loaded timer_countdown='{self.timer_countdown}'")
        logger.info("starting timer")

        while self.timer_countdown > 0:
            self._sse_processinfo(
                __class__.Stateinfo(
                    state=self.current_state.id,
                    countdown=round(self.timer_countdown, 1),
                )
            )
            time.sleep(0.1)
            self.timer_countdown -= 0.1

            if self.timer_countdown <= self._config.common.PROCESS_COUNTDOWN_OFFSET and self.counting.is_active:
                return

    def on_exit_counting(self):
        logger.info("on_exit_counting")
        self.timer_countdown = 0

    def on_enter_capture_still(self):
        """_summary_"""
        logger.info("on_enter_capture_still")
        self._evtbus.emit("statemachine/on_enter_capture_still")

        filepath_neworiginalfile = get_new_filename(type=MediaItemTypes.IMAGE)
        logger.debug(f"capture to {filepath_neworiginalfile=}")

        start_time_capture = time.time()

        # at this point it's assumed, a HQ image was requested by statemachine.
        # seems to not make sense now, maybe revert hat...
        # waitforpic and store to disk
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                image_bytes = self._aquisition_service.wait_for_hq_image()

                # send 0 countdown to UI
                self._sse_processinfo(
                    __class__.Stateinfo(
                        state=self.current_state.id,
                        countdown=0,
                    )
                )

                with open(filepath_neworiginalfile, "wb") as file:
                    file.write(image_bytes)

                # populate image item for further processing:
                self._filepath_originalimage_processing = filepath_neworiginalfile
            except TimeoutError:
                logger.error(f"error capture image. timeout expired {attempt=}/{MAX_ATTEMPTS}, retrying")
                # can we do additional error handling here?
            else:
                break
        else:
            # we failed finally all the attempts - deal with the consequences.
            logger.critical(f"finally failed after {MAX_ATTEMPTS} attempts to capture image!")
            raise RuntimeError(f"finally failed after {MAX_ATTEMPTS} attempts to capture image!")

        logger.info(f"-- process time: {round((time.time() - start_time_capture), 2)}s to capture still")

    def on_exit_capture_still(self):
        """_summary_"""
        logger.info("on_exit_capture_still")
        self._evtbus.emit("statemachine/on_exit_capture_still")

    ### some external functions

    def evt_chose_1pic_get(self):
        logger.info("evt_chose_1pic_get called to take picture")
        if not self.idle.is_active:
            raise ProcessMachineOccupiedError("bad request, only one request at a time!")

        try:
            self.thrill()
            self.countdown()
            self.shoot()
            self.postprocess()
            self.finalize()
        except Exception as exc:
            logger.exception(exc)
            logger.critical(f"something went wrong :( {exc}")
            self._reset()
            raise RuntimeError(f"something went wrong :( {exc}") from exc

    ### some custom helper

    def _sse_initial_processinfo(self):
        """_summary_"""
        self._sse_processinfo(__class__.Stateinfo(state=self.current_state.id))

    def _sse_processinfo(self, sse_data: Stateinfo):
        """_summary_"""
        self._evtbus.emit(
            "publishSSE",
            sse_event="statemachine/processinfo",
            sse_data=json.dumps(asdict(sse_data)),
        )
