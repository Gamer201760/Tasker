

from uuid import UUID

from PyQt5.QtWidgets import QDialog

from model.task import Task
from ui.task_dialog import Ui_Task


class NewTaskDialog(Ui_Task, QDialog):
    def __init__(self, user_id: UUID) -> None:
        super().__init__()
        self.user_id = user_id
        self.setupUi(self)
        self.create_btn.clicked.connect(self.create)

    def create(self):
        task = Task(
            text=self.task.text(),
            deadline=self.deadline.selectedDate().toPyDate(),
            user_id=self.user_id
        )
        task.create()
        self.reject()
