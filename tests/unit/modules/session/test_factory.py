from raydahub.modules.session.factory import make_session_id, make_session_token


def test_make_session_id_returns_uuid7() -> None:
    sut = make_session_id()

    assert sut.version == 7


def test_make_session_token_has_256_bits_of_entropy() -> None:
    sut = make_session_token()

    assert len(sut.value) == 43
