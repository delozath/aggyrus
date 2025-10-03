import re
import traceback



import bioread

import numpy as np


from aggyrus.validation.errors import ChannelNotFound

"""
Class biopac
------------
Defines a class `biopac` to encapsulate the process of loading, decoding, and manipulating physiological data from BIOPAC systems.
"""
class BiopacDriver:
    def __init__(self, fname):
        """
        Initializes a biopac object by loading data from a .acq file.

        Parameters
        ----------
        fname : str
            Filename/path of the .acq file to be loaded.
        """
        record = bioread.read(fname)  
        self.sr = record.samples_per_second  
        self.time = record.time_index  
        self.record = record  
    
    def decode(self):
        """
        Method to create a biopac instance, extract data, and assign a subject identifier.

        Parameters
        ----------
        subject : str
            Identifier for the subject whose data is being decoded.
        """
        self._extract_data()  
    
    def _extract_data(self):
        """
        Extracts channel data from the .acq file and organizes it into a structured format.
        """
        names = [] 
        data = []
        for chan in self.record.channels:
            if 'Channel' in str(chan):
                names.append(chan.name)
                data.append(chan.data)
        self._names = {nm: n for n, nm in enumerate (names)}
        self.names = np.array(names)  
        self.data = np.array(data)

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                idx = self._get_index(key)
                return self.data[idx]
            except ChannelNotFound as e:
                print(e.with_traceback())
        elif isinstance(key, (list, tuple, np.ndarray)):
            #if all(map(lambda k: isinstance(k, str), key)):
            keys_idx = [self._get_index(k) for k in key]
            return self.data[keys_idx]
        else:
            raise TypeError("key types expected: str | list[str] | tuple[str] | np.ndarray[U]")
    
    def _get_index(self, key):
        if key in self.names:
            return self._names[key]
        else:
            raise ChannelNotFound(f"Channel {key} not found...")


class EPPSignalBiopac(BiopacDriver):
    CHANN = ['ECG_A', 'PPG_1', 'PPG_2', 'BP', 'SPO2_1', 'SPO2_2']
    
    def __init__(self, fname):
        super().__init__(fname)

        match = re.search(r'([^/]+)(?=\.[^/.]+$)', fname)
        self.subject = match.group(0)
        self.decode()        