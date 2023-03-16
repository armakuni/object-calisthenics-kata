from random import randint
from typing import Dict, List

from src.intrastructure import datastore, mail_service
from src.intrastructure.datastore import DatastoreError


class CreateCasesError(Exception):
    pass


class CreateCases:
    def execute(self, questionnaire_id: str, respondents: List[Dict[str, str]]) -> None:
        try:
            datastore.fetch_one_by_field("questionnaires", "id", questionnaire_id)
        except DatastoreError:
            raise CreateCasesError(
                f"Questionnaire with ID {questionnaire_id} does not exist"
            )

        for respondent in respondents:
            uac = f"{str(randint(0, 999)).zfill(3)}-{str(randint(0, 999)).zfill(3)}"

            mail_service.send_email(respondent["email"], "Your UAC", f"UAC: {uac}")

            datastore.save(
                "cases",
                dict(
                    uac=uac,
                    questionnaire_id=questionnaire_id,
                    respondent_name=respondent["name"],
                    respondent_email=respondent["email"],
                    completed=False,
                    responses={},
                ),
            )
