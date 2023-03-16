import pytest

from src.intrastructure import datastore, mail_service


@pytest.fixture(autouse=True)
def clear_global_state():
    # This is a nasty global memory storage system, so we'll tidy up before each test
    datastore.clear()
    mail_service.clear()
