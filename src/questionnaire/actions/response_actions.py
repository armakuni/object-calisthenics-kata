from typing import Dict, List

from src.intrastructure import case_store, questionnaire_store


class SubmitResponseError(Exception):
    pass


def submit_response(uac: str, answers: dict) -> None:
    try:
        case = case_store.fetch_by_uac(uac)
        questionnaire = questionnaire_store.fetch_by_id(case["questionnaire_id"])
        questions = {
            question["question"]: question for question in questionnaire["questions"]
        }
        for question, answer in answers.items():
            if question not in questions:
                raise SubmitResponseError(
                    f"'{question}' is not a question in '{questionnaire['title']}'"
                )
        for question in questions:
            if question not in answers:
                raise SubmitResponseError(
                    f"'{question}' is a question in '{questionnaire['title']}' "
                    f"but has no answer"
                )

        case["completed"] = True
        case["responses"] = answers
        case_store.save_case(case)
    except case_store.CaseStoreError:
        raise SubmitResponseError(f"Case with UAC {uac} does not exist")


class ViewResponsesError(Exception):
    pass


def view_responses(questionnaire_id: str) -> List[Dict[str, str]]:
    try:
        questionnaire = questionnaire_store.fetch_by_id(questionnaire_id)

        case_rows = case_store.fetch_by_questionnaire_id(questionnaire_id)

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

    except questionnaire_store.QuestionnaireStoreError:
        raise ViewResponsesError(
            f"Questionnaire with ID {questionnaire_id} does not exist"
        )
