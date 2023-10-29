import uuid
from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from core.db import getCon, getCur
from model.user import User


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    text: str
    user_id: UUID
    deadline: date
    state: bool = False

    def create(self):
        getCur().execute(
            """
            insert into Task(id,text,user_id,deadline,state)
            values (:id,:text,:user_id,:deadline,:state);
            """,
            self.model_dump()
        )
        getCon().commit()

    @staticmethod
    def update(payload: list[dict]):
        getCur().executemany(
            """
            update Task
            set state=:state,
            text=:text,
            deadline=:deadline
            where id=:id;
            """,
            payload
        )
        getCon().commit()

    @classmethod
    def _generate_task(cls, id: UUID, text: str, user_id: UUID, deadline: date, state: bool):
        return cls(id=id, text=text, user_id=user_id, deadline=deadline, state=state)

    @classmethod
    def gettask_by_deadline(cls, user: User, deadline: date) -> list:
        getCur().execute(
            """
            select * from Task
            where user_id=:user AND deadline >= :deadline
            ORDER BY state,deadline;
            """,
            {
                'user': str(user.id),
                'deadline': deadline
            }
        )
        return list(map(lambda x: cls._generate_task(*x), getCur().fetchall()))

    @field_serializer('user_id')
    def serialize_user(self, user_id: UUID):
        return str(user_id)

    @field_serializer('id')
    def serialize_id(self, id: UUID):
        return str(id)
