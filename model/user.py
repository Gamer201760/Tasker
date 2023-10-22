import uuid
from uuid import UUID

from pydantic import BaseModel, Field, model_serializer

from core.db import getCon, getCur
from model.ejournal import EJUser
from model.token import JWToken


class User(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    username: str
    ejuser: EJUser | None = None

    def create(self):
        getCur().execute(
            """
            insert into User(id,username,token,ejusername)
            values (:id,:username,:token,:ejusername);
            """,
            self.model_dump()
        )
        getCon().commit()

    @classmethod
    def _generate_user(cls, id: UUID, username: str, token: str | None, ejname: str | None):
        ejuser = None
        if token and ejname:
            ejuser = EJUser(token=JWToken(token=token), username=ejname)
        return cls(id=id, username=username, ejuser=ejuser)

    @classmethod
    def get_all(cls) -> list:
        getCur().execute("""select * from User;""")
        return list(map(lambda x: cls._generate_user(*x), getCur().fetchall()))

    @model_serializer
    def ser_model(self) -> dict:
        return {
            'id': str(self.id),
            'username': self.username,
            'token': str(self.ejuser.token) if self.ejuser else None,
            'ejusername': self.ejuser.username if self.ejuser else None,
        }
