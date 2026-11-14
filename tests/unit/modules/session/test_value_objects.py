import hashlib

from raydahub.modules.session.value_objects import SessionToken


def test_session_token_hash_is_sha256_hex() -> None:
    sut = SessionToken("token").hash()

    assert sut.value == hashlib.sha256(b"token").hexdigest()


def test_session_token_hides_value_in_repr() -> None:
    sut = SessionToken("secret-token")

    assert "secret-token" not in repr(sut)
