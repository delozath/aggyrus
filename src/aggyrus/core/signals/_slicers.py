from abc import ABC, abstractmethod
from typing import Iterator


import numpy as np
from numpy.typing import NDArray


from aggyrus.core.signals._time_serie_types import SegmentedTimeSeries


class BaseSlicer(ABC):
    @abstractmethod
    def perform(
        self,
        record: SegmentedTimeSeries | NDArray[np.number],
        segments: NDArray[np.number]
     ) -> Iterator[NDArray[np.number]] | NDArray[np.number]:
        """
        Abstract method to perform slicing operation on a time series record or ndarray.

        Parameters
        ----------
        record : SegmentedTimeSeries | NDArray[np.number]
            The time series record or ndarray to be sliced.
        segments : NDArray[np.number]
            The segments defining the slices. If record is SegmentedTimeSeries segments should be ignored because segments are already defined in record.segments attribute.

        Returns
        -------
        Iterator[NDArray[np.number]] | NDArray[np.number]
            An iterator over the sliced segments as ndarrays, or a single ndarray if record is an ndarray.

        Yields
        ------
        NDArray[np.number]
            The sliced segment as an ndarray.
            
        Raises
        ------
        ValueError
            If no segments are defined in the time series record. | If segments are invalid.        
        """
        ...