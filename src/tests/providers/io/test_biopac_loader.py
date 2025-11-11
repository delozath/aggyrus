import pytest

import os
from dotenv import load_dotenv
load_dotenv()


from aggyrus.providers.io import BiopacLoader


@pytest.fixture
def biopac_loader():
    return BiopacLoader()

def test_BiopacLoader_decode(biopac_loader):
    pfname = os.getenv("ACQ_TEST_FILE")
    biopac_loader.decode(pfname)
    breakpoint()

def test_BiopacLoader_batch(biopac_loader):
    pass

def test_BiopacLoader_windowed(biopac_loader):
    pass

    