import pytest


from aggyrus.providers.filters.scipy_filters import ButterworthFilter

from scipy.signal import butter, filtfilt
import numpy as np

@pytest.fixture
def butterworth_filter():
    filter_instance = ButterworthFilter()
    """    
    filter_instance.design(
        order=4,
        cutoff=np.array([0.1, 20]),
        btype='bandpass',
        fs=100.0,
        analog=False
    )"""
    return filter_instance

def test_ButterworthFilter_design(butterworth_filter):
    butterworth_filter.design(
        order=4,
        cutoff=np.array([0.1, 20]),
        #btype='lowpass',
        fs=100.0,
        analog=False
    )
    assert hasattr(butterworth_filter, 'b')
    assert hasattr(butterworth_filter, 'a')

def test_ButterworthFilter_apply(butterworth_filter):
    butterworth_filter.design(
        order=4,
        cutoff=np.array([0.1, 20]),
        btype='bandpass',
        fs=100.0,
        analog=False
    )
    pass