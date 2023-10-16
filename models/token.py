
from jwt import decode, exceptions
from pydantic import BaseModel, field_serializer


class JWToken(BaseModel):
    token: str
    active: bool = True

    def __str__(self) -> str:
        return self.token

    @field_serializer('token')
    def serilizer_token(self, token: str) -> str:
        try:
            decode(token, algorithms=['HS256'], options = {
                'verify_signature': False,
                'verify_exp': True
            })
        except exceptions.ExpiredSignatureError:
            self.active = False
        return token
