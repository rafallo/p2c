# -*- coding: utf-8 -*-
import sys

import time
from gui.qml.classes import Tile
from p2c.app import Application
from gui.qml.binding import QMLBinding


def main():
    # Create the application instance.
    app = QMLBinding(sys.argv)
    app.run_view()



    logic = Application()
    app.connect_app(logic)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()