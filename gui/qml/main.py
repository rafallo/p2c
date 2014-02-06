# -*- coding: utf-8 -*-
import sys

from p2c.app import P2CDaemon
from gui.qml.app import P2CQMLApplication


def main():
    # Create the application instance.
    app = P2CQMLApplication(sys.argv)
    app.run_view()
    logic = P2CDaemon()
    app.connect_daemon(logic)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()