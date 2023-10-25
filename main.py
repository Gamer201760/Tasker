import sys
from datetime import datetime, timedelta

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow

from core.navigator import Pages, page
from model.user import User
from pages.register import RegisterDialog


class Tasker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self.pages = Pages({
            'login': (0, self.load_user),
            'main': (1, self.load_homework),
            'calendar': (2, None)
        })

        self.user_list.clicked.connect(self.user_select)
        self.register_btn.clicked.connect(self.register)
        self.calendar_btn.clicked.connect(lambda: self.navigate(self.pages['calendar']))

        self.user: User
        self.navigate(self.pages['login'])

    def register(self):
        RegisterDialog().exec_()
        self.navigate(self.pages['login'])

    def user_select(self, payload: QtCore.QModelIndex):
        self.user: User = payload.data(999)
        if self.user.ejuser and self.user.ejuser.is_active() is False:
            """Inactive"""
            print('inactive')
        self.navigate(self.pages['main'])

    def load_homework(self):
        self.task_list.clear()
        if self.user and self.user.ejuser:
            homeworks = self.user.ejuser.homework(date=datetime.now().date() + timedelta(days=1))
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

    def navigate(self, to: page):
        if to[1]:
            to[1]()
        self.stackedWidget.setCurrentIndex(to[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tasker()
    ex.show()
    sys.exit(app.exec_())
