# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import sys
import os
from p2c import settings
from p2c.app import P2CDaemon
from gui.qml.app import P2CQMLApplication


try:
    os.makedirs(settings.LOG_DIR)
except OSError:
    pass

logging.basicConfig(
    filename = os.path.join(settings.LOG_DIR, datetime.now().strftime('p2c_%H:%M:%S_%d-%m-%Y.log')),
    level = logging.DEBUG
)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('p2c.info_clients').setLevel(logging.WARNING)

def main():
    # Create the application instance.
    app = P2CQMLApplication(sys.argv)
    app.run_view()
    logic = P2CDaemon()
    app.connect_daemon(logic)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()