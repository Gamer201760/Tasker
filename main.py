import sys
from datetime import date, datetime, timedelta

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow

from core.exceptions import TaskerException
from core.navigator import Pages, page
from model.task import Task
from model.user import User
from page.login import LoginDialog
from page.notify import NotifyDialog
from page.register import RegisterDialog
from page.task_dialog import NewTaskDialog


class Tasker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self.setWindowTitle('Tasker')
        self.pages = Pages({
            'login': (0, self.login_page),
            'main': (1, self.main_page),
            'calendar': (2, None),
            'settings': (3, None)
        })
        self.user: User | None = None
        self.last_page: page = self.pages['login']

        # Nav bar
        self.new_task_btn.clicked.connect(self.new_task)
        self.back_btn.clicked.connect(self.back)
        self.calendar_btn.clicked.connect(lambda: self.navigate(self.pages['calendar']))
        self.user_btn.clicked.connect(lambda: self.navigate(self.pages['login']))
        self.settings_btn.clicked.connect(lambda: self.navigate(self.pages['settings']))

        # Login page
        self.user_list.clicked.connect(self.user_select)
        self.register_btn.clicked.connect(self.register)

        # Calendar page
        self.calendar_widget.selectionChanged.connect(self.select_date)
        self.sync_btn.clicked.connect(self.sync)

        # Settings page
        self.delete_btn.clicked.connect(self.delete_user)

        self.navigate(self.pages['login'])

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

    def back(self):
        """return to back page"""
        self.navigate(self.last_page)

    def register(self):
        RegisterDialog().exec_()
        self.navigate(self.pages['login'])

    def select_date(self):
        self.navigate(self.pages['main'], date=self.sender().selectedDate().toPyDate()) # type: ignore

    def new_task(self):
        if self.user:
            NewTaskDialog(user_id=self.user.id).exec_()

    def delete_user(self):
        if self.user:
            self.user.delete()
            self.navigate(self.pages['login'])

    def user_select(self, payload: QtCore.QModelIndex):
        self.user: User | None = payload.data(999)
        if self.user and self.user.ejuser and self.user.ejuser.is_active() is False:
            LoginDialog(user=self.user).exec_()
        self.navigate(self.pages['main'])

    def load_homework(self, date: date):
        self.task_list.clear()
        self.date_label.setText(date.strftime('%d-%m-%Y'))
        if self.user:
            tasks = Task.gettask_by_deadline(user=self.user, deadline=date)
            for task in tasks:
                taskw = QListWidgetItem(self.task_list)
                taskw.setData(999, task)
                taskw.setText(f'{task.text} {task.deadline.strftime("%d-%m-%Y")}')
                taskw.setCheckState(QtCore.Qt.CheckState.Checked if task.state else QtCore.Qt.CheckState.Unchecked)
            if self.user.ejuser:
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
        if self.stackedWidget.currentIndex() != to[0]:
            self.last_page = tuple(self.pages.values())[self.stackedWidget.currentIndex()] # type: ignore
            self.stackedWidget.setCurrentIndex(to[0])

    def iterAllItems(self):
        for i in range(self.task_list.count()):
            yield self.task_list.item(i)


def except_hook(cls, exception, traceback):
    if TaskerException in cls.__bases__:
        error = NotifyDialog(text=str(exception))
        error.setWindowTitle(cls.__name__)
        error.exec_()
        return
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tasker()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
