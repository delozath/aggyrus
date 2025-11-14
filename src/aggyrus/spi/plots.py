import numpy as np
from scipy import signal as sg
from typing import Any, Callable, Dict, Tuple, Literal, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class BasePlot(ABC):
    @abstractmethod
    def plot(self, *args, **kwargs) -> Any: ...

    @abstractmethod
    def show(self, *args, **kwargs) -> None: ...


class BaseContainerPlot[T](ABC):
    @abstractmethod
    def plot(self, x: T, /, **kwargs) -> Any: ...

    @abstractmethod
    def show(self, *args, **kwargs) -> None: ...


class BaseSignalPlot(ABC):
    @abstractmethod
    def plot(self, signal: np.ndarray, *args, **kwargs) -> Any: ...

    @abstractmethod
    def show(self, /, **kwargs) -> None: ...