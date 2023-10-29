from PyQt5.QtWidgets import QDialog

from model.ejournal import EJUser
from model.user import User
from page.notify import NotidyDialog
from ui.register_dialog import Ui_register_dialog


class RegisterDialog(Ui_register_dialog, QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.register_btn.clicked.connect(self.create)

    def create(self):
        if self.username.text().strip() == '':
            NotidyDialog('Имя пользователя не должно быть пустым').exec_()
            return
        ejuser = None
        if self.username_ej.text().strip() != '' and self.password_ej.text().strip() != '':
            ejuser = EJUser(username=self.username_ej.text())
            ejuser.login_ej(self.password_ej.text())

        user = User(username=self.username.text(), ejuser=ejuser)
        user.create()
        self.reject()
