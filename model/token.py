
from datetime import datetime

from jwt import decode
from pydantic import BaseModel, field_validator

from core.exceptions import UnAuthorized


class JWToken(BaseModel):
    token: str
    active: bool = True

    def __str__(self) -> str:
        return self.token

    @field_validator('token')
    @classmethod
    def validator_token(cls, token: str) -> str:
        t = decode(token, algorithms=['HS256'], options = {
            'verify_signature': False,
        })
        exp = t.get('exp')
        if exp and exp < datetime.now().timestamp():
            cls.active = False
            raise UnAuthorized()

        return token
