from behave import given, then, when
from hamcrest import assert_that, equal_to, has_item
from steps.helpers import capture_exception

import src.questionnaire.actions.submit_response
from src.questionnaire.actions.view_responses import ViewResponsesError
from src.questionnaire.actions_factory import ActionsFactory


@given('there is no case with the user access code "{uac}"')
def ensure_case_does_not_exist(context, uac):
    # If we don't create it then it doesn't exist
    pass


@when('I submit responses for case "{uac}"')
@capture_exception(src.questionnaire.actions.submit_response.SubmitResponseError)
def submit_example_responses(context, uac):
    ActionsFactory.create_submit_response_action().execute(uac, {})


@given('"{respondent_name}" has submitted responses')
@when('"{respondent_name}" submits the following responses')
@capture_exception(src.questionnaire.actions.submit_response.SubmitResponseError)
def submit_responses(context, respondent_name):
    responses = {row["question"]: row["answer"] for row in context.table}
    ActionsFactory.create_submit_response_action().execute(
        context.uac_for[respondent_name], responses
    )


@when('I view the responses for the questionnaire "{questionnaire_name}"')
def view_responses_for_questionnaire(context, questionnaire_name):
    context.responses = ActionsFactory.create_view_responses_action().execute(
        context.questionnaire_id
    )


@then("I should see the responses")
def assert_responses(context):
    expected_responses = [dict(row.as_dict()) for row in context.table.rows]

    assert_that(
        len(context.responses),
        equal_to(len(expected_responses)),
        "Didn't get the expected number of responses",
    )

    for response in expected_responses:
        assert_that(context.responses, has_item(response))


@when('I view the responses for the questionnaire with ID "{questionnaire_id}"')
@capture_exception(ViewResponsesError)
def view_responses_for_questionnaire_with_d(context, questionnaire_id):
    context.responses = ActionsFactory.create_view_responses_action().execute(
        questionnaire_id
    )
