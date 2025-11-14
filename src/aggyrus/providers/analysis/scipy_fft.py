import numpy as np
from scipy import signal as sg
from scipy import fft
from typing import Any, Callable, Dict, Tuple, Literal, override

from aggyrus.core.validations.signature import save_init_kwargs
from aggyrus.spi.analysis import SpectrumAnalyzerParams, SpectrumAnalyzer, SpectrumContainer

from matplotlib import pyplot as plt

class ScipyFFTAnalyzer(SpectrumAnalyzer):
    def __init__(self, sr: float = 100.0, mag_mode: Literal['dB', 'power'] = 'power'):
        self.name = "scipy_fft_analyzer"
        self.params = SpectrumAnalyzerParams(sr=sr, mag_mode=mag_mode)

    def compute(self, signal: np.ndarray, *, phase_mode=None, **kwargs) -> SpectrumContainer:
        shape = signal.shape
        freq = np.linspace(0, self.params.sr/2, shape[0]//2)
        transform = fft.fft(signal)[:shape[0]//2]

        mag = self._magnitude_factory(self.params.mag_mode, transform)
        spectrum = SpectrumContainer(
            freq=freq,
            magnitude=mag,
            phase= np.angle(transform) if phase_mode == 'angle' else None,
            sr=self.params.sr,
            mag_mode=self.params.mag_mode
        )
        return spectrum
    
    def perform(self, /, **kwargs) -> None:...
    
    @override
    def plot(self, spectrum: SpectrumContainer, /, **kwargs) -> Any:
        plot_func = self._plot_factory(spectrum, **kwargs)
        plot_func(spectrum.freq, spectrum.magnitude)
        plt.show()
        breakpoint()
        
        plt.show()
        return plt.gcf()
    
    def _plot_factory(self, spectrum, size=(18, 6)) -> Any:
        #TODO: implement phase plotting in subplots if phase data is provided
        plt.figure(figsize=size)

        if spectrum.mag_mode == 'power':
            title = 'Power Spectrum'
            y_label = 'Power'
            func = plt.semilogy
        else:
            title = 'Magnitude Spectrum (dB)'
            y_label = 'Magnitude'
            func = plt.plot
        
        plt.xlabel('Frequency (Hz)')
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()
        return func
        

    def show(self, /, **kwargs) -> None:...