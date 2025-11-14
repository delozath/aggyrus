from typing import override, Literal, Any

from dataclasses import dataclass, field

from aggyrus.core.validations.signature import save_init_kwargs
from aggyrus.spi.filters import BaseDigitalFilter
from aggyrus.spi.errors import FilterInitializerError, FilterDesignError

from scipy.signal import butter, filtfilt
import numpy as np

@dataclass(kw_only=True)
class ButterworthFilterContainer:
    order: int = 4
    cutoff: float | np.ndarray = field(default_factory = lambda: np.array([0.1, 20]))
    btype: Literal['lowpass' 'highpass', 'bandpass', 'bandstop'] = 'bandpass'
    fs: float = 100.0
    output: Literal['ba', 'zpk', 'sos'] = 'sos'
    analog: bool = False
    design: Any | None = None

    def __post_init__(self):
        if not isinstance(self.order, int) or self.order < 1:
            raise FilterInitializerError("Order must be a positive integer.")
        if not isinstance(self.cutoff, (float, np.ndarray)):
            raise FilterInitializerError("Cutoff frequency must be a float or a numpy array.")
        if self.btype not in ['lowpass', 'highpass', 'bandpass', 'bandstop']:
            raise FilterInitializerError("Invalid filter type specified.")
        if not isinstance(self.fs, (float, int)) or self.fs <= 0:
            raise FilterInitializerError("Sampling frequency must be a positive number.")
        if not isinstance(self.analog, bool):
            raise FilterInitializerError("Analog flag must be a boolean value.")



class ButterworthFilter(BaseDigitalFilter):
    def __init__(self):
        self.name = "butterworth"

    @override
    def design(self, /, **kwargs) -> None:
        self._container = save_init_kwargs(ButterworthFilterContainer, **kwargs)
        design_ = butter(
                N=self._container.order,
                Wn=self._container.cutoff,
                btype=self._container.btype,
                analog=self._container.analog,
                output=self._container.output,
                fs=self._container.fs
         )
        self._container.design = design_
        breakpoint()



    @override
    def apply(self, signal: np.ndarray) -> np.ndarray:
        filtered_signal = filtfilt(self.b, self.a, signal)
        return filtered_signal