import pytest

import os
from dotenv import load_dotenv
load_dotenv()


import numpy as np


from aggyrus.providers.io import BiopacLoader
from aggyrus.core.signals._utils import index_slice


@pytest.fixture
def biopac_loader():
    loader = BiopacLoader()
    pfname = os.getenv("ACQ_TEST_FILE")
    loader.decode(pfname)
    return loader

def test_BiopacLoader_decode(biopac_loader):
    breakpoint()
    index_slice(biopac_loader.record)
    