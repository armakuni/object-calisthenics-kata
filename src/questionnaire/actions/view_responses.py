from typing import Dict, List

from src.intrastructure import datastore
from src.intrastructure.datastore import DatastoreError


class ViewResponsesError(Exception):
    pass


class ViewResponses:
    def execute(self, questionnaire_id: str) -> List[Dict[str, str]]:
        try:
            questionnaire = datastore.fetch_one_by_field(
                "questionnaires", "id", questionnaire_id
            )
        except DatastoreError:
            raise ViewResponsesError(
                f"Questionnaire with ID {questionnaire_id} does not exist"
            )

        case_rows = datastore.fetch_by_field(
            "cases", "questionnaire_id", questionnaire_id
        )

        responses: List[Dict[str, str]] = []
        for case in case_rows:
            case_responses = {
                question["question"]: case["responses"][question["question"]]
                if case["completed"]
                else ""
                for question in questionnaire["questions"]
            }
            response = dict(
                respondent=case["respondent_name"],
                case_complete="yes" if case["completed"] else "no",
                **case_responses,
            )
            responses.append(response)

        return responses
