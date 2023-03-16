from behave import then
from hamcrest import assert_that, has_property, has_string


@then('"{respondent_name}" receives an error "{message}"')
def assert_user_receives_error(context, respondent_name: str, message: str):
    assert_i_receive_error(context, message)


@then('I receive an error "{message}"')
def assert_i_receive_error(context, message: str):
    assert_that(
        context,
        has_property("last_error"),
        "Expected an error, no error has been caught",
    )
    assert_that(context.last_error, has_string(message))
