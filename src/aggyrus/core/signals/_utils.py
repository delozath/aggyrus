import numpy as np


from aggyrus.core.signals._time_serie_types import SegmentedTimeSeries


def index_slice(
    loader: SegmentedTimeSeries,
) -> np.ndarray:
    if len(loader.segments) == 0:
        raise ValueError("No segments found in the record.")
    breakpoint()

