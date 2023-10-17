import sys
from datetime import datetime, timedelta

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow

from models.user import User


class Tasker(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('./ui/main.ui', self)
        self.user_list.clicked.connect(self.user_select)

        self.user: User
        self.navigate_login()

        self.stackedWidget.setCurrentIndex(0)

    def user_select(self, payload: QtCore.QModelIndex):
        self.user = payload.data(999)
        self.stackedWidget.setCurrentIndex(1)
        self.navigate_main()

    def navigate_main(self):
        self.listWidget.clear()
        homeworks = self.user.ejuser.homework(date=datetime.now().date() + timedelta(days=1)) if self.user.ejuser else None
        if homeworks:
            for homework in homeworks:
                hwid = QListWidgetItem(self.listWidget)
                hwid.setText(f'{homework.name}: {homework.homework}')
                hwid.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def navigate_login(self):
        self.user_list.clear()
        for user in User.get_all():
            userwid = QListWidgetItem(self.user_list)
            userwid.setText(user.username)
            # user.ejuser.is_active() if user.ejuser else False
            userwid.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            userwid.setData(999, user)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tasker()
    ex.show()
    sys.exit(app.exec_())
