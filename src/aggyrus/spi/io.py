from abc import ABC, abstractmethod
from typing import Iterable, Sequence, Tuple, List

from pathlib import Path


import numpy as np
from numpy.typing import NDArray


from aggyrus.core._time_serie_types import BaseTimeSeries


class IOProviderError(Exception):
    """
    Exception raised for errors in the IO provider from external libraries.
    """
    def __init__(self, message: str):
        print("IOProverderError raised")
        super().__init__(message)


class IOWindowrError(Exception):
    """
    Exception raised when the segments attempted to fetch are outside the signal duration.
    """
    def __init__(self, message: str):
        print("The segments attempted to fetch is outside signal duration")
        super().__init__(message)


class BaseSignalLoader(ABC):
    #def decode(self, source: str | Path, options: None = None) -> BaseTimeSeries:
    @abstractmethod
    def decode(self, source: str | Path, /, *args, **kwargs) -> BaseTimeSeries: 
        """
        Abstract Protocol method to read a signal from a given source.

        Parameters
        ----------
        source : str | Path
            The path or identifier of the signal source.
        kwargs : dict, optional
            Additional options for reading the signal.
        
        Raises
        ------
        IOProviderError
            If there is an error reading the signal from external library provider.
        """

        ...

    @abstractmethod
    def batch(self, sources: Iterable[str | Path], options: None = None) -> Iterable[BaseTimeSeries]:
        """
        Abstract Protocol method to read multiple signals from given sources.

        Parameters
        ----------
        sources : Iterable[str | Path]
            An iterable of paths or identifiers of the signal sources.
        options : None, optional
            Additional options for reading the signals, by default None.
        
        Raises
        ------
        IOProviderError
            If there is an error reading any of the signals from external library provider.

        Yields
        ------
        BaseTimeSeries
            The read signal as a BaseTimeSeries object.    
        """
        ...

    @abstractmethod
    def windowed(
        self,
        source: str | Path,
        windows: Sequence[Tuple[float | int, float | int]] | NDArray[np.float64 | np.float32 | np.int64] | None = None,
    ) -> Iterable[BaseTimeSeries] | NDArray[np.float64 | np.float32] | List[NDArray]:
        """
        Abstract Protocol method to read specific windows of a signal from a given source.
        
        Parameters
        ----------
        source : str | Path
            The path or identifier of the signal source.
        windows : Sequence[Tuple[float, float]] | NDArray[np.float64 | np.float32] | None, optional
            The windows to read from the signal, by default None. It represents all pairs of (start, end) in seconds (floats) or samples (ints). Note means the entire signal.
        
        Yields
        ------
        BaseTimeSeries
            The windowed signal as a BaseTimeSeries object.
        
        
        Returns
        -------
            NumPy arrays or list of NumPy arrays containing the windowed signal data.
        
        Raises
        ------
        IOWindowrError
            If the segments attempted to fetch are outside the signal duration.
        """
        ...


__all__ = [
    "BaseSignalLoader",
    "IOProviderError",
    "IOWindowrError",
]
