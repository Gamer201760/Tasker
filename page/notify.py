from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget


class NotifyDialog(QDialog):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi()
        self.setWindowTitle('Notify')
        self.label.setText(text)

    def setupUi(self):
        self.setGeometry(300, 300, 500, 50)
        self.v_layout = QVBoxLayout()

        self.label = QLabel(self)
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(30)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_btn = QPushButton('Ok', self)
        self.close_btn.clicked.connect(self.reject)

        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.v_layout)

