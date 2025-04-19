import sys
import os
import re
from pathlib import Path
import pandas as pd

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import Qt
from gui.layout_colorwidget import Color
import core.global_var as globalvar
from core.log_format_parser import LogFormatParser

class ParseMyLogPandasTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class ParseMyLogTableView(QTableView):
    def __init__(self):
        super().__init__()
        # log
        self.log = globalvar.get_val("LOGGER")

        # Table View
        self.setCornerButtonEnabled(False)
        self.setShowGrid(True)
        #self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setSortingEnabled(True)
        #self.setStyleSheet('QTableView {background-color: rgb(50,50,50); color: white;}')
        #_font = QtGui.QFont(["Courier New"],14)
        #self.setFont(_font)

        # Log format parser
        self.log_format_parser = LogFormatParser()
        self.log_parser_temp_dir = globalvar.get_val("LOG_PARSER_TEMP_DIR")

        self.model = ParseMyLogPandasTableModel(pd.DataFrame())

    def _clear_table(self):
        data = pd.DataFrame([])
        model = ParseMyLogPandasTableModel(data)
        self.setModel(model)

    def _drop_duplicates(self,df):
        if 'log' in df.columns:
            df = df.drop_duplicates(subset=['log'], keep='last')
        else:
            df = df.drop_duplicates()
        return df

    def _filter_log_level(self):
        loglevel = self.filter_loglevel.get()
        df = self.table.model.df
        if loglevel !='NONE' and 'log_level' in df.columns:
            df = df[df.log_level.str.upper().eq(loglevel)]
        self.table.model.df = df

    def _filter_regex(self):
        reg_pattern = self.regex_entry.get()
        print("regex is  ", reg_pattern)
        if len(reg_pattern) == 0:
            return
        df = self.table.model.df
        # user may give invalid regex
        try:
            if 'log' in df.columns:
                df = df[df.log.str.contains(
                    pat=reg_pattern, regex=True, flags=re.IGNORECASE, na=False)]
        except:
            pass
        self.table.model.df = df

    def _get_csv_file_path(self, file_path):
        file_name = os.path.basename(file_path)
        folder_name = os.path.dirname(file_path)
        csv_filename = file_name + '.csv'
        parsed_logs_folder = os.path.join(
            folder_name, self.log_parser_temp_dir)
        csv_file_path = os.path.join(parsed_logs_folder,csv_filename)
        return csv_file_path

    def _apply_filter_updates(self, csv_file_path):
        self._filter_log_level()
        self.drop_duplicates()
        self._filter_regex()
    
    def _table_redraw(self, data):
        model = ParseMyLogPandasTableModel(data)
        self.setModel(model)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    
    def _import_csv(self, filename):
        self.log.debug(f"Importing CSV file: {filename}")
        try:
            df = pd.read_csv(filename, sep=',', encoding='unicode_escape', header=0, index_col=0)
            return df
        except Exception as e:
            self.log.error(f"Error importing CSV file: {e}")
            return pd.DataFrame()

    def _update_table(self,file_path):
        self._clear_table()
        csv_file_path = self._get_csv_file_path(file_path)
        self.log.debug(f"CSV file path: {csv_file_path}")
        # Check if the CSV file already exists
        # If it doesn't exist, parse the logs and create the CSV file
        if not os.path.exists(csv_file_path):
            self.log_format_parser.set_path(file_path)
            self.log_format_parser.ParseLogs()

        # If it exists, import the CSV file
        if os.path.exists(csv_file_path):
            df = self._import_csv(csv_file_path)
            self._table_redraw(df)
        