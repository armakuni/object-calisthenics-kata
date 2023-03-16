import re

from behave import given, then, when
from hamcrest import assert_that, equal_to, matches_regexp
from steps.helpers import capture_exception

from src.intrastructure import datastore, mail_service
from src.intrastructure.mail_service import Email
from src.questionnaire.actions.create_cases import CreateCasesError
from src.questionnaire.actions_factory import ActionsFactory


@given('there is a case for respondent "{respondent_name}" for the questionnaire')
def create_case_for_respondent(context, respondent_name: str):
    email_address = f"{respondent_name.lower()}@minions.evil"
    context.respondents = [dict(email=email_address, name=respondent_name)]
    ActionsFactory.create_create_cases_action().execute(
        context.questionnaire_id, context.respondents
    )

    uac_email = mail_service.get_last_email_to(email_address)
    uac = extract_uac(uac_email)
    context.case_uac = uac
    context.uac_for[respondent_name] = uac


@given("there are cases for respondents")
@when("I create cases for the questionnaire for respondents")
def create_cases(context):
    context.respondents = [
        dict(email=row["email_address"], name=row["name"]) for row in context.table.rows
    ]
    ActionsFactory.create_create_cases_action().execute(
        context.questionnaire_id, context.respondents
    )
    context.uac_for = {
        respondent["name"]: extract_uac(
            mail_service.get_last_email_to(respondent["email"])
        )
        for respondent in context.respondents
    }


@when('I create some cases for questionnaire "{questionnaire_id}"')
@capture_exception(CreateCasesError)
def create_example_cases(context, questionnaire_id):
    respondents = [
        dict(email="norbert@minions.evil", name="Norbert"),
        dict(email="kevin@minions.evil", name="Kevin"),
    ]
    ActionsFactory.create_create_cases_action().execute(questionnaire_id, respondents)


@then("each respondent should should receive an email with a unique access code")
def assert_unique_access_code_emails(context):
    uacs = [
        get_uac_for_respondent(respondent["email"])
        for respondent in context.respondents
    ]
    assert_that(len(set(uacs)), equal_to(len(uacs)), f"UACs are not unique: {uacs}")


@then("the case should be completed")
def assert_case_completed(context):
    case = datastore.fetch_one_by_field("cases", "uac", context.case_uac)
    assert case["completed"] is True


@then("the cases should not be completed")
def assert_cases_are_not_completed(context):
    for respondent in context.respondents:
        uac = get_uac_for_respondent(respondent["email"])
        case = datastore.fetch_one_by_field("cases", "uac", uac)
        assert (
            case["completed"] is False
        ), f"Case {uac} for response {respondent} should not be completed"


def get_uac_for_respondent(email_address: str) -> str:
    email = mail_service.get_last_email_to(email_address)
    return extract_uac(email)


def extract_uac(email: Email) -> str:
    assert_that(email["subject"], equal_to("Your UAC"))
    assert_that(email["body"], matches_regexp(r"UAC: \d\d\d-\d\d\d"))
    match = re.search(r"UAC: (\d\d\d-\d\d\d)", email["body"])
    if not match:
        raise AssertionError(f"UAC not found in email body: {email['body']}")
    return match[1]
