# Using global state like this module does is bad design. It specifically does
# this to promote the idea of abstracting it out during the exercise.
from enum import Enum
from typing import Dict, List, TypedDict


class QuestionTypeField(Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOL = "bool"


class QuestionRow(TypedDict):
    question: str
    type: QuestionTypeField


class QuestionnaireRow(TypedDict):
    id: str
    title: str
    questions: List[QuestionRow]


_QUESTIONNAIRES: Dict[str, QuestionnaireRow] = {}


class QuestionnaireStoreError(Exception):
    pass


def clear() -> None:
    _QUESTIONNAIRES.clear()


def save_questionnaire(questionnaire: QuestionnaireRow) -> None:
    _QUESTIONNAIRES[questionnaire["id"]] = questionnaire


def fetch_by_id(questionnaire_id: str) -> QuestionnaireRow:
    if questionnaire_id not in _QUESTIONNAIRES:
        raise QuestionnaireStoreError("Does not exist")
    return _QUESTIONNAIRES[questionnaire_id]
