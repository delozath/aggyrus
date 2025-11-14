import numpy as np
from scipy import signal as sg
from typing import Any, Callable, Dict, Tuple, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields

from aggyrus.core.validations.descriptors import TypedMutableDescr, TypedNonMutableDescr
from aggyrus.spi.plots import BaseContainerPlot


@dataclass(kw_only=True)
class SpectrumAnalyzerParams:
    sr: float = 100.0
    mag_mode: Literal['power', 'dB'] = 'power'

    def __post_init__(self):
        if not isinstance(self.sr, (float, int)) or self.sr <= 0:
            raise ValueError("Sampling rate must be a positive number.")
        if self.mag_mode not in ['power', 'dB']:
            raise ValueError("Magnitude type must be 'power' or 'dB'.")

    def __str__(self) -> str:
        field_list = ', '.join([f.name for f in fields(self)])
        return f"<{type(self).__name__}: fields>: {field_list}"


@dataclass
class SpectrumContainer(SpectrumAnalyzerParams):
    freq: np.ndarray = field(default_factory=lambda: np.array([]))
    magnitude: np.ndarray = field(default_factory=lambda: np.array([]))
    phase: np.ndarray | None = field(default=None)


class SpectrumAnalyzer(BaseContainerPlot[SpectrumContainer]):
    name = TypedNonMutableDescr(str)
    params = TypedMutableDescr(SpectrumAnalyzerParams)

    @abstractmethod
    def perform(self, /, **kwargs) -> None: ...
    
    @abstractmethod
    def compute(self, signal: np.ndarray, /, **kwargs) -> SpectrumContainer: ...

    def _magnitude_factory(self, mode: Literal['power', 'dB'], x: np.ndarray) -> np.ndarray:
        if mode == 'power':
            magnitude = np.abs(x)**2
        else:
            magnitude = 20 * np.log10(np.abs(x))
        return magnitude



