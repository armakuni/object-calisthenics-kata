from typing import Dict, List

from behave import given, then, when
from hamcrest import assert_that, equal_to, has_key, has_property, has_string, is_not
from steps.helpers import capture_exception

import src.questionnaire.actions.questionaire_actions as questionnaire_actions
from src.questionnaire.actions.questionaire_actions import CreateQuestionnaireError


@given("there is a questionnaire")
def create_example_questionnaire(context):
    questions = [dict(question="Example question", type="text")]
    create_questionnaire(context, title="Example", questions=questions)


@given('there is no questionnaire with ID "{questionnaire_id}')
def delete_questionnaire_by_id(context, questionnaire_id):
    # if we don't create it then it doesn't exist
    pass


@given('there is a questionnaire "{title}" with questions')
@when('I create questionnaire with title "{title}" with questions')
def create_questionnaire_with_questions(context, title: str):
    questions = [
        dict(question=row["question"], type=row["type"]) for row in context.table.rows
    ]
    create_questionnaire(context, title=title, questions=questions)


@when('I create questionnaire with title "{title}" with no questions')
def create_questionnaire_without_questions(context, title):
    create_questionnaire(context, title=title, questions=[])


@when("I view the questionnaire")
def view_questionnaire(context):
    view_questionnaire_by_id(context, context.questionnaire_id)


@when('I view questionnaire "{questionnaire_id}"')
@capture_exception(questionnaire_actions.ViewQuestionnaireError)
def view_questionnaire_by_id(context, questionnaire_id: str):
    context.questionnaire = questionnaire_actions.view_questionnaire(questionnaire_id)


@then("I should receive a questionnaire ID")
def assert_questionnaire_id(context):
    assert_that(
        context, has_property("questionnaire_id"), "Expected a questionnaire ID"
    )
    assert_that(context.questionnaire_id, is_not(None))


@then('the title should be "{title}"')
def assert_questionnaire_title(context, title: str):
    assert_that(
        context,
        has_property("questionnaire"),
        "Expected a questionnaire, no questionnaire has been viewed",
    )
    assert_that(
        context.questionnaire,
        has_key("title"),
        "Expected a title, no title has been found",
    )
    assert_that(context.questionnaire["title"], equal_to(title))


@then("the questions should be")
def assert_questionnaire_questions(context):
    questions = [
        dict(question=row["question"], type=row["type"]) for row in context.table.rows
    ]
    assert_that(
        context,
        has_property("questionnaire"),
        "Expected a questionnaire, no questionnaire has been viewed",
    )
    assert_that(
        context.questionnaire,
        has_key("questions"),
        "Expected questions, no questions has been found",
    )
    assert_that(context.questionnaire["questions"], equal_to(questions))


@capture_exception(CreateQuestionnaireError)
def create_questionnaire(context, title: str, questions: List[Dict[str, str]]):
    context.questionnaire_id = questionnaire_actions.create_questionnaire(
        title=title, questions=questions
    )


def assert_last_error_message(context, message: str):
    assert_that(
        context,
        has_property("last_error"),
        "Expected an error, no error has been caught",
    )
    assert_that(context.last_error, has_string(message))
