from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout


class Ui_Notify(object):
    def setupUi(self, Notify):
        Notify.setGeometry(300, 300, 500, 50)
        Notify.setWindowTitle('Notify')

        self.v_layout = QVBoxLayout(Notify)

        self.label = QLabel(Notify)
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(30)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_btn = QPushButton('Ok', Notify)
        self.close_btn.clicked.connect(Notify.reject)

        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        Notify.setLayout(self.v_layout)