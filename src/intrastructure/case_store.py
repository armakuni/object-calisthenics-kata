from typing import Dict, List, TypedDict


class CaseStoreError(Exception):
    pass


class CaseRow(TypedDict):
    uac: str
    questionnaire_id: str
    respondent_name: str
    respondent_email: str
    completed: bool
    responses: Dict[str, str]


_CASES: Dict[str, CaseRow] = {}


def clear() -> None:
    _CASES.clear()


def save_case(case: CaseRow) -> None:
    _CASES[case["uac"]] = case


def fetch_by_uac(uac: str) -> CaseRow:
    if uac not in _CASES:
        raise CaseStoreError("Does not exist")

    return _CASES[uac]


def fetch_by_questionnaire_id(questionnaire_id: str) -> List[CaseRow]:
    return [
        case for case in _CASES.values() if case["questionnaire_id"] == questionnaire_id
    ]
