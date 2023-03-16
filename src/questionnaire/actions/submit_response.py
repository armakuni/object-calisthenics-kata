from src.intrastructure import datastore


class SubmitResponseError(Exception):
    pass


class SubmitResponse:
    def execute(self, uac: str, responses: dict) -> None:
        try:
            case = datastore.fetch_one_by_field("cases", "uac", uac)
            questionnaire = datastore.fetch_one_by_field(
                "questionnaires", "id", case["questionnaire_id"]
            )
            questions = {
                question["question"]: question
                for question in questionnaire["questions"]
            }
            for question, answer in responses.items():
                if question not in questions:
                    raise SubmitResponseError(
                        f"'{question}' is not a question in '{questionnaire['title']}'"
                    )
            for question in questions:
                if question not in responses:
                    raise SubmitResponseError(
                        f"'{question}' is a question in '{questionnaire['title']}' "
                        f"but has no answer"
                    )

            case["responses"] = {}
            for question, answer in responses.items():
                if questions[question]["type"] == "bool":
                    if answer not in ["yes", "no"]:
                        raise SubmitResponseError(
                            f"'{question}' must be 'yes' or 'no', got '{answer}'"
                        )
                elif questions[question]["type"] == "number":
                    if not answer.isnumeric():
                        raise SubmitResponseError(
                            f"'{question}' must be a number, got '{answer}'"
                        )

                case["responses"][question] = answer

            case["completed"] = True
            datastore.update("cases", "uac", case)
        except datastore.DatastoreError:
            raise SubmitResponseError(f"Case with UAC {uac} does not exist")
