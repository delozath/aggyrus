import enum
from typing import Any
from matplotlib import pyplot as plt


import numpy as np


from aggyrus.core.signals._time_serie_types import BiomedicalSignalRecord
from aggyrus.spi.plots import BaseContainerPlot

class BiomedicalSignalPlot(BaseContainerPlot[BiomedicalSignalRecord]):
    SIZE = (16, 8)
    def plot(self, signal: BiomedicalSignalRecord, /, size=None, **kwargs) -> Any:
        size = size if size is not None else self.SIZE
        time = np.arange(len(signal.data)) / signal.sr
        self._plot_factory(signal, time, **kwargs)
        breakpoint()
    
        plt.figure(figsize=(10, 4))
        plt.plot(time, signal.data)
        plt.title("Biomedical Signal")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()
    
    def _plot_factory(self, signal: BiomedicalSignalRecord, time: np.ndarray, /, **kwargs) -> Any:
        if signal.data.ndim == 1:
            self._single_plot(signal.data, time, **kwargs)
        elif signal.data.ndim != 1:
            if signal.data.shape[-1] == 1:
                self._single_plot(signal.data.squeeze(), time)
            else:
                self._subplots_signals(signal.data, time, **kwargs)
            plt.legend()
        breakpoint()
    
    def _single_plot(self, signal: np.ndarray, time: np.ndarray, /, **kwargs) -> Any:
        plt.figure(figsize=(10, 4))
        plt.plot(time, signal)
        plt.title("Biomedical Signal - Single Channel")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()
    
    def _subplots_signals(self, signal: np.ndarray, time: np.ndarray, /, **kwargs) -> Any:
        num_channels = signal.shape[1]
        fig, axes = plt.subplots(num_channels, 1, figsize=(18, 1.1 * num_channels), sharex=True)
        for i, (ax, sig) in enumerate(zip(axes, signal.T)):
            ax.plot(time, sig)
            ax.set_title(f"Channel {i+1}")
            ax.set_ylabel("Amplitude")
            ax.grid()
        axes[-1].set_xlabel("Time (s)")
        plt.tight_layout()
        plt.show()

    def show(self, /, **kwargs) -> None:
        # Implementation for showing the plot
        pass