import re

import traceback

from abc import ABC, abstractmethod
from typing import override


import bioread

import numpy as np


from aggyrus.validation.errors import ChannelNotFound

class BiosignalDriver(ABC):
    def __init__(self, sr, time, signals, names) -> None:
        self._sr = sr
        self._time = time
        self._signals = signals
        self._names = names
    
    @property
    def sr(self):
        return self._sr
    
    @property
    def time(self):
        return self._time
    
    @property
    def signals(self):
        return self._signals
    
    @property
    def names(self):
        return self._names

    @abstractmethod
    def decode(self, *args, **kwargs):
        ...



"""
Class biopac
------------
Defines a class `biopac` to encapsulate the process of loading, decoding, and manipulating physiological data from BIOPAC systems.
"""
class BiopacDriver(BiosignalDriver):
    def __init__(self, fname):
        """
        Initializes a biopac object by loading data from a .acq file.

        Parameters
        ----------
        fname : str
            Filename/path of the .acq file to be loaded.
        """
        record = bioread.read(fname)
        data, names, _names = self.decode(record)
        super().__init__(
            sr=record.samples_per_second,
            time=record.time_index,
            signals=data,
            names=names
         )
        
        self.record = record
        self._names_hash = _names
    
    @override
    def decode(self, record):
        """
        Method that extract data and metadata from biopac instance

        Parameters
        ----------
        subject : str
            Identifier for the subject whose data is being decoded. Extracts channel data from the .acq file and organizes it into a structured format.
        """
        names = [] 
        data = []
        for chan in record.channels:
            if 'Channel' in str(chan):
                names.append(chan.name)
                data.append(chan.data)
        _names = {nm: n for n, nm in enumerate (names)}
        names = np.array(names)  
        data = np.array(data)

        return data, names, _names

    def __getitem__(self, key):
        if isinstance(key, str):
            idx = self._get_index(key)
            return self._signals[idx]
        elif isinstance(key, (list, tuple, np.ndarray)):
            #if all(map(lambda k: isinstance(k, str), key)):
            keys_idx = [self._get_index(k) for k in key]
            return self._signals[keys_idx]
        else:
            raise TypeError("key types expected: str | list[str] | tuple[str] | np.ndarray[U]")
    
    def _get_index(self, key):
        if key in self.names:
            return self._names_hash[key]
        else:
            raise ChannelNotFound(f"Channel {key} not found...")


class EPPSignalBiopac(BiopacDriver):
    CHANN = ['ECG_A', 'PPG_1', 'PPG_2', 'BP', 'SPO2_1', 'SPO2_2']
    
    def __init__(self, fname):
        super().__init__(fname)

        match = re.search(r'([^/]+)(?=\.[^/.]+$)', fname)
        self.subject = match.group(0)       