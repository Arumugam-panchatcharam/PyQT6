#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import re
import csv
import os
from pathlib import Path
import shutil

from importlib import resources

import pandas as pd

import core.global_var as globalvar

class LogFormatParser():
    def __init__(self, inpath=None) -> None:
        self.inpath = inpath
        self.foldername = None
        self.filename = None
        self.error = None
        self.log_format = None
        self.parsed_logs_folder = None
        self.log_parser_temp_dir = globalvar.get_val("LOG_PARSER_TEMP_DIR")
        self.log = globalvar.get_val("LOGGER")

    def set_path(self,inpath):
        self.inpath = inpath

        if not os.path.exists(inpath):
            self._error("Input path not Exists")
            return
        if os.path.isdir(inpath):
            self.foldername = inpath
        if os.path.isfile(inpath):
            self.foldername, self.filename = os.path.split(
                os.path.realpath(inpath))
            self.log.debug("folder {0} file {1}".format(self.foldername, self.filename))

        self.parsed_logs_folder = os.path.join(
            self.foldername, self.log_parser_temp_dir)
        
        globalvar.set_val("PARSED_LOGS_FOLDER", self.parsed_logs_folder)

        if not os.path.exists(self.parsed_logs_folder):
            os.mkdir(self.parsed_logs_folder)
        
    def _error(self, error_str):
        self.error = error_str
        self.log.error(self.error)

    def _search(self, log_file, logInfo):
        self.log.debug('Log Name {0}'.format(log_file))
        self.log.debug('Log REGEX {0}'.format(logInfo.get('regex')))

        log_file_path = os.path.join(self.foldername, log_file)
        self.log.debug('Log file path {0}'.format(log_file_path))
        if not log_file_path:
            self.log.debug('Log file not found')
            return
        
        # Check if file is empty
        if os.path.getsize(log_file_path) == 0:
            self.log.debug('Log file is empty')
            return
        
        # Check if file is already parsed
        csv_filename = os.path.join(self.parsed_logs_folder, log_file + '.csv')
        self.log.debug('CSV file {0}'.format(csv_filename))
        if os.path.exists(csv_filename):
            self.log.debug('Log file already parsed')
            return

        # unformatted log file
        if logInfo.get('regex').lower() == 'unformatted':
            try:
                df = pd.read_csv(log_file_path, delimiter="\n",
                                    skip_blank_lines=True, skipinitialspace=True,
                                    names=['log', ], encoding='utf-8',
                                    lineterminator='\n')
                df.to_csv(csv_filename, encoding='utf-8', index=True)
            except:
                pass
            return
        # regex
        try:
            log_regex = re.compile(logInfo.get('regex'))
        except:
            self.log.debug('Log Regex Error')
            return
        
        csv_fields = list(dict(log_regex.groupindex).keys())
        # Remove Null at the start of File
        with open(log_file_path, 'r+') as file:
            data = file.read().lstrip('\x00')
            file.seek(0)
            file.write(data)
            file.truncate()

        # write parsed data to CSV
        with open(csv_filename, 'w', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
            csv_writer.writeheader()

            with open(log_file_path, 'r') as file:
                for line in file:
                    match = log_regex.search(line)
                    if match is not None:
                        csv_writer.writerow(match.groupdict())

        try:
            df = pd.read_csv(csv_filename, delimiter=",",
                                skip_blank_lines=True, skipinitialspace=True,
                                encoding='utf-8',lineterminator='\n')
            df.to_csv(csv_filename, encoding='utf-8', index=True)
        except:
            pass
        
        self.log.debug('{0} parsed successfully'.format(log_file))

    def ParseLogs(self):
        if not self.foldername:
            return
        self.log.debug(' Parse Logs')

        # Check if Log config file exists
        if not resources.is_resource("configs", "config.yaml"):
            self._error("Log config file not found")
            return

        # Load yaml file
        with resources.open_text("configs", "config.yaml") as lcf:
            try:
                self.log_format = yaml.safe_load(lcf.read())
            except:
                self._error("Log config YAML load error")

        if self.filename:
            for logname in self.log_format.get('logfiles'):
                log_info = self.log_format.get('logfiles')[logname]
                log_filename = log_info.get('filename')
                if log_filename.lower() in self.filename.lower():
                    self._search(self.filename, log_info)
                    break

if __name__ == '__main__':
    pass