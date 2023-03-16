from typing import Dict, TypedDict


class EmailNotFoundError(Exception):
    pass


class Email(TypedDict):
    to: str
    subject: str
    body: str


_EMAIL: Dict[str, Email] = {}


def clear() -> None:
    _EMAIL.clear()


def get_last_email_to(email_address: str) -> Email:
    if email_address not in _EMAIL:
        raise EmailNotFoundError(f"No email has been sent to {email_address}")

    return _EMAIL[email_address]


def send_email(to: str, subject: str, body: str) -> None:
    _EMAIL[to] = dict(
        to=to,
        subject=subject,
        body=body,
    )
