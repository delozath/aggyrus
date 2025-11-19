import pytest


from matplotlib import pyplot as plt


from aggyrus.providers.plots.biomedical_signals import BiomedicalSignalPlot
from aggyrus.core.signals._time_serie_types import BiomedicalSignalRecord

import numpy as np
import pandas as pd



EPS_FREQ = 0.1
SR = 100.0

def gen_signal(duration=5, freqs=None, sr=SR):
    if freqs is None:
        freqs = np.array([1.0, 5.0, 10.0, 25, 30])

    if freqs.max() > 2 * sr:
        raise ValueError("Frequencies exceed Nyquist limit.")
    
    t = np.arange(sr * duration) / sr
    signal = np.sin(2*np.pi * freqs * t[:, None]).sum(axis=1)
    return signal

@pytest.fixture
def signal_plot():
    instance = BiomedicalSignalPlot()
    return instance

def test_BiomedicalSignalPlot_plot_single_signal(signal_plot):
    signal = gen_signal()
    record = BiomedicalSignalRecord(data=signal, chn_names=["channel_1"], sr=SR)
    result = signal_plot.plot(record)
    signal_plot.show()

def test_BiomedicalSignalPlot_plot_multiple_channel(signal_plot):
    signal = gen_signal()
    signal_2 = gen_signal(freqs=np.array([2.0, 8.0, 15.0]))

    x = np.concatenate([signal[:, None], signal_2[:, None], signal[:, None], signal_2[:, None], signal[:, None], signal_2[:, None]], axis=1)
    record_multi = BiomedicalSignalRecord(data=x, chn_names=["channel_-1", "channel_-2", "channel_3", "channel_4", "channel_0", "channel_6"], sr=SR)
    result = signal_plot.plot(record_multi)
    signal_plot.show()
