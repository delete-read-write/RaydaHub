import pytest

from raydahub.modules.user.value_objects import Email, HashedPassword


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("user@example.com", "user@example.com"),
        ("User@Example.COM", "user@example.com"),
        ("  user@example.com\n", "user@example.com"),
    ],
)
def test_email_normalizes_value(raw: str, expected: str) -> None:
    sut = Email(raw)

    assert sut.value == expected


def test_email_accepts_max_length() -> None:
    raw = "a@" + "x" * (Email.EMAIL_MAX_LENGTH - 6) + ".com"

    sut = Email(raw)

    assert len(sut.value) == Email.EMAIL_MAX_LENGTH


@pytest.mark.parametrize(
    "raw",
    [
        "",
        "   ",
        "user",
        "@example.com",
        "user@",
        "user@localhost",
        "user@name@example.com",
        "a@" + "x" * (Email.EMAIL_MAX_LENGTH - 5) + ".com",
    ],
)
def test_email_rejects_invalid_value(raw: str) -> None:
    with pytest.raises(ValueError, match="Invalid email"):
        Email(raw)


def test_hashed_password_hides_value_in_repr() -> None:
    sut = HashedPassword("secret-hash")

    assert "secret-hash" not in repr(sut)
