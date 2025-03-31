#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path
import sys

from PyQt6.QtWidgets import QApplication
from gui.app import MainWindow

import core.global_var as globalvar

VERSION='v0.0.1'
globalvar.init_global_var()
globalvar.set_val("APP_NAME", "ParseMyLog")
globalvar.set_val("APP_PATH", path.dirname(__file__))
globalvar.set_val("APP_VERSION", VERSION)

import logging
import logging.config
import yaml

LOGGING_CONFIG_FILE = \
    path.join(path.dirname(__file__),"configs", r'logging_conf.yaml')

# logging
with open(LOGGING_CONFIG_FILE, 'r') as f:
    log_cfg = yaml.safe_load(f.read())

logging.config.dictConfig(log_cfg)
logger = logging.getLogger('Dev')

# Temp location to store the parsed CSV files
LOG_PARSER_TEMP_DIR = '.parsemylog'

globalvar.set_val("LOGGER", logger)
globalvar.set_val("LOG_PARSER_TEMP_DIR", LOG_PARSER_TEMP_DIR)

class ParseMyLog():
    def __init__(self) -> None:
        app = QApplication(sys.argv)
        app.setApplicationName("ParseMyLog")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    ParseMyLog()
