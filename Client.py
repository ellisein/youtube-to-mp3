import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Application(QMainWindow):
    TITLE = ""

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.startFlow()

    def initWindow(self):
        self.setWindowTitle(self.TITLE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
