from PyQt5.QtWidgets import QDialog

from model.ejournal import EJUser
from model.user import User
from page.notify import NotifyDialog
from ui.login_dialog import Ui_Login


class LoginDialog(Ui_Login, QDialog):
    def __init__(self, user: User) -> None:
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.setWindowTitle('Login')
        self.register_btn.clicked.connect(self.create)

    def create(self):
        if self.username_ej.text().strip() == '' or self.password_ej.text().strip() == '':
            NotifyDialog('Имя пользователя и пароль не должны быть пустыми').exec_()
            return

        ejuser = EJUser(username=self.username_ej.text())
        ejuser.login_ej(self.password_ej.text())

        self.user.ejuser = ejuser
        self.user.update()
        self.reject()
