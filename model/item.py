
from datetime import date

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    homework: str
    ended: bool = False
    date_lesson: date

    def is_end(self) -> bool:
        return self.ended

    def __str__(self) -> str:
        return self.homework

    def __repr__(self) -> str:
        return f'Item({self.name})'

    def __eq__(self, other):
        if str(other) == str(self):
            return True
        return False
