from dataclasses import dataclass, field
from typing import Tuple, Dict

import numpy as np
from numpy.typing import NDArray

@dataclass
class BaseTimeSeries:
    data: NDArray[np.float_]
    fs: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class LabeledTimeSeries(BaseTimeSeries):
    chn_names: Tuple[str, ...] | Dict[str, int] = field(default_factory=tuple)


@dataclass
class AnnotatedTimeSeries(BaseTimeSeries):
    annotations: NDArray[np.float_] = field(default_factory=lambda: np.array([]))


@dataclass
class SegmentedTimeSeries(BaseTimeSeries):
    segments: NDArray[np.float_] = field(default_factory=lambda: np.array([]))


@dataclass
class BiomedicalSignal(LabeledTimeSeries, AnnotatedTimeSeries, SegmentedTimeSeries):
    id: str | int | None = None