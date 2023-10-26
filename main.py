import sys
from datetime import date, datetime, timedelta

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow

from core.navigator import Pages, page
from model.task import Task
from model.user import User
from pages.register import RegisterDialog
from pages.task_dialog import NewTaskDialog


class Tasker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self.pages = Pages({
            'login': (0, self.login_page),
            'main': (1, self.main_page),
            'calendar': (2, self.calendar_page)
        })

        self.user_list.clicked.connect(self.user_select)
        self.register_btn.clicked.connect(self.register)

        self.new_task_btn.clicked.connect(self.new_task)
        self.calendar_btn.clicked.connect(lambda: self.navigate(self.pages['calendar']))
        self.user_btn.clicked.connect(lambda: self.navigate(self.pages['login']))

        self.calendar_widget.selectionChanged.connect(self.select_date)
        self.sync_btn.clicked.connect(self.sync)

        self.user: User | None = None
        self.navigate(self.pages['login'])

    def calendar_page(self):
        """setup calendar page"""
        ...

    def main_page(self, date: date = datetime.now().date()):
        """setup main page"""
        self.navigate_bar.setVisible(True)
        self.load_homework(date=date)

    def login_page(self):
        """setup login page"""
        self.navigate_bar.setVisible(False)
        self.load_user()

    def sync(self):
        """synchronizes all tasks"""
        tasks = []
        for item in self.iterAllItems():
            if item.data(999):
                task: Task = item.data(999)
                task.state = True if item.checkState() == QtCore.Qt.CheckState.Checked else False
                tasks.append(task.model_dump())
        Task.update(payload=tasks)

    def select_date(self):
        self.navigate(self.pages['main'], date=self.sender().selectedDate().toPyDate())

    def new_task(self):
        if self.user:
            NewTaskDialog(user_id=self.user.id).exec_()

    def register(self):
        RegisterDialog().exec_()
        self.navigate(self.pages['login'])

    def user_select(self, payload: QtCore.QModelIndex):
        self.user: User | None = payload.data(999)
        if self.user and self.user.ejuser and self.user.ejuser.is_active() is False:
            """Inactive"""
            print('inactive')
        self.navigate(self.pages['main'])

    def load_homework(self, date: date):
        self.task_list.clear()
        self.date_label.setText(date.strftime('%d-%m-%Y'))
        if self.user and self.user.ejuser:
            tasks = Task.gettask_by_deadline(user=self.user, deadline=date)
            for task in tasks:
                taskw = QListWidgetItem(self.task_list)
                taskw.setData(999, task)
                taskw.setText(f'{task.text} {task.deadline.strftime("%d-%m-%Y")}')
                taskw.setCheckState(QtCore.Qt.CheckState.Checked if task.state else QtCore.Qt.CheckState.Unchecked)

            homeworks = self.user.ejuser.homework(date=date + timedelta(days=1))
            for homework in homeworks:
                hwid = QListWidgetItem(self.task_list)
                hwid.setText(f'{homework.name}: {homework.homework}')
                hwid.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def load_user(self):
        self.user_list.clear()
        for user in User.get_all():
            userwid = QListWidgetItem(self.user_list)
            userwid.setText(user.username)
            userwid.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            userwid.setData(999, user)

    def navigate(self, to: page, *args, **kwargs):
        if to[1]:
            to[1](*args, **kwargs)
        self.stackedWidget.setCurrentIndex(to[0])

    def iterAllItems(self):
        for i in range(self.task_list.count()):
            yield self.task_list.item(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tasker()
    ex.show()
    sys.exit(app.exec_())
