import pytest
from hamcrest import assert_that, equal_to

from src.intrastructure import questionnaire_store
from src.intrastructure.questionnaire_store import QuestionnaireStoreError


@pytest.fixture()
def case1():
    return dict(
        id="c1f0bf95-c693-4077-98ec-401709a75d5d",
        title="My Questionnaire",
        questions=[dict(question="What is your name?", type="text")],
    )


def test_clear(case1):
    questionnaire_store.save_questionnaire(case1)
    questionnaire_store.clear()
    with pytest.raises(QuestionnaireStoreError, match="Does not exist"):
        questionnaire_store.fetch_by_id(case1["id"])


def test_fetching_a_questionnaire(case1):
    questionnaire_store.save_questionnaire(case1)
    fetched_questionnaire = questionnaire_store.fetch_by_id(case1["id"])
    assert_that(fetched_questionnaire, equal_to(case1))


def test_fetching_a_questionnaire_that_does_not_exist():
    with pytest.raises(QuestionnaireStoreError, match="Does not exist"):
        questionnaire_store.fetch_by_id("3f1fd0f2-7a1b-4a81-8cf1-061a9b1fcf8f")
