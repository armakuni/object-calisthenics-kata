from src.intrastructure import datastore
from src.intrastructure.datastore import DatastoreError


class ViewQuestionnaireError(Exception):
    pass


class ViewQuestionnaire:
    def execute(self, questionnaire_id: str) -> dict:
        try:
            questionnaire = datastore.fetch_one_by_field(
                "questionnaires", "id", questionnaire_id
            )
        except DatastoreError:
            raise ViewQuestionnaireError(
                f"Questionnaire with ID {questionnaire_id} does not exist"
            )

        questions = []
        for question in questionnaire["questions"]:
            if question["type"] == "text":
                questions.append(dict(question=question["question"], type="text"))
            elif question["type"] == "number":
                questions.append(dict(question=question["question"], type="count"))
            elif question["type"] == "bool":
                questions.append(dict(question=question["question"], type="yes/no"))

        return dict(title=questionnaire["title"], questions=questions)
