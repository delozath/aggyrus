from typing import override, Literal, Callable, Dict, Tuple, Any
from dataclasses import dataclass, field


import numpy as np
import scipy.signal as sg


from aggyrus.core.validations.signature import save_init_kwargs
from aggyrus.core.validations.descriptors import TypedMutableDescr
from aggyrus.spi.filters import BaseDigitalFilter
from aggyrus.spi.errors import FilterInitializerError, FilterApplyModeError


@dataclass(kw_only=True)
class ScipyLinearFilterContainer:
    order: int = 4
    cutoff: float | np.ndarray = field(default_factory = lambda: np.array([0.1, 20]))
    btype: Literal['lowpass' 'highpass', 'bandpass', 'bandstop'] = 'bandpass'
    sr: float = 100.0
    output: Literal['ba', 'sos'] = 'sos'
    analog: bool = False

    def __post_init__(self):
        if not isinstance(self.order, int) or self.order < 1:
            raise FilterInitializerError("Order must be a positive integer.")
        if not isinstance(self.cutoff, (float, np.ndarray)):
            raise FilterInitializerError("Cutoff frequency must be a float or a numpy array.")
        if self.btype not in ['lowpass', 'highpass', 'bandpass', 'bandstop']:
            raise FilterInitializerError("Invalid filter type specified.")
        if not isinstance(self.sr, (float, int)) or self.sr <= 0:
            raise FilterInitializerError("Sampling frequency must be a positive number.")
        if not isinstance(self.analog, bool):
            raise FilterInitializerError("Analog flag must be a boolean value.")
        if self.output not in ['ba', 'sos']:
            raise FilterInitializerError("Output format must be 'ba', or 'sos'.")
        if self.sr <= 2 * np.max(self.cutoff):
            raise FilterInitializerError("Cutoff frequency exceeds Nyquist limit.")


@dataclass(kw_only=True)
class ScipyChebyshev1FilterContainer(ScipyLinearFilterContainer):
    ripple: float = 1.0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.ripple, (float, int)) or self.ripple <= 0:
            raise FilterInitializerError("Ripple must be a positive number.")


@dataclass(kw_only=True)
class ScipyFIRContainer(ScipyLinearFilterContainer):
    ripple: float = 1.0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.ripple, (float, int)) or self.ripple <= 0:
            raise FilterInitializerError("Ripple must be a positive number.")


numtaps, cutoff, width=None, window='hamming', pass_zero=True, scale=True, fs=None

class BaseScipyFilter:
    filter_ = TypedMutableDescr(ScipyLinearFilterContainer)
    model: Any

    def _apply_factory(self, mode) -> Tuple[Callable, Dict[str, np.ndarray]]:
        output = self._filter_.output
        if output == 'sos':
            func = sg.sosfiltfilt if mode == 'filtfilt' else sg.sosfilt
            params = {'sos': self.model}
        else:
            func = sg.filtfilt if mode == 'filtfilt' else sg.lfilter
            params = {'b': self.model[0], 'a': self.model[1]}

        return func, params


class ButterworthFilter(BaseDigitalFilter, BaseScipyFilter):
    def __init__(self):
        self.name = "butterworth"

    @override
    def design(self, /, **kwargs) -> None:
        self._filter_ = save_init_kwargs(ScipyLinearFilterContainer, **kwargs)
        self.model = sg.butter(
                N=self._filter_.order,
                Wn=self._filter_.cutoff,
                btype=self._filter_.btype,
                analog=self._filter_.analog,
                output=self._filter_.output,
                fs=self._filter_.sr
         )

    @override
    def apply(
        self,
        signal: np.ndarray,
        mode: Literal['filtfilt', 'filt']='filtfilt',
        **kwargs
     ) -> np.ndarray:
        if not hasattr(self, 'model'):
            raise FilterApplyModeError("Filter has not been designed yet. Call the `design` method first.")
        if mode not in ['filtfilt', 'filt']:
            raise FilterApplyModeError("Invalid mode specified. Use 'filtfilt' or 'filt'.")
        
        func, params = self._apply_factory(mode)
        params |= {'x': signal} | kwargs
        filt_signal = func(**params)

        return filt_signal


class Chebyshev1Filter(BaseDigitalFilter, BaseScipyFilter):
    def __init__(self):
        self.name = "chebyshev_type_1"

    @override
    def design(self, /, **kwargs) -> None:
        self._filter_ = save_init_kwargs(ScipyChebyshev1FilterContainer, **kwargs)
        self.model = sg.cheby1(
                N=self._filter_.order,
                rp=self._filter_.ripple,
                Wn=self._filter_.cutoff,
                btype=self._filter_.btype,
                analog=self._filter_.analog,
                output=self._filter_.output,
                fs=self._filter_.sr
         )

    @override
    def apply(
        self,
        signal: np.ndarray,
        mode: Literal['filtfilt', 'filt']='filtfilt',
        **kwargs
     ) -> np.ndarray:
        if not hasattr(self, 'model'):
            raise FilterApplyModeError("Filter has not been designed yet. Call the `design` method first.")
        if mode not in ['filtfilt', 'filt']:
            raise FilterApplyModeError("Invalid mode specified. Use 'filtfilt' or 'filt'.")
        
        func, params = self._apply_factory(mode)
        params |= {'x': signal} | kwargs
        filt_signal = func(**params)

        return filt_signal






firwin(