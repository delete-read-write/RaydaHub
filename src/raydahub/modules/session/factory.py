import secrets
import uuid

from raydahub.modules.session.types_ import SessionId
from raydahub.modules.session.value_objects import SessionToken


def make_session_id() -> SessionId:
    return SessionId(uuid.uuid7())


def make_session_token() -> SessionToken:
    return SessionToken(secrets.token_urlsafe(32))
