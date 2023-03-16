import pytest

from src.intrastructure import mail_service, questionnaire_store


@pytest.fixture(autouse=True)
def clear_global_state():
    # This is a nasty global memory storage system, so we'll tidy up before each test
    questionnaire_store.clear()
    mail_service.clear()
