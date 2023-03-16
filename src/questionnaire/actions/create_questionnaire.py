import uuid
from typing import Dict, List

from src.intrastructure import datastore


class CreateQuestionnaireError(Exception):
    pass


class CreateQuestionnaire:
    def execute(self, title: str, questions: List[Dict[str, str]]):
        if not questions:
            raise CreateQuestionnaireError(
                "Questionnaire must have at least one question"
            )

        questionnaire_id = str(uuid.uuid4())

        question_rows = []

        for question in questions:
            question_text = question["question"]
            if question["type"] == "text":
                question_type = "text"
            elif question["type"] == "count":
                question_type = "number"
            elif question["type"] == "yes/no":
                question_type = "bool"
            else:
                raise CreateQuestionnaireError(
                    "Invalid question type '{}' for question '{}'".format(
                        question["type"], question_text
                    )
                )

            question_rows.append(dict(question=question_text, type=question_type))

        datastore.save(
            "questionnaires",
            dict(
                id=questionnaire_id,
                title=title,
                questions=question_rows,
            ),
        )

        return questionnaire_id
