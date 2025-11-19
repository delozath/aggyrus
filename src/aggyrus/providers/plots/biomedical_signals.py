import enum
from typing import Any
from matplotlib import pyplot as plt


import numpy as np


from aggyrus.core.signals._time_serie_types import BiomedicalSignalRecord
from aggyrus.spi.plots import BaseContainerPlot

class BiomedicalSignalPlot(BaseContainerPlot[BiomedicalSignalRecord]):
    """
    class for plotting biomedical signals.

    Methods
    -------
    plot(signal: BiomedicalSignalRecord, /, size=None, **kwargs) -> Any
        Plots the biomedical signal data.

    show(/, **kwargs) -> None
        Displays the plotted biomedical signal. 
    """

    def plot(self, signal: BiomedicalSignalRecord, /, size=None, **kwargs) -> Any:
        """
        Plots the biomedical signal data. Generates time axis based on the signal's sampling rate.

        Parameters
        ----------
        signal : BiomedicalSignalRecord
            The biomedical signal record to be plotted.
        size : tuple, optional
            Size of the plot figure (width, height). Default is None.
        **kwargs : dict
            Additional keyword arguments for customization.

        Returns
        -------
        Any
        """
        time = np.arange(len(signal.data)) / signal.sr
        self._plot_factory(signal, time, **kwargs)
    
    def _plot_factory(self, signal: BiomedicalSignalRecord, time: np.ndarray, /, **kwargs) -> Any:
        """
        Factory method to determine the type of plot based on signal dimensions. If single channel, creates a single plot; if multi-channel, creates subplots.
        
        Parameters
        ----------
        signal : BiomedicalSignalRecord
            The biomedical signal record to be plotted.
        time : np.ndarray
            The time axis for the signal data.
        **kwargs : dict
            Additional keyword arguments for customization.
        
        Returns
        -------
        Any"""
        if signal.data.ndim == 1:
            self._single_plot(signal.data, time, **kwargs)
        elif signal.data.ndim != 1:
            if signal.data.shape[-1] == 1:
                self._single_plot(signal.data.squeeze(), time)
            else:
                self._subplots_signals(signal, time, **kwargs)
            plt.legend()
    
    def _single_plot(self, signal: np.ndarray, time: np.ndarray, /, **kwargs) -> Any:
        plt.figure(figsize=(18, 4))
        plt.plot(time, signal)
        plt.title("Biomedical Signal - Single Channel")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        
    
    def _subplots_signals(self, signal: BiomedicalSignalRecord, time: np.ndarray, /, **kwargs) -> Any:
        """
        Creates subplots for multi-channel biomedical signals.
        
        Parameters
        ----------
        signal : BiomedicalSignalRecord
            The biomedical signal record to be plotted.
        time : np.ndarray
            The time axis for the signal data.
        **kwargs : dict
            Additional keyword arguments for customization.
            
        Returns
        -------
        Any"""
        num_channels = signal.data.shape[1]
        name_channels = (
            signal.chn_names 
            if num_channels == len(signal.chn_names) 
            else [f'channel_{c}' for c in range(num_channels)]
        )
        
        fig, axes = plt.subplots(num_channels, 1, figsize=(18, 1.1 * num_channels), sharex=True)
        for i, (ax, x, cname) in enumerate(zip(axes, signal.data.T, name_channels)):
            ax.plot(time, x, label=cname)
            ax.set_title(f"{cname}", fontsize=10)
            ax.set_ylabel("Amplitude", fontsize=8)
            ax.grid()
        axes[-1].set_xlabel("Time (s)")
        plt.tight_layout()

    def show(self, /, **kwargs) -> None:
        if len(kwargs) > 0:
            plt.show(**kwargs)        
        else:
            plt.show()