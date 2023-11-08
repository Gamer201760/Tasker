from PyQt5.QtWidgets import QDialog, QWidget

from ui.notify_dialog import Ui_Notify


class NotifyDialog(Ui_Notify, QDialog):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.label.setText(text)
