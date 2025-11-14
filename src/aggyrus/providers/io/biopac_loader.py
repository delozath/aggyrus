from typing import Iterable, Dict, override

from pathlib import Path


import numpy as np

import bioread


from aggyrus.core.validations.descriptors import TypedMutableDescr
from aggyrus.core.signals._time_serie_types import BaseTimeSeries
from aggyrus.core.signals._time_serie_types import BiomedicalSignalRecord
from aggyrus.spi.errors import IOProviderReadError
from aggyrus.spi.io import BaseSignalLoader


class BiopacLoader(BaseSignalLoader):
    record = TypedMutableDescr(BiomedicalSignalRecord)

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
        try:
            loader = bioread.read(source)
        except Exception as e:
            raise IOProviderReadError(f"An error occurred while reading the Biopac file: {e}") from e
        else:            
            data, chn_names = self._decode(loader)
            sr = loader.samples_per_second
            params = self._get_parameters(ID, metadata, segments, annotations)

            record = BiomedicalSignalRecord(
                data=data,
                sr=sr,
                chn_names=chn_names,
                **params
            )
            self.record = record
            return record
    
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

    @override
    def batch(self, sources: Iterable[str | Path], options: None = None) -> Iterable[BaseTimeSeries]:
        raise NotImplementedError("This class only supports single file loading")
