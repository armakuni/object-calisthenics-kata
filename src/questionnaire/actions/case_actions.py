from random import randint
from typing import Dict, List

from src.intrastructure import case_store, mail_service, questionnaire_store


def create_cases(questionnaire_id: str, respondents: List[Dict[str, str]]) -> None:
    try:
        questionnaire_store.fetch_by_id(questionnaire_id)

        for respondent in respondents:
            uac = f"{str(randint(0, 999)).zfill(3)}-{str(randint(0, 999)).zfill(3)}"

            mail_service.send_email(respondent["email"], "Your UAC", f"UAC: {uac}")

            case_store.save_case(
                dict(
                    uac=uac,
                    questionnaire_id=questionnaire_id,
                    respondent_name=respondent["name"],
                    respondent_email=respondent["email"],
                    completed=False,
                    responses={},
                )
            )
    except questionnaire_store.QuestionnaireStoreError:
        raise CreateCasesError(
            f"Questionnaire with ID {questionnaire_id} does not exist"
        )


class CreateCasesError(Exception):
    pass
