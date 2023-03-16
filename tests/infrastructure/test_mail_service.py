import pytest
from hamcrest import assert_that, equal_to

from src.intrastructure import mail_service


@pytest.fixture(autouse=True)
def before_each():
    mail_service.send_email(
        "stuart@minions.evil",
        "Minion News Letter",
        "Dear Stuart,\n" "\n" "Here is you weekly update of minion related activities!",
    )
    mail_service.send_email(
        "bob@minions.evil",
        "Minion News Letter",
        "Dear Bob,\n" "\n" "Here is you weekly update of minion related activities!",
    )


def test_clear_removes_all_emails():
    mail_service.clear()

    with pytest.raises(mail_service.EmailNotFoundError):
        mail_service.get_last_email_to("stuart@minions.evil")

    with pytest.raises(mail_service.EmailNotFoundError):
        mail_service.get_last_email_to("kevin@minions.evil")


def test_get_last_email_to_when_email_not_sent():
    with pytest.raises(
        mail_service.EmailNotFoundError,
        match="No email has been sent to kevin@minions.evil",
    ):
        mail_service.get_last_email_to("kevin@minions.evil")


@pytest.mark.parametrize(
    "email_address,name",
    [
        ("stuart@minions.evil", "Stuart"),
        ("bob@minions.evil", "Bob"),
    ],
)
def test_get_last_email_to_when_email_exists(email_address, name):
    email = mail_service.get_last_email_to(email_address)
    assert_that(email["subject"], equal_to("Minion News Letter"))
    assert_that(
        email["body"],
        equal_to(
            f"Dear {name},\n"
            f"\n"
            f"Here is you weekly update of minion related activities!"
        ),
    )


def test_get_last_email_to_returns_the_last_email():
    mail_service.send_email("stuart@minions.evil", "Recent announcement", "")
    email = mail_service.get_last_email_to("stuart@minions.evil")
    assert_that(email["subject"], equal_to("Recent announcement"))
