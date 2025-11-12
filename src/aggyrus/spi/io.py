from abc import ABC, abstractmethod
from typing import Iterable

from pathlib import Path


from aggyrus.core.signals._time_serie_types import BaseTimeSeries


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