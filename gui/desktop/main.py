# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import QApplication
from p2c.app import Application
from gui.desktop.mainwindow import MainWindow


logging.basicConfig(level=logging.DEBUG)

def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.setupUi(ui)
    logic = Application()
    ui.connect_app(logic)
#    ui.play()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()