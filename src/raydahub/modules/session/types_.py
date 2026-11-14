import uuid
from typing import NewType

SessionId = NewType("SessionId", uuid.UUID)
