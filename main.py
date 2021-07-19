#!/usr/bin/python3

import os
import sys

from HoneyUI import HoneyUI
from HoneyClass import HoneyManager
from PySide2 import QtWidgets

if __name__ == "__main__":
    path = ''

    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.getcwd()

    app = QtWidgets.QApplication(['main.py', '--no-sandbox'])
    window = QtWidgets.QMainWindow()
    main_ui = HoneyUI()
    main_ui.setupUi(window)
    manager = HoneyManager(main_ui, path)
    main_ui.link_on_clicks(manager.loc_on_click, manager.pass_on_click, manager.api_on_click)
    main_ui.link_map_html('file:' + path + '/map.html')
    manager.start()
    window.show()
    launch = app.exec_()
    manager.save_data()
    sys.exit(launch)
