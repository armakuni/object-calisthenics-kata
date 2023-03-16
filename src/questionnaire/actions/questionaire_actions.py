import uuid
from typing import Dict, List

from src.intrastructure import questionnaire_store
from src.intrastructure.questionnaire_store import (
    QuestionnaireStoreError,
    QuestionRow,
    QuestionTypeField,
)


class CreateQuestionnaireError(Exception):
    pass


def create_questionnaire(title: str, questions: List[Dict[str, str]]) -> str:
    if not questions:
        raise CreateQuestionnaireError("Questionnaire must have at least one question")

    questionnaire_id = str(uuid.uuid4())

    question_rows: List[QuestionRow] = []

    # TODO test existence of question
    for question in questions:
        question_text = question["question"]
        if question["type"] == "text":
            question_type = QuestionTypeField.TEXT
        elif question["type"] == "count":
            question_type = QuestionTypeField.NUMBER
        elif question["type"] == "yes/no":
            question_type = QuestionTypeField.BOOL
        else:
            raise CreateQuestionnaireError(
                "Invalid question type '{}' for question '{}'".format(
                    question["type"], question_text
                )
            )

        question_rows.append(dict(question=question_text, type=question_type))

    questionnaire_store.save_questionnaire(
        dict(
            id=questionnaire_id,
            title=title,
            questions=question_rows,
        )
    )

    return questionnaire_id


class ViewQuestionnaireError(Exception):
    pass


def view_questionnaire(questionnaire_id: str) -> dict:
    try:
        questionnaire = questionnaire_store.fetch_by_id(questionnaire_id)
    except QuestionnaireStoreError:
        raise ViewQuestionnaireError(
            f"Questionnaire with ID {questionnaire_id} does not exist"
        )

    questions = []
    for question in questionnaire["questions"]:
        if question["type"] == QuestionTypeField.TEXT:
            questions.append(dict(question=question["question"], type="text"))
        elif question["type"] == QuestionTypeField.NUMBER:
            questions.append(dict(question=question["question"], type="count"))
        elif question["type"] == QuestionTypeField.BOOL:
            questions.append(dict(question=question["question"], type="yes/no"))

    return dict(title=questionnaire["title"], questions=questions)
