import pytest


from matplotlib import pyplot as plt


from aggyrus.providers.filters.scipy_filters import ButterworthFilter
from aggyrus.providers.analysis.scipy_fft import ScipyFFTAnalyzer

import numpy as np
import pandas as pd
import neurokit2 as nk

from aggyrus.spi.errors import FilterInitializerError


def gen_signal(duration=5, freqs=None, sr=100.0):
    if freqs is None:
        freqs = np.array([1.0, 5.0, 10.0, 25, 30])

    if freqs.max() > 2 * sr:
        raise ValueError("Frequencies exceed Nyquist limit.")
    
    t = np.arange(sr * duration) / sr
    signal = np.sin(2*np.pi * freqs * t[:, None]).sum(axis=1)
    return signal

@pytest.fixture
def butterworth_filter():
    filter_instance = ButterworthFilter()
    """    
    filter_instance.design(
        order=4,
        cutoff=np.array([0.1, 20]),
        btype='bandpass',
        sr=100.0,
        analog=False
    )"""
    return filter_instance

def test_ButterworthFilter_design(butterworth_filter):
    butterworth_filter.design(
        order=4,
        cutoff=np.array([0.1, 20]),
        #btype='lowpass',
        sr=300.0,
        analog=False
    )
    assert hasattr(butterworth_filter, 'model')
    assert butterworth_filter.filter_.sr == 300.0
    assert butterworth_filter.filter_.btype == 'bandpass'
    assert butterworth_filter.filter_.output == 'sos'

    butterworth_filter.design(
        order=8,
        cutoff=30.,
        btype='lowpass',
        output='ba'
    )
    assert butterworth_filter.filter_.order == 8
    assert butterworth_filter.filter_.btype == 'lowpass'
    assert butterworth_filter.filter_.cutoff == 30.
    assert butterworth_filter.filter_.output == 'ba'

    with pytest.raises(FilterInitializerError):
        butterworth_filter.design(order=-2)
        butterworth_filter.design(cutoff="invalid")
        butterworth_filter.design(btype="notch")
        butterworth_filter.design(sr=-100)
        butterworth_filter.design(analog="yes")
        butterworth_filter.design(output="invalid")
        butterworth_filter.design(sr=10, cutoff=np.array([6, 10]))


def test_ButterworthFilter_apply(butterworth_filter):
    sr = 200.0
    freqs = np.array([1.0, 5.0, 10.0, 25, 30, 80])
    order = 8
    butterworth_filter.design(
        order=order,
        cutoff=np.array([0.1, 20]),
        btype='bandpass',
        sr=sr,
        analog=False,
        output='sos'
    )
    signal = gen_signal(freqs=freqs, sr=sr)
    filt_signal = butterworth_filter.apply(signal, mode='filt')
    filtfilt_signal = butterworth_filter.apply(signal, mode='filtfilt')
    signals = pd.DataFrame([signal, filt_signal, filtfilt_signal]).T
    signals.columns = ['Original Signal', 'Filtered Signal', 'Zero-phase filt Signal']
    fft = ScipyFFTAnalyzer(sr=sr, mag_mode='dB')
    
    spectrum = fft.compute(signal)
    fft.plot(spectrum)
    nk.signal_plot(signals, sampling_rate=sr, subplots=True)
    breakpoint()

    plt.show()
    breakpoint()
