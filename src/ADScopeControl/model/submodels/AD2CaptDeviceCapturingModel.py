import pandas as pd
from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig
from ADScopeControl.model.AD2Constants import AD2Constants


class AD2CaptDeviceCapturingSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)


    # Acquisition Settings
    sample_rate_changed = Signal(int)
    streaming_rate_changed = Signal(int)
    selected_ain_channel_changed = Signal(int)
    streaming_history_changed = Signal(int)
    # Acquired Signal Information
    recorded_samples_changed = Signal(list)
    recording_time_changed = Signal(float)
    samples_captured_changed = Signal(int)
    samples_lost_changed = Signal(int)
    samples_corrupted_changed = Signal(int)
    # Actually for the worker, these are the samples that have not been consumed yet by the UI thread.
    unconsumed_stream_samples_changed = Signal(int)
    unconsumed_capture_samples_changed = Signal(int)

    # Recording Flags (starting, stopping and pausing)
    device_capturing_state_changed = Signal(AD2Constants.CapturingState)
    ready_for_recording_changed = Signal(bool)
    start_recording_changed = Signal(bool)
    stop_recording_changed = Signal(bool)
    reset_recording_changed = Signal(bool)
    capturing_finished_changed = Signal(bool)

class AD2CaptDeviceCapturingModel:
    def __init__(self, config: CaptDeviceConfig):
        self.signals = AD2CaptDeviceCapturingSignals()
        self.config = config

        # Acquired Signal Information
        # The number of recorded samples
        self._recorded_samples: list = []
        self.recorded_samples_preview: list = []
        self._recorded_samples_df: pd.DataFrame = None
        # The length of the recording
        self._recording_time: float = 0

        # Number of the captured, lost and corrupted samples
        self._number_samples_captured: int = 0
        self._number_samples_lost: int = 0
        self._number_samples_corrupted: int = 0

        # Flag if the capturing is finished
        self._capturing_finished: bool = False

        # Actually for the worker, these are the samples that have not been consumed yet by the UI thread.
        self._unconsumed_stream_samples: int = 0
        self._unconsumed_capture_samples: int = 0

        # Recording Flags (starting, stopping and pausing)
        self._device_capturing_state: AD2Constants.CapturingState = AD2Constants.CapturingState.STOPPED()
        self._ready_for_recording: bool = False
        self._start_recording = False
        self._stop_recording = True
        self._reset_recording = True

# ==================================================================================================================
    # Acquired Signal Information
    # ==================================================================================================================
    @property
    def recorded_samples(self) -> list:
        return self._recorded_samples

    @recorded_samples.setter
    def recorded_samples(self, value: list):
        self._recorded_samples = value
        self.samples_captured = len(self._recorded_samples)
        # self.signals.num_of_current_recorded_samples_changed.emit(self.num_of_current_recorded_samples)
        self.signals.recorded_samples_changed.emit(self.recorded_samples)

    @property
    def recorded_samples_df(self) -> list:
        return self._recorded_samples_df

    @recorded_samples_df.setter
    def recorded_samples_df(self, value: pd.DataFrame):
        self._recorded_samples_df = value


    @property
    def recording_time(self) -> float:
        return self._recording_time

    @recording_time.setter
    def recording_time(self, value: float):
        self._recording_time = value
        self.signals.recording_time_changed.emit(self.recording_time)

    @property
    def samples_captured(self) -> int:
        return self._samples_captured

    @samples_captured.setter
    def samples_captured(self, value: int):
        self._samples_captured = value
        self.signals.samples_captured_changed.emit(self.samples_captured)

    @property
    def samples_lost(self) -> int:
        return self._samples_lost

    @samples_lost.setter
    def samples_lost(self, value: int):
        self._samples_lost = value
        self.signals.samples_lost_changed.emit(self.samples_lost)

    @property
    def samples_corrupted(self) -> int:
        return self._samples_corrupted

    @samples_corrupted.setter
    def samples_corrupted(self, value: int):
        self._samples_corrupted = value
        self.signals.samples_corrupted_changed.emit(self.samples_corrupted)

    @property
    def capturing_finished(self) -> bool:
        return self._capturing_finished

    @capturing_finished.setter
    def capturing_finished(self, value: bool):
        self._capturing_finished = value
        #print(f"Set _capturing_finished to {self._capturing_finished}")
        self.signals.capturing_finished_changed.emit(self._capturing_finished)

    # ==================================================================================================================
    # Recording Flags (starting, stopping and pausing)
    # ==================================================================================================================
    @property
    def device_capturing_state(self) -> AD2Constants.CapturingState:
        return self._device_capturing_state

    @device_capturing_state.setter
    def device_capturing_state(self, value: int):
        #print(f"Set device_capturing_state to {value}")
        self._device_capturing_state = value
        self.signals.device_capturing_state_changed.emit(self.device_capturing_state)

    @property
    def ready_for_recording(self) -> bool:
        return self._ready_for_recording

    @ready_for_recording.setter
    def ready_for_recording(self, value: bool):
        self._ready_for_recording = value
        self.signals.ready_for_recording_changed.emit(self.ready_for_recording)
    @property
    def start_recording(self) -> bool:
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {self._start_recording}")
        return self._start_recording

    @start_recording.setter
    def start_recording(self, value: bool):
        self._start_recording = value
        self.signals.start_recording_changed.emit(self._start_recording)

    @property
    def stop_recording(self) -> bool:
        return self._stop_recording

    @stop_recording.setter
    def stop_recording(self, value: bool):
        self._stop_recording = value
        self.signals.stop_recording_changed.emit(self.stop_recording)

    @property
    def reset_recording(self):
        return self._reset_recording

    @reset_recording.setter
    def reset_recording(self, value):
        self._reset_recording = value
        self.signals.reset_recording_changed.emit(self._reset_recording)

    @property
    def unconsumed_stream_samples(self) -> int:
        return self._unconsumed_stream_samples

    @unconsumed_stream_samples.setter
    def unconsumed_stream_samples(self, value: int):
        self._unconsumed_stream_samples = value
        self.signals.unconsumed_stream_samples_changed.emit(self.unconsumed_stream_samples)

    @property
    def unconsumed_capture_samples(self) -> int:
        return self._unconsumed_capture_samples

    @unconsumed_capture_samples.setter
    def unconsumed_capture_samples(self, value: int):
        self._unconsumed_capture_samples = value
        self.signals.unconsumed_capture_samples_changed.emit(self.unconsumed_capture_samples)


    @property
    def streaming_history(self) -> float:
        return self.config.streaming_history.get()

    @streaming_history.setter
    def streaming_history(self, value: float):
        self.config.streaming_history.set(value)
        self.signals.streaming_history_changed.emit(self.streaming_history)

    @property
    def streaming_rate(self):
        return self.config.streaming_rate.get()

    @streaming_rate.setter
    def streaming_rate(self, value):
        self.config.streaming_rate.set(value)
        self.signals.streaming_rate_changed.emit(self.streaming_rate)

    @property
    def streaming_deque_length(self):
        return int((self.streaming_history / 1000) * self.sample_rate)

   # ==================================================================================================================
    # Acquisition Settings
    # ==================================================================================================================
    @property
    def sample_rate(self):
        return self.config.sample_rate.get()

    @sample_rate.setter
    def sample_rate(self, value):
        self.config.sample_rate.set(value)
        self.signals.sample_rate_changed.emit(self.sample_rate)

