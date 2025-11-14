import pytest


import numpy as np
from matplotlib import pyplot as plt
#import neurokit2 as nk


from aggyrus.providers.analysis.scipy_fft import ScipyFFTAnalyzer


TEST = 1

EPS_FREQ = 0.1
SR = 200.0
EPS_QUANTILE  = 0.988
MODE = 'dB' if TEST == 0 else 'power'


def gen_signal(duration=5, freqs=None, sr=100.0):
    if freqs is None:
        freqs = np.array([1.0, 5.0, 10.0, 25, 30])

    if freqs.max() > 2 * sr:
        raise ValueError("Frequencies exceed Nyquist limit.")
    
    t = np.arange(sr * duration) / sr
    signal = np.sin(2*np.pi * freqs * t[:, None]).sum(axis=1)
    return signal

@pytest.fixture
def spectrum_analyzer():
    fft_instance = ScipyFFTAnalyzer(sr=SR, mag_mode=MODE)
    return fft_instance


def test_ScipyFFTAnalyzer_apply(spectrum_analyzer):
    freqs = np.array([1.0, 5.0, 10.0, 25, 30, 80])
    signal = gen_signal(freqs=freqs, sr=SR)
    
    spectrum = spectrum_analyzer.compute(signal)
    spectrum_analyzer.plot(spectrum, size=(12, 4))
    max_freqs = spectrum.freq[spectrum.magnitude > np.quantile(spectrum.magnitude, EPS_QUANTILE)]
    assert all((max_freqs - freqs)**2 < EPS_FREQ)
    #nk.signal_plot(signal, sampling_rate=SR, subplots=True)
    plt.show()
    breakpoint()
    