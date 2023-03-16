from src.questionnaire.actions.create_cases import CreateCases
from src.questionnaire.actions.create_questionnaire import CreateQuestionnaire
from src.questionnaire.actions.submit_response import SubmitResponse
from src.questionnaire.actions.view_questionnaire import ViewQuestionnaire
from src.questionnaire.actions.view_responses import ViewResponses


class ActionsFactory:
    @staticmethod
    def create_create_questionnaire_action() -> CreateQuestionnaire:
        return CreateQuestionnaire()

    @staticmethod
    def create_view_questionnaire_action() -> ViewQuestionnaire:
        return ViewQuestionnaire()

    @staticmethod
    def create_create_cases_action() -> CreateCases:
        return CreateCases()

    @staticmethod
    def create_submit_response_action() -> SubmitResponse:
        return SubmitResponse()

    @staticmethod
    def create_view_responses_action() -> ViewResponses:
        return ViewResponses()
