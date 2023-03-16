import pytest
from hamcrest import assert_that, equal_to

from src.intrastructure import case_store
from src.intrastructure.case_store import CaseRow


@pytest.fixture()
def case1() -> CaseRow:
    return dict(
        uac="123-001",
        questionnaire_id="c1f0bf95-c693-4077-98ec-401709a75d5d",
        respondent_email="kevin@minions.evil",
        respondent_name="Kevin",
        completed=False,
        responses={},
    )


@pytest.fixture()
def case2() -> CaseRow:
    return dict(
        uac="123-002",
        questionnaire_id="c1f0bf95-c693-4077-98ec-401709a75d5d",
        respondent_email="norbert@minions.evil",
        respondent_name="Norbert",
        completed=False,
        responses={},
    )


@pytest.fixture()
def case3() -> CaseRow:
    return dict(
        uac="123-003",
        questionnaire_id="c1f0bf95-c693-4077-98ec-401709a75d5d",
        respondent_email="stuart@minions.evil",
        respondent_name="Stuart",
        completed=False,
        responses={},
    )


def test_clear(case1):
    case_store.save_case(case1)
    case_store.clear()
    with pytest.raises(case_store.CaseStoreError, match="Does not exist"):
        case_store.fetch_by_uac(case1["uac"])


class TestFetchByUac:
    def test_returns_the_case(self, case1):
        case_store.save_case(case1)
        fetched_case = case_store.fetch_by_uac(case1["uac"])
        assert_that(fetched_case, equal_to(case1))

    def test_raise_an_error_when_case_does_not_exist(self):
        with pytest.raises(case_store.CaseStoreError, match="Does not exist"):
            case_store.fetch_by_uac("567-890")


class TestFetchByQuestionnaireID:
    def test_returns_cases_for_questionnaire(self, case1, case2, case3):
        questionnaire1_id = "a9817d78-4c5c-4bf3-aa53-9e49a3eb6bfb"
        questionnaire2_id = "aa0be0eb-87da-4cfd-9f15-b97b6b171724"
        case1["questionnaire_id"] = questionnaire1_id
        case2["questionnaire_id"] = questionnaire1_id
        case3["questionnaire_id"] = questionnaire2_id

        case_store.save_case(case1)
        case_store.save_case(case2)
        case_store.save_case(case3)

        cases = case_store.fetch_by_questionnaire_id(questionnaire1_id)

        assert_that(cases, equal_to([case1, case2]))
