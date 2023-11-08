import sys
from datetime import date, datetime, timedelta

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow

import ui.img_qr  # noqa: F401
from core.exceptions import TaskerException
from core.navigator import Pages, page
from model.task import Task
from model.user import User
from page.login import LoginDialog
from page.notify import NotifyDialog
from page.register import RegisterDialog
from page.task_dialog import NewTaskDialog
from ui.main_ui import Ui_MainWindow


class Tasker(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Tasker')
        self.pages = Pages({
            'login': (0, self.login_page),
            'main': (1, self.main_page),
            'calendar': (2, None),
            'settings': (3, None)
        })

        self.user: User | None = None
        self.date = datetime.now().date()
        self.last_page: page = self.pages['login']

        # Nav bar
        self.new_task_btn.clicked.connect(self.new_task)
        self.back_btn.clicked.connect(self.back)
        self.calendar_btn.clicked.connect(lambda: self.navigate(self.pages['calendar']))
        self.user_btn.clicked.connect(lambda: self.navigate(self.pages['login']))
        self.settings_btn.clicked.connect(lambda: self.navigate(self.pages['settings']))

        # Login page
        self.user_list.clicked.connect(self.select_user)
        self.register_btn.clicked.connect(self.register)

        # Calendar page
        self.calendar_widget.selectionChanged.connect(self.select_date)
        self.sync_btn.clicked.connect(self.sync)

        # Settings page
        self.delete_btn.clicked.connect(self.delete_user)

        # Main page
        self.archive_btn.clicked.connect(self.load_archive)

        self.navigate(self.pages['login'])

    # Init pages
    def main_page(self):
        """setup main page"""
        self.load_tasks()
        self.navigate_bar.setVisible(True)

    def login_page(self):
        """setup login page"""
        self.navigate_bar.setVisible(False)
        self.load_user()

    # Connect btns from bar
    def register(self):
        """show register dialog"""
        RegisterDialog().exec_()
        self.navigate(self.pages['login'])

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

    def new_task(self):
        """add new task"""
        if self.user:
            NewTaskDialog(user_id=self.user.id).exec_()
            self.navigate(self.pages['main'])

    # Connect btn from settings
    def delete_user(self):
        """delete user from db"""
        if self.user:
            self.user.delete()
            self.navigate(self.pages['login'])

    # Selectable
    def select_date(self):
        """select date for display tasks"""
        self.set_date(self.sender().selectedDate().toPyDate()) # type: ignore
        self.navigate(self.pages['main'])

    def select_user(self, payload: QtCore.QModelIndex):
        """select user"""
        self.user: User | None = payload.data(999)
        if self.user and self.user.ejuser and self.user.ejuser.is_active() is False:
            LoginDialog(user=self.user).exec_()
        self.navigate(self.pages['main'])

    # Load from db
    def load_user(self):
        self.user_list.clear()
        self.show_user(users=User.get_all())

    def load_tasks(self):
        if self.user:
            self.task_list.clear()
            self.date_label.setText(self.date.strftime('%d-%m-%Y'))
            self.show_task(Task.gettask_by_deadline(user=self.user, deadline=self.date))
            self.show_homework(user=self.user)

    def load_archive(self):
        self.last_page = self.pages['main']
        if self.user:
            self.task_list.clear()
            self.date_label.setText('Архив')
            self.show_task(Task.getarchivedtasks(user=self.user))

    # Show data
    def show_task(self, tasks: list):
        for task in tasks:
            task = Task.get_task_from_raw(*task)
            taskw = QListWidgetItem(self.task_list)
            taskw.setData(999, task)
            taskw.setText(f'{task.text} {task.deadline.strftime("%d-%m-%Y")}')
            taskw.setCheckState(QtCore.Qt.CheckState.Checked if task.state else QtCore.Qt.CheckState.Unchecked)

    def show_homework(self, user: User):
        if user.ejuser:
            homeworks = user.ejuser.homework(date=self.date + timedelta(days=1))
            for homework in homeworks:
                hwid = QListWidgetItem(self.task_list)
                hwid.setText(f'{homework.name}: {homework.homework}')
                hwid.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def show_user(self, users: list[tuple]):
        for user in users:
            user = User.get_user_from_raw(*user)
            userwid = QListWidgetItem(self.user_list)
            userwid.setText(user.username)
            userwid.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            userwid.setData(999, user)

    # Other functions
    def navigate(self, to: page, *args, **kwargs):
        if to[1]:
            to[1](*args, **kwargs)
        if self.stackedWidget.currentIndex() != to[0]:
            self.last_page = tuple(self.pages.values())[self.stackedWidget.currentIndex()] # type: ignore
            self.stackedWidget.setCurrentIndex(to[0])

    def set_date(self, date: date):
        self.date = date


# Catch exceptions
def except_hook(cls, exception, traceback):
    if TaskerException in cls.__bases__:
        error = NotifyDialog(text=str(exception))
        error.setWindowTitle(cls.__name__)
        error.exec_()
        return
    sys.__excepthook__(cls, exception, traceback)
    exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tasker()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
