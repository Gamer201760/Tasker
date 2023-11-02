import uuid
from uuid import UUID

from pydantic import BaseModel, Field, model_serializer

from core.db import getCon, getCur
from model.ejournal import EJUser


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

    def update(self):
        getCur().execute(
            """
            update User
            set username=:username,
            token=:token,
            ejusername=:ejusername
            where id=:id;
            """,
            self.model_dump()
        )
        getCon().commit()

    def delete(self):
        getCur().execute(
            """
            delete from User
            where id=:id;
            """,
            self.model_dump()
        )
        getCon().commit()

    @staticmethod
    def get_user_from_raw(id: UUID, username: str, token: str | None, ejname: str | None):
        ejuser = None
        if token and ejname:
            ejuser = EJUser(token=token, username=ejname)
        return User(id=id, username=username, ejuser=ejuser)

    @classmethod
    def get_all(cls) -> list[tuple]:
        getCur().execute("""select * from User;""")
        return getCur().fetchall()

    @model_serializer
    def ser_model(self) -> dict:
        return {
            'id': str(self.id),
            'username': self.username,
            'token': str(self.ejuser.token) if self.ejuser else None,
            'ejusername': self.ejuser.username if self.ejuser else None,
        }
