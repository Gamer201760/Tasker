from jwt import decode, ExpiredSignatureError
from pydantic import BaseModel, field_validator


class JWToken(BaseModel):
    token: str
    active: bool = True

    def __str__(self) -> str:
        return self.token

    @field_validator('token')
    @classmethod
    def validator_token(cls, token: str) -> str:
        try:
            decode(token, algorithms=['HS256'], options = {
                'verify_signature': False,
                'verify_exp': True
            })
        except ExpiredSignatureError:
            cls.active = False

        return token
