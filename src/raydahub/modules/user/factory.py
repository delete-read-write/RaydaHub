import uuid

from raydahub.modules.user.types_ import UserId


def make_user_id() -> UserId:
    return UserId(uuid.uuid7())
