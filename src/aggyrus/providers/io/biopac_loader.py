from typing import Iterable, Sequence, Tuple, List, Dict, override

from pathlib import Path


import numpy as np
from numpy.typing import NDArray

import bioread


from aggyrus.spi.io import BaseSignalLoader
from aggyrus.core._time_serie_types import BaseTimeSeries
from aggyrus.api.signals import BiomedicalSignal

class BiopacLoader(BaseSignalLoader):
    @override
    def decode(
            self,
            source: str | Path,
            /, 
            ID = None,
            metadata = None,
            segments = None,
            annotations = None,
         ) -> BaseTimeSeries:
        record = bioread.read(source)
        data, chn_names = self._decode(record)
       
        sr = record.samples_per_second
        params = self._get_parameters(ID, metadata, segments, annotations)

        signal = BiomedicalSignal(
            data=data,
            sr=sr,
            chn_names=chn_names,
            **params
        )
        
        return signal
    
    def _get_parameters(self, ID, metadata, segments, annotations) -> Dict:
        keys  = ["ID", "metadata", "segments", "annotations"]
        values  = [ID, metadata, segments, annotations]
        params = {k: v for k, v in zip(keys, values) if v is not None}
        return params

    def _decode(self, record):
        chn_names = [] 
        data = []
        for chn in record.channels:
            if 'Channel' in str(chn):
                chn_names.append(chn.name)
                data.append(chn.data)
        
        chn_names = {nm: n for n, nm in enumerate (chn_names)}  
        data = np.array(data)

        return data, chn_names

    override
    def batch(self, sources: Iterable[str | Path], options: None = None) -> Iterable[BaseTimeSeries]:
        # Implement batch loading logic for Biopac files
        pass
    
    @override
    def windowed(
        self,
        source: str | Path,
        segments: Sequence[Tuple[float, float]],
        options: None = None
    ) -> List[BaseTimeSeries]:
        # Implement windowed loading logic for Biopac files
        pass