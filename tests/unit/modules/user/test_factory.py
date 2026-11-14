from raydahub.modules.user.factory import make_user_id


def test_make_user_id_returns_uuid7() -> None:
    sut = make_user_id()

    assert sut.version == 7


def test_make_user_id_returns_unique_ids() -> None:
    assert make_user_id() != make_user_id()
