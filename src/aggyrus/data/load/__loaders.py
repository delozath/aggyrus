import re


import bioread

import numpy as np

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
        self.subject = 'known'  
    
    def decode(self, subject):
        """
        Method to create a biopac instance, extract data, and assign a subject identifier.

        Parameters
        ----------
        subject : str
            Identifier for the subject whose data is being decoded.
        """
        self._extract_data()  
        self.subject = subject  
    
    def _extract_data(self):
        """
        Extracts channel data from the .acq file and organizes it into a structured format.
        """
        chn_names = {}  
        data = []  
        for n, chan in enumerate(self.record.channels):
            cname = re.match(r"(Channel )(\w+)(?=:)", str(chan))[2]
            chn_names[cname] = n
            data.append(chan.data)
        self.chn_names = chn_names  
        self.data = np.array(data)  
 
class EPPSignalBiopac(BiopacDriver):
    CHANN = ['ECG_A', 'PPG_1', 'PPG_2', 'BP', 'SPO2_1', 'SPO2_2']
    
    def __init__(self, fname):
        super().__init__(fname)
        match = re.search(r'([^/]+)(?=\.[^/.]+$)', fname)
        subject = match.group(0)
        self.decode(subject)
        channels = (lambda names: [names[chn] for chn in EPPSignalBiopac.CHANN])(self.chn_names)
        self.data = self.data[channels]