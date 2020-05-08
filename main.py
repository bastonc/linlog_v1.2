#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import parse
import re
import os
import datetime
import telnetlib
import internetworker
import time
import tci
import std
import settings
import subprocess
import ext
import json
import requests
from os.path import expanduser
from bs4 import BeautifulSoup

# import pyautogui

# import xdo  # $ pip install  python-libxdo
from PyQt5.QtWidgets import QApplication, QMessageBox, QAction, QWidget, QMainWindow, QTableView, QTableWidget, QTableWidgetItem, QTextEdit, \
    QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QFont, QBrush, QPixmap, QColor, QStandardItemModel
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from time import gmtime, strftime, localtime


# from tel import telnet_cluster
class Settings_file:

    def update_file_to_disk(self):
        filename = 'settings.cfg'
        with open(filename, 'r') as f:
            old_data = f.readlines()
        for index, line in enumerate(old_data):
            key_from_line = line.split('=')[0]
            # print ("key_from_line:",key_from_line)
            for key in self.settingsDict:

                if key_from_line == key:
                    # print("key",key , "line", line)
                    old_data[index] = key + "=" + self.settingsDict[key] + "\n"
        with open(filename, 'w') as f:
            f.writelines(old_data)
        print("Update_to_disk: ", old_data)
        return True

class Adi_file:

    def __init__(self):

        self.filename = 'log.adi'

        with open(self.filename, 'r') as file: #read all strings

            self.strings_in_file = file.readlines()

    def get_last_string(self):
        return len(self.strings_in_file)

    def rename_adi(self, old_name, new_name):
        os.rename(old_name, new_name)

    def store_changed_qso(self, object):
        '''
        1. Function recived object in format (ch.1)
        2. Building string for log.adi file
        3. Read all strings
        4. ReWrite string in log.adi file
        chapter 1
        :param object: {'BAND': '40M', 'CALL': 'UR4LGA', 'FREQ': 'Freq: 7028500', 'MODE': 'ESSB',
        'OPERATOR': 'UR4LGA', 'QSO_DATE': '20191109', 'TIME_ON': '224058', 'RST_RCVD': '59',
         'RST_SENT': '59', 'NAME': '', 'QTH': '', 'COMMENTS': '', 'TIME_OFF': '224058',
         'eQSL_QSL_RCVD': 'Y', 'EOR': 'R\n',
         'string_in_file': '186', 'records_number': '89'}

        :return:
        '''

        #print("hello  store_changed_qso method in Adi_file class\n", object)
        stringToAdiFile = "<BAND:" + str(len(object['BAND'])) + ">" + object['BAND'] + "<CALL:" + str(
            len(object['CALL'])) + ">"

        stringToAdiFile = stringToAdiFile + object['CALL'] + "<FREQ:" + str(len(object['FREQ'])) + ">" + \
                          object['FREQ']
        stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(object['MODE'])) + ">" + object[
            'MODE'] + "<OPERATOR:" + str(len(object['OPERATOR']))
        stringToAdiFile = stringToAdiFile + ">" + object['OPERATOR'] + "<QSO_DATE:" + str(
            len(object['QSO_DATE'])) + ">"
        stringToAdiFile = stringToAdiFile + object['QSO_DATE'] + "<TIME_ON:" + str(
            len(object['TIME_ON'])) + ">"
        stringToAdiFile = stringToAdiFile + object['TIME_ON'] + "<RST_RCVD:" + \
                          str(len(object['RST_RCVD'])) + ">" + object['RST_RCVD']
        stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(object['RST_SENT'])) + ">" + \
                          object['RST_SENT'] + "<NAME:" + str(len(object['NAME'])) + ">" + object['NAME'] + \
                          "<QTH:" + str(len(object['QTH'])) + ">" + object['QTH'] + "<COMMENTS:" + \
                          str(len(object['COMMENTS'])) + ">" + object['COMMENTS'] + "<TIME_OFF:" + \
                          str(len(object['TIME_OFF'])) + ">" + object['TIME_OFF'] + "<eQSL_QSL_RCVD:1>Y<EOR>\n"
        print("store_changed_qso: stringToAdiFile", stringToAdiFile)

        self.strings_in_file[int(object['string_in_file'])-1] = stringToAdiFile
        with open(self.filename, 'w') as file:
            #file.seek(0, 2)
            file.writelines(self.strings_in_file)


        #print("this:", self.strings_in_file[int(object['string_in_file'])-1])

    def get_header(self):

        '''
        This function returned string with cariage return
        :return: string header with cariage return
        '''

        self.header_string="ADIF from LinLog Light v."+APP_VERSION+" \n"
        self.header_string +="Copyright 2019-"+strftime("%Y", gmtime())+"  Baston V. Sergey\n"
        self.header_string +="Header generated on "+strftime("%d/%m/%y %H:%M:%S", gmtime())+" by "+settingsDict['my-call']+"\n"
        self.header_string +="File output restricted to QSOs by : All Operators - All Bands - All Modes \n"
        self.header_string +="<PROGRAMID:6>LinLog\n"
        self.header_string += "<PROGRAMVERSION:"+str(len(APP_VERSION))+">"+APP_VERSION+"\n"
        self.header_string += "<EOH>\n\n"
        return self.header_string

    def get_all_qso(self):
        try:
            with  open(self.filename, 'r') as file:
                lines = file.readlines()
                #print (lines)
        except Exception:
            print ("Adi_file: Exception. Don't open or read"+self.filename)

    def record_dict_qso (self, list_data):
        '''
        This function recieve List (list_data) with Dictionary with QSO-data
        Dictionary including:
        call
        name
        qth
        rst_send
        rst_reciev
        band
        mode
        comment
        :param list_data: List with Dictionary with QSO-data
        :return:
        '''
        index = len(list_data)
        with open ('log.adi', 'a') as file:
            for i in range(index):
               # print(i,list_data[i]['BAND'])
                stringToAdiFile = "<BAND:" + str(len(list_data[i]['BAND'])) + ">" + list_data[i]['BAND'] + "<CALL:" + str(
                    len(list_data[i]['CALL'])) + ">"

                stringToAdiFile = stringToAdiFile + list_data[i]['CALL'] + "<FREQ:" + str(len(list_data[i]['FREQ'])) + ">" + \
                                  list_data[i]['FREQ']
                stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(list_data[i]['MODE'])) + ">" + list_data[i][
                    'MODE'] + "<OPERATOR:" + str(len(list_data[i]['OPERATOR']))
                stringToAdiFile = stringToAdiFile + ">" + list_data[i]['OPERATOR'] + "<QSO_DATE:" + str(
                    len(list_data[i]['QSO_DATE'])) + ">"
                stringToAdiFile = stringToAdiFile + list_data[i]['QSO_DATE'] + "<TIME_ON:" + str(
                    len(list_data[i]['TIME_ON'])) + ">"
                stringToAdiFile = stringToAdiFile + list_data[i]['TIME_ON'] + "<RST_RCVD:" + \
                                  str(len(list_data[i]['RST_RCVD'])) + ">" + list_data[i]['RST_RCVD']
                stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(list_data[i]['RST_SENT'])) + ">" + \
                                  list_data[i]['RST_SENT'] + "<NAME:" + str(len(list_data[i]['NAME'])) + ">" + list_data[i]['NAME'] + \
                                  "<QTH:" + str(len(list_data[i]['QTH'])) + ">" + list_data[i]['QTH'] + "<COMMENTS:" + \
                                  str(len(list_data[i]['COMMENTS'])) + ">" + list_data[i]['COMMENTS'] + "<TIME_OFF:" + \
                                  str(len(list_data[i]['TIME_OFF'])) + ">" + list_data[i]['TIME_OFF'] + "<eQSL_QSL_RCVD:1>Y<EOR>\n"
                file.write(stringToAdiFile)



        #print(list_data[0]['call'])
        #header = self.get_header()
        #with open('aditest.adi', 'w') as file:
          #  file.writelines(header)
            #file.writelines(list_data)

    def create_adi(self, name):
        with open(name, 'w') as f:
            f.writelines(self.get_header())

class Filter(QObject):

    previous_call = ''



    def eventFilter(self, widget, event):


        if event.type() == QEvent.FocusOut:

                textCall = logForm.inputCall.text()
                foundList = self.searchInBase(textCall)

                logSearch.overlap(foundList)

                freq = logForm.get_freq()

                if textCall != '' and textCall != Filter.previous_call:
                    if settingsDict['search-internet-window'] == 'true':

                        Filter.previous_call = textCall
                        self.isearch = internetworker.internetWorker(window=internetSearch, callsign=textCall, settings=settingsDict)
                        self.isearch.start()
                        if settingsDict['tci'] == 'enable':
                            try:
                                tci.Tci_sender(settingsDict['tci-server']+":"+settingsDict['tci-port']).set_spot(textCall, freq)
                            except:
                                print("Filter: Can't connect to TCI-server")

                if textCall == '' or textCall == ' ':
                    pixmap = QPixmap('logo.png')




                return False

        if event.type() == QEvent.FocusIn:

                if logForm.inputCall.text() == '':
                    logForm.inputRstS.setText('59')
                    logForm.inputRstR.setText('59')

                    # return False so that the widget will also handle the event
                    # otherwise it won't focus out
                return False
        else:
                # we don't care about other events
                return False



    def searchInBase(self, call):
        #print ("search_in Base:_>", call)
        foundList = []  # create empty list for result list
        All_records = logWindow.get_all_record()
        lenRecords = len(All_records)  # get count all Records
        #print("Search InBase: lenRecords: _>", All_records)
        for counter in range(lenRecords):  # start cicle where chek all elements at equivivalent at input call
            if All_records[counter]['CALL'].strip() == call.strip():
                foundList.append(All_records[counter])

        #print("search_in Base:_>",foundList)
        return foundList
        # print (foundList)
        #

#####################

class Communicate(QObject):
    signalComplited = pyqtSignal(list)

class Fill_table(QThread):
    def __init__(self, all_column, window, all_record, communicate, parent=None):
        super().__init__()
        self.all_collumn = all_column
        self.window = window
        #self.all_record = all_record
        self.c = communicate


    def run(self):

        self.allRecord = parse.getAllRecord(self.all_collumn, "log.adi")
        #self.all_record = self.allRecord
        self.c = Communicate()
        self.c.signalComplited.connect(Reciev_allRecords)
        self.c.signalComplited.emit(self.allRecord)

        self.allRows = len(self.allRecord)
        #print(" self.allRecords:_> ",  self.allRecord)
        self.window.tableWidget.setRowCount(self.allRows)
        allCols = len(self.all_collumn)
        #self.window.tableWidget.setHorizontalHeaderLabels(
        #    ["No", "     Date     ", " Time ", "Band", "   Call   ", "Mode", "RST r",
         #    "RST s", "      Name      ", "      QTH      ", " Comments ", " Time off ", " eQSL Rcvd "])

        for row in range(self.allRows):
            #self.window.tableWidget.insertRow(row)
            #print("row -", row)
            for col in range(allCols):
                #print("col -", col, self.all_collumn[col])
                pole = self.all_collumn[col]
                # print(self.allRows, row, self.allRows - row )
                # print("Number record:", self.allRecord[row][pole])
                if self.allRecord[(self.allRows - 1) - row][pole] != ' ' or \
                        self.allRecord[(self.allRows - 1) - row][pole] != '':
                    #self.window.tableWidget.setItem(row, col,
                     #                               self.protectionItem(self.allRecord[(self.allRows - 1) - row][pole],
                      #                                                  Qt.ItemIsSelectable | Qt.ItemIsEnabled))
                    if col == 0:
                       self.window.tableWidget.setItem(row, col,
                                                 self.protectionItem(self.allRecord[(self.allRows - 1) - row][pole],
                                                                     Qt.ItemIsSelectable | Qt.ItemIsEnabled))

                        # QTableWidgetItem(self.allRecord[(self.allRows - 1) - row][pole]))
                    elif col == 1:
                        date = str(self.allRecord[(self.allRows - 1) - row][pole])
                        date_formated = date[:4] + "-" + date[4:6] + "-" + date[6:]
                        #print(time_formated)
                        self.window.tableWidget.setItem(row, col,
                                                        QTableWidgetItem(date_formated))

                    elif col == 2:
                        time = str(self.allRecord[(self.allRows - 1) - row][pole])
                        time_formated = time[:2] + ":" + time[2:4] + ":" + time[4:]
                        #print(time_formated)
                        self.window.tableWidget.setItem(row, col,
                                                        QTableWidgetItem(time_formated))


                    else:
                        self.window.tableWidget.setItem(row, col,
                                                 QTableWidgetItem(self.allRecord[(self.allRows - 1) - row][pole]))
        self.window.tableWidget.resizeColumnsToContents()
        self.window.tableWidget.resizeRowsToContents()

    def update_All_records(self, all_records_list):
        self.all_records_list = all_records_list
        All_records = self.all_records_list
        #print("update_All_records > All_records:_>", All_records)

    def protectionItem(self, text, flags):
        tableWidgetItem = QTableWidgetItem(text)
        tableWidgetItem.setFlags(flags)
        return tableWidgetItem

class Reciev_allRecords:
    def __init__(self, allRecords):
        self.allRecords = allRecords
        for i in range(len(self.allRecords)):
            All_records.append(self.allRecords[i])

        #print("Reciev_allRecords: _>", allRecords)
        #print("Reciev_allRecords: _>", All_records)

class log_Window(QWidget):

        def __init__(self):
            super().__init__()
            self.filename = "log.adi"
            if os.path.isfile(self.filename):
                pass
            else:
                with open(self.filename, "w") as file:
                    file.write(Adi_file().get_header())

            self.allCollumn = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT',
                               'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD']
            # self.allRecord = parse.getAllRecord(self.allCollumn, self.filename)

            self.initUI()


        def initUI(self):

                self.setGeometry(int(settingsDict['log-window-left']),
                                 int(settingsDict['log-window-top']),
                                 int(settingsDict['log-window-width']),
                                 int(settingsDict['log-window-height']))
                self.setWindowTitle('LinuxLog | All QSO')
                self.setWindowIcon(QIcon('logo.png'))
                self.setWindowOpacity(float(settingsDict['logWindow-opacity']))
                style = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
                    'color'] + ";"
                self.setStyleSheet(style)

                # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
                #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
                #		   )
                self.tableWidget = QTableWidget()
                self.tableWidget.move(0, 0)
                self.tableWidget.verticalHeader().hide()
                style_table = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
                    'color-table'] + "; font: 12px; "
                self.tableWidget.setStyleSheet(style_table)
                fnt = self.tableWidget.font()
                fnt.setPointSize(8)
                self.tableWidget.setSortingEnabled(True)
                self.tableWidget.setFont(fnt)
                self.tableWidget.setColumnCount(13)

                self.tableWidget.itemActivated.connect(self.store_change_record)

                self.layout = QVBoxLayout()
                self.layout.addWidget(self.tableWidget)
                self.setLayout(self.layout)
                #self.show()
                if self.isEnabled():
                    self.refresh_data()

        def changeEvent(self, event):

            if event.type() == QtCore.QEvent.WindowStateChange:
                if self.isMinimized():
                    settingsDict['log-window'] = 'false'
                    #print("log-window: changeEvent:_>", settingsDict['log-window'])
                    # telnetCluster.showMinimized()
                elif self.isVisible():
                    settingsDict['log-window'] = 'true'
                    #print("log-window: changeEvent:_>", settingsDict['log-window'])
                QWidget.changeEvent(self, event)

        def refresh_data(self):
            #print("refresh_data:_>", All_records)
            self.tableWidget.clear()
            #self.tableWidget.insertRow()

            self.tableWidget.setHorizontalHeaderLabels(
                ["No", "     Date     ", "   Time   ", "Band", "   Call   ", "Mode", "RST r",
                 "RST s", "      Name      ", "      QTH      ", " Comments ",
                 " Time off ", " eQSL Rcvd "])

            self.allRecords = Fill_table(all_column=self.allCollumn, window=self, all_record=All_records, communicate=signal_complited)
            self.allRecords.start()
            #self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            #self.tableWidget.resizeRowsToContents()
            #time.sleep(2)
            self.allRows = len(All_records)
            #print("class Fill_table(QThread) - self.all_record >:", return_data)

        #def fill_data_table(self):
        #    fill = Fill_table(window=logWindow)
        #    fill.start()

        def get_all_record(self):
            return All_records

        def protectionItem(self, text, flags):
            tableWidgetItem = QTableWidgetItem(text)
            tableWidgetItem.setFlags(flags)
            return tableWidgetItem

        def store_change_record(self):

            #print("store_change_record")
            row = self.tableWidget.currentItem().row()
            record_number = self.tableWidget.item(row, 0).text()
            date = str(self.tableWidget.item(row, 1).text())
            date_formated = date.replace("-", "")
            time = str(self.tableWidget.item(row, 2).text())
            time_formated = time.replace(":", "")
            call = self.tableWidget.item(row, 4).text()
            freq = All_records[int(record_number) - 1]['FREQ']
            rstR = self.tableWidget.item(row, 6).text()
            rstS = self.tableWidget.item(row, 7).text()
            name = self.tableWidget.item(row, 8).text()
            qth = self.tableWidget.item(row, 9).text()
            operator = All_records[int(record_number) - 1]['OPERATOR']
            band = self.tableWidget.item(row, 3).text()
            comment = self.tableWidget.item(row, 10).text()
            time_off = self.tableWidget.item(row, 11).text()
            eQSL_QSL_RCVD = self.tableWidget.item(row, 12).text()
            mode = self.tableWidget.item(row, 5).text()
            string_in_file = All_records[int(record_number) - 1]['string_in_file']
            records_number = All_records[int(record_number) - 1]['records_number']

           # if 'string_in_file' in self.allRecord:
           #     pass

            #else:
            #    pass

            new_object = {'BAND': band, 'CALL': call, 'FREQ': freq, 'MODE': mode, 'OPERATOR': operator,
                          'QSO_DATE': date_formated, 'TIME_ON': time_formated, 'RST_RCVD': rstR, 'RST_SENT': rstS,
                          'NAME': name, 'QTH': qth, 'COMMENTS': comment, 'TIME_OFF': time_off,
                          'eQSL_QSL_RCVD': eQSL_QSL_RCVD,
                          'EOR': 'R\n', 'string_in_file': string_in_file, 'records_number': records_number}

           # print("store_change_record: NEW Object", new_object)
            Adi_file().store_changed_qso(new_object)
            All_records[int(record_number) - 1] = new_object

        def refresh_interface(self):

            self.update_color_schemes()

        def update_color_schemes(self):
            style = "background-color:" + settingsDict['background-color'] + "; color:" + \
                    settingsDict['color'] + ";"

            style_form = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
                'color-table'] + "; font: 12px;"
            self.tableWidget.setStyleSheet(style_form)

            self.setStyleSheet(style)

        def addRecord(self, recordObject):
            # <BAND:3>20M <CALL:6>DL1BCL <FREQ:9>14.000000
            # <MODE:3>SSB <OPERATOR:6>UR4LGA <PFX:3>DL1 <QSLMSG:19>TNX For QSO TU 73!.
            # <QSO_DATE:8:D>20131011 <TIME_ON:6>184700 <RST_RCVD:2>57 <RST_SENT:2>57 <TIME_OFF:6>184700
            # <eQSL_QSL_RCVD:1>Y <APP_LOGGER32_QSO_NUMBER:1>1  <EOR>
            # record to file
            stringToAdiFile = "<BAND:" + str(len(recordObject['BAND'])) + ">" + recordObject['BAND'] + "<CALL:" + str(
                len(recordObject['CALL'])) + ">"

            stringToAdiFile = stringToAdiFile + recordObject['CALL'] + "<FREQ:" + str(len(recordObject['FREQ'])) + ">" + \
                              recordObject['FREQ']
            stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(recordObject['MODE'])) + ">" + recordObject[
                'MODE'] + "<OPERATOR:" + str(len(recordObject['OPERATOR']))
            stringToAdiFile = stringToAdiFile + ">" + recordObject['OPERATOR'] + "<QSO_DATE:" + str(
                len(recordObject['QSO_DATE'])) + ">"
            stringToAdiFile = stringToAdiFile + recordObject['QSO_DATE'] + "<TIME_ON:" + str(
                len(recordObject['TIME_ON'])) + ">"
            stringToAdiFile = stringToAdiFile + recordObject['TIME_ON'] + "<RST_RCVD:" + str(
                len(recordObject['RST_RCVD'])) + ">" + recordObject['RST_RCVD']
            stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(recordObject['RST_SENT'])) + ">" + recordObject[
                'RST_SENT'] + "<NAME:" + str(
                len(recordObject['NAME'])) + ">" + recordObject['NAME'] + "<QTH:" + str(
                len(recordObject['QTH'])) + ">" + recordObject['QTH'] + "<COMMENTS:" + str(
                len(recordObject['COMMENTS'])) + ">" + recordObject[
                                  'COMMENTS'] + "<TIME_OFF:" + str(len(recordObject['TIME_OFF'])) + ">" + recordObject[
                                  'TIME_OFF'] + "<eQSL_QSL_RCVD:1>Y<EOR>\n"
            # print(stringToAdiFile)
            recordObject['string_in_file'] = Adi_file().get_last_string() + 1

            file = open(self.filename, 'a')
            resultWrite = file.write(stringToAdiFile)
            # print(resultWrite)
            if resultWrite > 0:
                file.close()
            else:
                print("QSO not write in logfile")
                file.close()
            #####

            # record to allRecord
            #print(recordObject)

            All_records.append(recordObject)
            all_rows = len(All_records)
            # record to table
            allCols = len(self.allCollumn)
            # row = self.allRows + 1
            # print(recordObject)
            # print (row)
            self.tableWidget.setRowCount(all_rows)
            self.tableWidget.insertRow(0)
            self.tableWidget.resizeRowsToContents()

            for col in range(allCols):
                if col == 1:
                    date = str(recordObject[self.allCollumn[col]])
                    date_formated = date[:4] + "-" + date[4:6] + "-" + date[6:]
                    self.tableWidget.setItem(0, col, QTableWidgetItem(date_formated))
                elif col == 2:
                    time = str(recordObject[self.allCollumn[col]])
                    time_formated = time[:2] + ":" + time[2:4] + ":" + time[4:]
                    self.tableWidget.setItem(0, col, QTableWidgetItem(time_formated))
                else:
                    self.tableWidget.setItem(0, col, QTableWidgetItem(recordObject[self.allCollumn[col]]))

        def search_in_table(self, call):
            list_dict = []
            if self.tableWidget.rowCount() > 0:
                for rows in range(self.tableWidget.rowCount()):
                    #print(self.tableWidget.item(rows, 4).text())
                    try:
                        if self.tableWidget.item(rows, 4).text() == call:
                            row_in_dict = {"No":self.tableWidget.item(rows,0).text(),
                                            "Date":self.tableWidget.item(rows,1).text(),
                                            "Time":self.tableWidget.item(rows,2).text(),
                                            "Band":self.tableWidget.item(rows,3).text(),
                                            "Call":self.tableWidget.item(rows,4).text(),
                                            "Mode":self.tableWidget.item(rows,5).text(),
                                            "Rstr":self.tableWidget.item(rows,6).text(),
                                            "Rsts":self.tableWidget.item(rows,7).text(),
                                            "Name":self.tableWidget.item(rows,8).text(),
                                            "Qth":self.tableWidget.item(rows,9).text(),
                                            "Comments":self.tableWidget.item(rows,10).text(),
                                            "Time_off":self.tableWidget.item(rows,11).text(),
                                            "Eqsl_sent":self.tableWidget.item(rows,12).text()}
                            list_dict.append(row_in_dict)
                    except Exception:
                        print("Search in table > Don't Load text from table")
                return list_dict


class logSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.foundList = []
        self.initUI()

    def initUI(self):

        self.setGeometry(int(settingsDict['log-search-window-left']), int(settingsDict['log-search-window-top']),
                         int(settingsDict['log-search-window-width']), int(settingsDict['log-search-window-height']))
        self.setWindowTitle('LinuxLog | Search')
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowOpacity(float(settingsDict['logSearch-opacity']))
        style = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + "; font: 12px;"
        self.setStyleSheet(style)

        # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
        #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
        #		   )
        self.tableWidget = QTableWidget()
        style_table = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + "; font: 12px;"
        self.tableWidget.setStyleSheet(style_table)
        fnt = self.tableWidget.font()
        fnt.setPointSize(9)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setFont(fnt)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        #self.show()

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                settingsDict['log-search-window'] = 'false'
                #print("log-search-window: changeEvent:_>", settingsDict['log-search-window'])
                    #telnetCluster.showMinimized()
            elif self.isVisible():
                settingsDict['log-search-window'] = 'true'
               # print("log-search-window: changeEvent:_>", settingsDict['log-search-window'])
            QWidget.changeEvent(self, event)

    def overlap(self, foundList):
        if foundList != "":
            allRows = len(foundList)
            #print("overlap", foundList)
            self.tableWidget.setRowCount(allRows)
            self.tableWidget.setColumnCount(10)
            self.tableWidget.setHorizontalHeaderLabels(
                ["No", "   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
                 "RST s", "      Name      ", "      QTH      "])
            self.tableWidget.resizeColumnsToContents()
            allCols = len(logWindow.allCollumn)
            # print(foundList[0]["CALL"])
            for row in range(allRows):
                for col in range(allCols):
                    pole = logWindow.allCollumn[col]
                    #print("foundList[row][pole]", foundList[row][pole])
                    self.tableWidget.setItem(row, col, QTableWidgetItem(foundList[row][pole]))

            self.tableWidget.resizeRowsToContents()
            self.tableWidget.resizeColumnsToContents()
            self.foundList = foundList
        else:
            self.tableWidget.clearContents()
        # print(self.foundList)

    def refresh_interface(self):

        self.update_color_schemes()

    def update_color_schemes(self):
        style = "background-color:" + settingsDict['background-color'] + "; color:" + \
                settingsDict['color'] + ";"

        style_form = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + "; font: 12px"
        self.tableWidget.setStyleSheet(style_form)

        self.setStyleSheet(style)

class check_update ():



    def __init__(self, APP_VERSION, settingsDict, parrentWindow):
        super().__init__()
        self.version = APP_VERSION
        self.settingsDict = settingsDict
        self.parrent = parrentWindow
        self.run()


    def run(self):

        server_url_get = 'http://357139-vds-bastonsv.gmhost.pp.ua'
        path_directory_updater_app = "/upd/"

        action = server_url_get+path_directory_updater_app+self.version+"/"+self.settingsDict['my-call']
        flag = 0
        data_flag = 0
        try:
            response = requests.get(action)
            flag = 1
        except Exception:
            flag = 0

        if flag == 1:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                version = soup.find(id="version").get_text()
                git_path = soup.find(id="git_path").get_text()
                date = soup.find(id="date").get_text()
                data_flag = 1
            except Exception:
                std.std.message(self.parrent, "You have latest version", "UPDATER")
                self.parrent.check_update.setText("> Check update <")
                self.parrent.check_update.setEnabled(True)
            if data_flag == 1:
                update_result = QMessageBox.question(self.parrent, "LinuxLog | Updater",
                                     "Found new version "+version+" install it?",
                                     buttons=QMessageBox.Yes | QMessageBox.No,
                                     defaultButton=QMessageBox.Yes)
                if update_result == QMessageBox.Yes:
                   # print("Yes")
                    #try:
                    self.parrent.check_update.setText("Updating")
                    adi_name_list = []
                    for file in os.listdir():
                        if file.endswith(".adi"):
                            adi_name_list.append(file)
                    print("found all .adi file")
                    rules_name_list = []
                    for file in os.listdir():
                        if file.endswith(".rules"):
                            rules_name_list.append(file)
                    print("found all .rules file")
                   # print("Rules name List:_>", rules_name_list)
                   # print("Adi name List:_>", adi_name_list)
                    home = expanduser("~")
                    print("Home path:_>", home)
                    if os.path.isdir(home+'/linuxlog-backup'):
                        os.system("rm -rf "+home+"/linuxlog-backup")
                    else:
                        pass
                    print("Create buckup folder (linuxlog-buckup)")
                    os.mkdir(home+"/linuxlog-backup")
                    for i in range(len(adi_name_list)):
                        os.system("cp '"+adi_name_list[i]+"' "+home+"/linuxlog-backup")
                    print("Copy all .adi file to backup folder")
                    for i in range(len(rules_name_list)):
                        os.system("cp  '" + rules_name_list[i] + "' " + home + "/linuxlog-backup")
                    print("Copy all .rules file to backup folder")
                    os.system("cp settings.cfg " + home+"/linuxlog-backup")
                    print("Copy settings.cfg to backup folder")

                    # archive dir
                    if os.path.isdir(home+'/linlog-old'):
                     pass
                    else:
                        os.system("mkdir "+home+"/linlog-old")
                    os.system("tar -cf "+home+"/linlog-old/linlog"+version+".tar.gz " + home + "/linlog/")
                    print("Create archive with linlog folder")
                    print("Delete Linlog folder")
                    # delete dir linlog
                    #os.system("rm -rf " + home + "/linlog")
                    # clone from git repository to ~/linlog
                    print("Git clone to new linlog folder")
                    os.system("git clone " + git_path + " " + home + "/linlog_"+version)

                    # copy adi and rules file from linuxlog-backup to ~/linlog

                    for i in range(len(adi_name_list)):
                        os.system("cp '"+home+"/linuxlog-backup/" + adi_name_list[i] + "' '" + home + "/linlog_"+version+"'")
                    for i in range(len(rules_name_list)):
                        os.system("cp '" + home + "/linuxlog-backup/" + rules_name_list[i] + "' '" + home + "/linlog_"+version+"'")

                    # read and replace string in new settings.cfg

                    file = open(home+"/linlog_"+version+"/settings.cfg", "r")
                    settings_list = {}
                    for configstring in file:
                        if configstring != '' and configstring != ' ' and configstring[0] != '#':
                            configstring = configstring.strip()
                            configstring = configstring.replace("\r", "")
                            configstring = configstring.replace("\n", "")
                            splitString = configstring.split('=')
                            settings_list.update({splitString[0]: splitString[1]})
                    file.close()
                    for key_new in settings_list:
                        for key_old in self.settingsDict:
                            if key_new == key_old:
                                 settings_list[key_new] = self.settingsDict[key_old]



                   # print("settings list^_>", settings_list)

                    filename = home+"/linlog_"+version+"/settings.cfg"
                    with open(filename, 'r') as f:
                        old_data = f.readlines()
                    for index, line in enumerate(old_data):
                        key_from_line = line.split('=')[0]
                        # print ("key_from_line:",key_from_line)
                        for key in settings_list:

                            if key_from_line == key:
                                # print("key",key , "line", line)
                                old_data[index] = key + "=" + settings_list[key] + "\n"
                    with open(filename, 'w') as f:
                        f.writelines(old_data)
                    # done!

                    os.system("chmod +x "+home+"/linlog_"+version+"/linlog")
                    with open(home+"/linlog/linlog", "w") as f:
                       string_to_file = ['#! /bin/bash\n', 'cd '+home+'/linlog_'+version+'\n', 'python3 main.py\n']
                       f.writelines(string_to_file)

                    #delete backup dir
                    os.system("rm -rf " + home + "/linuxlog-backup")

                    os.system("rm -rf " + home + "/linlog_"+self.version)

                    std.std.message(self.parrent, "Update to v."+version+" \nCOMPLITED \n "
                                                                         "Please restart LinuxLog", "UPDATER")
                    self.version = version
                    self.parrent.check_update.setText("> Check update <")
                    self.parrent.check_update.setEnabled(True)
                    self.parrent.text.setText("Version:"+version+"\n\nBaston Sergey\nbastonsv@gmail.com")


                else:
                  #  print("No")
                    self.parrent.check_update.setText("> Check update <")
                    self.parrent.check_update.setEnabled(True)

        else:
            std.std.message(self.parrent, "Sorry\ntimeout server.", "UPDATER")



class About_window(QWidget):
    def __init__(self, capture, text):
        super().__init__()
        self.capture_string = capture
        self.text_string = text
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        #self.setGeometry(100,100,210,100)
        width_coordinate = (desktop.width() / 2) - 100
        height_coordinate = (desktop.height() / 2) - 100
        #self.setWindowModified(False)
        self.setFixedHeight(200)
        self.setFixedWidth(320)

        self.setGeometry(int(width_coordinate), int(height_coordinate), 200, 300)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('About | LinuxLog')
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        self.capture = QLabel(self.capture_string)
        self.capture.setStyleSheet("font-size: 18px")
        self.capture.setFixedHeight(30)
        self.text = QLabel(self.text_string)
        #self.text.setFixedHeight(200)
        self.text.setStyleSheet("font-size: 12px")
        self.about_layer = QVBoxLayout()
        self.image = QPixmap("logo.png")
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(self.image)
        #about_layer.setAlignment(Qt.AlignCenter)
        self.check_update = QPushButton()
        self.check_update.setFixedWidth(130)
        self.check_update.setFixedHeight(60)
        self.check_update.setText("> Check update <")
        self.check_update.setStyleSheet("size: 10px;")

        self.check_update.clicked.connect(self.updater)
        self.about_layer.addWidget(self.capture)
        self.about_layer.addSpacing(5)
        self.about_layer.addWidget(self.check_update)
        self.about_layer.addWidget(self.text)
        self.horizontal_lay = QHBoxLayout()
        self.horizontal_lay.addWidget(self.image_label)
        self.horizontal_lay.addLayout(self.about_layer)

        self.setLayout(self.horizontal_lay)

    def updater(self):
        self.check_update.setEnabled(False)
        self.check_update.setText("Found update")
        self.check = check_update(APP_VERSION, settingsDict=settingsDict, parrentWindow=self)
        #self.check.start()

class realTime(QThread):

    def __init__(self, logformwindow, parent=None):
        super().__init__()
        self.logformwindow = logformwindow

    def run(self):

        while 1:
            self.logformwindow.labelTime.setText("Loc: "+strftime("%H:%M:%S", localtime())+
                                                 "  |  GMT: "+strftime("%H:%M:%S", gmtime()))
            time.sleep(0.5)

class logForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.diploms_init()
        #self.diploms = self.get_diploms()
        self.initUI()


        #print("self.Diploms in logForm init:_>", self.diploms)


    def menu(self):

        logSettingsAction = QAction('&Settings', self)
        #logSettingsAction.setStatusTip('Name, Call and other of station')
        logSettingsAction.triggered.connect(self.logSettings)
        #
        window_cluster_action = QAction('Cluster', self)
        #windowAction.setStatusTip('Name, Call and other of station')
        window_cluster_action.triggered.connect(self.stat_cluster)
        #
        window_inet_search_action = QAction ('Internet search', self)
        window_inet_search_action.triggered.connect(self.stat_internet_search)
        #
        window_repeat_qso_action = QAction ('Repeat QSO', self)
        window_repeat_qso_action.triggered.connect(self.stat_repeat_qso)


        self.menuBarw = self.menuBar()
        self.menuBarw.setStyleSheet("QWidget{font: 12px;}")
      #  settings_menu = menuBar.addMenu('Settings')
        self.menuBarw.addAction(logSettingsAction)
        WindowMenu = self.menuBarw.addMenu('&Window')
        #WindowMenu.triggered.connect(self.logSettings)
        WindowMenu.addAction(window_cluster_action)
        WindowMenu.addAction(window_inet_search_action)
        WindowMenu.addAction(window_repeat_qso_action)

        self.otherMenu = self.menuBarw.addMenu('&Diploms')
        window_form_diplom = QAction('New diploma', self)
        window_form_diplom.triggered.connect(self.new_diplom)
        self.otherMenu.addAction(window_form_diplom)
        #
        aboutAction = QAction('&About', self)
        # logSettingsAction.setStatusTip('Name, Call and other of station')
        aboutAction.triggered.connect(self.about_window)
        self.menuBarw.addAction(aboutAction)

        if self.diploms != []:

            for i in range(len(self.diploms)):
                diplom_data = self.diploms[i].get_data()
                #print("self.diploms:_>", diplom_data[0]['name'])
                self.menu_add(diplom_data[0]['name'])

        '''
        catSettingsAction = QAction(QIcon('logo.png'), 'Cat settings', self)
        catSettingsAction.setStatusTip('Name, Call and other of station')
        catSettingsAction.triggered.connect(self.logSettings)
        #
        logWindowAction = QAction(QIcon('logo.png'), 'All log Window', self)
        logWindowAction.setStatusTip('Name, Call and other of station')
        logWindowAction.triggered.connect(self.logSettings)
        #
        searchWindowAction = QAction(QIcon('logo.png'), 'Search window', self)
        searchWindowAction.setStatusTip('Name, Call and other of station')
        searchWindowAction.triggered.connect(self.searchWindow)
        #
        importAdiAction = QAction(QIcon('logo.png'), 'Import ADI', self)
        importAdiAction.setStatusTip('Name, Call and other of station')
        importAdiAction.triggered.connect(self.logSettings)
        #
        exportAdiAction = QAction(QIcon('logo.png'), 'Export ADI', self)
        exportAdiAction.setStatusTip('Name, Call and other of station')
        exportAdiAction.triggered.connect(self.logSettings)
        #

        telnetAction = QAction(QIcon('logo.png'), 'Cluster window', self)
        telnetAction.setStatusTip('Name, Call and other of station')
        telnetAction.triggered.connect(self.logSettings)
        #
        newDiplomEnvAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        newDiplomEnvAction.setStatusTip('Name, Call and other of station')
        newDiplomEnvAction.triggered.connect(self.logSettings)
        #
        helpAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        helpAction.setStatusTip('Name, Call and other of station')
        helpAction.triggered.connect(self.logSettings)
        #
        aboutAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        aboutAction.setStatusTip('Name, Call and other of station')
        aboutAction.triggered.connect(self.logSettings)
        #
        exitAction = QAction(QIcon('logo.png'), '&Exit', self)
        exitAction.triggered.connect(QApplication.quit)

        menuBar = self.menuBar()
        mainMenu = menuBar.addMenu('&Menu')
        mainMenu.addAction(logSettingsAction)
        mainMenu.addAction(catSettingsAction)
        searchWindowMenu = mainMenu.addMenu('Window')
        searchWindowMenu.addAction(telnetAction)
        searchWindowMenu.addAction(logWindowAction)
        searchWindowMenu.addAction(searchWindowAction)
        mainMenu.addAction(importAdiAction)
        mainMenu.addAction(exportAdiAction)
        diplomMenu = mainMenu.addMenu('Diplom Env.')
        diplomMenu.addAction(newDiplomEnvAction)
        mainMenu.addAction(exitAction)
        ###
        helpMenu = menuBar.addMenu('Help')
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)
        '''
        #pass

    def menu_add(self, name_menu):
        # self.otherMenu = self.menuBarw.addMenu('&Other')

       # print(name_menu)
        self.item_menu = self.otherMenu.addMenu(name_menu)
        edit_diploma = QAction('Edit '+name_menu, self)
        edit_diploma.triggered.connect(lambda checked, name_menu=name_menu : self.edit_diplom(name_menu))
        show_stat = QAction('Show statistic', self)
        show_stat.triggered.connect(lambda checked, name_menu=name_menu : self.show_statistic_diplom(name_menu))
        del_diploma = QAction ("Delete "+name_menu, self)
        del_diploma.triggered.connect(lambda checked, name_menu=name_menu : self.del_diplom(name_menu))
        self.item_menu.addAction(show_stat)
        self.item_menu.addAction(edit_diploma)
        self.item_menu.addAction(del_diploma)

    def menu_rename_diplom(self):
        self.menuBarw.clear()
        #self.otherMenu.clear()



    def edit_diplom(self, name):
        all_data = ext.diplom.get_rules(self=ext.diplom, name=name+".rules")
        self.edit_window = ext.Diplom_form(settingsDict=settingsDict, log_form=self,
                        adi_file=adi_file, diplomname=name, list_data=all_data)
        self.edit_window.show()

        #print("edit_diplom:_>", name, "all_data:", all_data)

    def show_statistic_diplom(self, name):
        self.stat_diplom = ext.static_diplom(diplom_name=name, settingsDict=settingsDict)
        self.stat_diplom.show()
        #print("show_statistic_diplom:_>", name)

    def del_diplom (self, name):
        ext.diplom.del_dilpom(ext.diplom, name, settingsDict, self)
        #print("del_diplom:_>", name)

    def new_diplom(self):
        #new_diploma = ext.Diplom_form(settingsDict=settingsDict, log_form=logForm)

        #diploma.show()
        new_diploma.show()

    def about_window(self):
       # print("About_window")
        about_window.show()

    def searchWindow(self):

        logSearch.hide()

    def initUI(self):
        font = QFont("Cantarell Light", 10, QFont.Normal)
        QApplication.setFont(font)
        styleform = "background :" + settingsDict['form-background']+\
                    "; color: " + settingsDict['color-table'] + ";"
        self.setGeometry(int(settingsDict['log-form-window-left']), int(settingsDict['log-form-window-top']),
                         int(settingsDict['log-form-window-width']), int(settingsDict['log-form-window-height']))
        self.setWindowTitle('LinuxLog | Form')
        self.setWindowIcon(QIcon('logo.png'))
        style = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";"
        self.setStyleSheet(style)
        self.menu()

        # self.test()
        self.labelCall = QLabel("Call")
        self.labelCall.setFont(QtGui.QFont('SansSerif', 9))

        # labelCall.move(40,40)
        self.inputCall = QLineEdit()
        self.inputCall.setFocusPolicy(Qt.StrongFocus)
        self.inputCall.setStyleSheet(styleform)
        self.inputCall.setFixedWidth(108)
        self.inputCall.setFixedHeight(30)
        self.inputCall.textChanged[str].connect(
            self.onChanged)  # событие изминения текста, привязываем в слот функцию onChanged
        self._filter = Filter()
        # adjust for your QLineEdit
        self.inputCall.installEventFilter(self._filter)
        self.inputCall.returnPressed.connect(
            self.logFormInput)  # событие нажатия Enter, привязываем в слот функцию logSettings
        #self.inputCall.tabPressed.connect(self.internetWorker.get_internet_info)
        # inputCall.move(40,40)
        self.labelRstR = QLabel('RSTr')
        self.labelRstR.setFont(QtGui.QFont('SansSerif', 7))

        self.inputRstR = QLineEdit(self)
        self.inputRstR.setFixedWidth(30)
        self.inputRstR.setFixedHeight(30)
        self.inputRstR.setStyleSheet(styleform)
        self.inputRstR.returnPressed.connect(self.logFormInput)

        self.inputRstR.installEventFilter(self._filter)

        self.labelRstS = QLabel('RSTs')
        self.labelRstS.setFont(QtGui.QFont('SansSerif', 7))
        self.inputRstS = QLineEdit(self)
        self.inputRstS.setFixedWidth(30)
        self.inputRstS.setFixedHeight(30)
        self.inputRstS.setStyleSheet(styleform)
        self.inputRstS.returnPressed.connect(self.logFormInput)

        self.labelName = QLabel('Name')
        self.labelName.setFont(QtGui.QFont('SansSerif', 9))
        self.inputName = QLineEdit(self)
        self.inputName.setFixedWidth(137)
        self.inputName.setFixedHeight(30)
        self.inputName.setStyleSheet(styleform)
        self.inputName.returnPressed.connect(self.logFormInput)

        self.labelQth = QLabel("QTH  ")
        self.labelQth.setFont(QtGui.QFont('SansSerif', 9))

        self.inputQth = QLineEdit(self)
        self.inputQth.setFixedWidth(137)
        self.inputQth.setFixedHeight(30)
        self.inputQth.setStyleSheet(styleform)
        self.inputQth.returnPressed.connect(self.logFormInput)

        self.comboMode = QComboBox(self)
        self.comboMode.setFixedWidth(80)
        self.comboMode.setFixedHeight(30)
        self.comboMode.addItems(["SSB", "ESSB", "CW", "AM", "FM", "DSB", "DIGI"])
        indexMode = self.comboMode.findText(settingsDict['mode'])
        self.comboMode.setCurrentIndex(indexMode)
        self.comboMode.activated[str].connect(self.rememberMode)

        self.comboBand = QComboBox(self)
        self.comboBand.setFixedWidth(80)
        self.comboBand.setFixedHeight(30)
        self.comboBand.addItems(["160", "80", "40", "30", "20", "17", "15", "12", "10", "6", "2", "100", "200"])
        indexBand = self.comboBand.findText(settingsDict['band'])
        self.comboBand.setCurrentIndex(indexBand)
        self.comboBand.activated[str].connect(self.rememberBand)

        self.labelStatusCat = QLabel('    ')
        self.labelStatusCat.setAlignment(Qt.AlignLeft)
        self.labelStatusCat.setFont(QtGui.QFont('SansSerif', 7))

        self.labelStatusTelnet = QLabel('')
        self.labelStatusTelnet.setAlignment(Qt.AlignLeft)
        self.labelStatusTelnet.setFont(QtGui.QFont('SansSerif', 7))

        self.labelTime = QLabel()
        self.labelTime.setFont(QtGui.QFont('SansSerif', 7))


        self.labelFreq = QLabel()
        self.labelFreq.setFont(QtGui.QFont('SansSerif', 7))
        self.labelFreq.setText('')

        self.labelMyCall = QLabel(settingsDict['my-call'])
        self.labelMyCall.setFont(QtGui.QFont('SansSerif', 10))
        self.comments = QTextEdit()
        self.comments.setFontPointSize(10)
        self.comments.setFontWeight(3)
        self.comments.setPlaceholderText("Comment")
        self.comments.setFixedHeight(60)

        hBoxHeader = QHBoxLayout()
        hBoxHeader.addWidget(self.labelTime)

        #hBoxLeft = QHBoxLayout(self)
        #hBoxRight = QHBoxLayout(self)
        hBoxRst = QHBoxLayout(self)

        vBoxLeft = QVBoxLayout(self)

        vBoxRight = QVBoxLayout(self)
        vBoxMain = QVBoxLayout(self)
        # Build header line
        hBoxHeader.addStretch(20)
        hBoxHeader.addWidget(self.labelFreq)
        hBoxHeader.addWidget(self.labelMyCall)
        # Build Left block
        # vBoxLeft.addLayout(hBoxHeader)

        # set label Call
        # set input CALL
        hCall = QHBoxLayout(self)
        hCall.addWidget(self.labelCall)
        hCall.addWidget(self.inputCall)
        hCall.addStretch(1)
        vBoxLeft.addLayout(hCall)

        hBoxRst.addWidget(self.labelRstR)  # set label RSTr
        hBoxRst.addWidget(self.inputRstR)
        hBoxRst.addWidget(self.labelRstS)  # set input RSTr
        hBoxRst.addWidget(self.inputRstS)
        hBoxRst.addStretch(1)

        vBoxLeft.addLayout(hBoxRst)
        hName = QHBoxLayout(self)

        hName.addWidget(self.labelName)
        hName.addWidget(self.inputName)
        hName.addStretch(1)
        vBoxLeft.addLayout(hName)

        hQth = QHBoxLayout(self)
        hQth.addWidget(self.labelQth)
        hQth.addWidget(self.inputQth)
        hQth.addStretch(1)
        vBoxLeft.addLayout(hQth)

        # vBoxLeft.addWidget( labelName) #set label Name
        # vBoxLeft.addWidget( inputName) #set input Name
        # vBoxLeft.addWidget( labelQth)  #set label QTH
        # vBoxLeft.addWidget( inputQth)  #set input RSTr

        vBoxRight.addWidget(self.comboBand)
        vBoxRight.addWidget(self.comboMode)
        vBoxRight.addStretch(1)
        #vBoxRight.addWidget(self.labelStatusCat)
        #vBoxRight.addWidget(self.labelStatusTelnet)

        leftRight = QHBoxLayout()

        leftRight.addLayout(vBoxLeft)
        leftRight.addLayout(vBoxRight)
        # leftRight.setAlignment(Qt.AlignHCenter)

        vBoxMain.addLayout(hBoxHeader)
        vBoxMain.addLayout(leftRight)

        hBoxStatus = QHBoxLayout()
        hBoxStatus.setAlignment(Qt.AlignRight)
        hBoxStatus.addWidget(self.labelStatusTelnet)
        hBoxStatus.addWidget(self.labelStatusCat)

        vBoxMain.addWidget(self.comments)
        vBoxMain.addLayout(hBoxStatus)

        style = "QTextEdit{background:" + settingsDict['form-background'] + "; border: 1px solid " + settingsDict[
            'solid-color'] + ";}"
        self.comments.setStyleSheet(style)

        central_widget = QWidget()
        central_widget.setLayout(vBoxMain)
        self.setCentralWidget(central_widget)

       # self.show()

        # run time in Thread
        self.run_time = realTime(logformwindow=self) #run time in Thread
        self.run_time.start()

    def rememberBand(self, text):
        with open('settings.cfg', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        for i in range(len(data)):
            string = data[i]
            string = string.strip()
            string = string.replace("\r", "")
            string = string.replace("\n", "")
            string = string.split('=')
            # print(string)
            if data[i][0] != "#":
                if string[0] == 'band':
                    string[1] = self.comboBand.currentText().strip()
                data[i] = string[0] + '=' + string[1] + '\n'
                with open('settings.cfg', 'w') as file:
                    file.writelines(data)

    def rememberMode(self, text):
        # print(self.comboMode.currentText())
        with open('settings.cfg', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        for i in range(len(data)):
            string = data[i]
            string = string.strip()
            string = string.replace("\r", "")
            string = string.replace("\n", "")
            string = string.split('=')
            # print(string)
            if data[i][0] != "#":
                if string[0] == 'mode':
                    string[1] = self.comboMode.currentText().strip()
                data[i] = string[0] + '=' + string[1] + '\n'
                with open('settings.cfg', 'w') as file:
                    file.writelines(data)

    def key_lay_reverse(self, string: str):
        '''
        This method reciev string on russian and reverse lay
        in equivalent to english keyboard lay. ЙЦУКЕН => QWERTY
        :param string: input original string
        :return:
        '''

        reverse_dict = {"Й":"Q", "Ц":"W", "У":"E", "К":"R", "Е":"T", "Н":"Y", "Г":"U",
                        "Ш":"I", "Щ":"O", "З":"P", "Х":"", "Ъ":"",
                        "Ф":"A", "Ы":"S", "В":"D", "А":"F", "П":"G", "Р":"H", "О":"J",
                        "Л":"K", "Д":"L", "Ж":":","Э":"",
                        "Я":"Z", "Ч":"X", "С":"C", "М":"V", "И":"B", "Т":"N", "Ь":"M",
                        "Б":"", "Ю":"",".":"/"}
        new_string = ""

        for char in string:
                if re.search('[А-Я]', char):
                    char_reverse = reverse_dict[char]
                else:
                    char_reverse = char
                new_string += char_reverse
        return new_string

    def onChanged(self, text):
        '''метод которій отрабатывает как только произошло изменение в поле ввода'''
        self.inputCall.setText(text.upper())

        if re.search('[А-Я]', text):
            #self.inputCall.setStyleSheet("color: rgb(255,2,2);")
            string_old = self.inputCall.text()
            string_reverse = self.key_lay_reverse(string_old)
            self.inputCall.setText(string_reverse)
        #elif re.search('[A-Z]', text):
            #style = "border: 1px solid " + settingsDict[
            #    'solid-color'] + "; border-radius: 50px; background: " + settingsDict[
             #           'form-background'] + "; font-weight: bold;"
           # self.inputCall.setStyleSheet(style)
            # pyautogui.hotkey('ctrl', 'shift')
            # print(text)

        # print (locale)

    def logFormInput(self):

        call = str(self.inputCall.text()).strip()
        # print(call+ "this")
        if call != '':
            recordObject = {}
            #freq = str(self.labelFreq.text()).strip()

            mode = str(self.comboMode.currentText()).strip()
            rstR = str(self.inputRstR.text()).strip()
            rstS = str(self.inputRstS.text()).strip()
            name = str(self.inputName.text()).strip()
            qth = str(self.inputQth.text()).strip()
            operator = str(self.labelMyCall.text()).strip()
            band = str(self.comboBand.currentText()).strip() + "M"
            comment = str(self.comments.toPlainText()).strip()
            comment = comment.replace("\r", " ")
            comment = comment.replace("\n", " ")
            freq = self.get_freq()
            eQSL_QSL_RCVD = "N"
            all_records = logWindow.get_all_record()            # print("'QSO_DATE':'20190703', 'TIME_ON':'124600', 'FREQ':"+freq+" 'CALL':"+cal+"'MODE'"+mode+" 'RST_RCVD':"+rstR+" 'RST_SENT':"+rstS+", 'NAME':"+name+", 'QTH':"+qth+"'OPERATOR':"+operator+"'BAND':"+band+"'COMMENT':"+comment)
            record_number = len(All_records) + 1

            #print("record_number:", record_number)
            datenow = datetime.datetime.now()
            date = datenow.strftime("%Y%m%d")
            time = str(strftime("%H%M%S", gmtime()))


            recordObject = {'records_number': str(record_number), 'QSO_DATE': date, 'TIME_ON': time, 'FREQ': freq, 'CALL': call, 'MODE': mode,
                            'RST_RCVD': rstR, 'RST_SENT': rstS, 'NAME': name, 'QTH': qth, 'OPERATOR': operator,
                            'BAND': band, 'COMMENTS': comment, 'TIME_OFF': time,
                            'eQSL_QSL_RCVD': eQSL_QSL_RCVD}

            logWindow.addRecord(recordObject)
            call_dict = {'call': call, 'mode': mode, 'band': band}
            print ("call_dict:_>", call_dict)
            if settingsDict['diplom'] == 'enable':
                for diploms in self.diploms:
                    if diploms.filter(call_dict):
                        #print("filter true for:", diploms, "string:", recordObject)
                        diploms.add_qso(recordObject)

            if settingsDict['eqsl'] == 'enable':
                sync_eqsl = internetworker.Eqsl_services(settingsDict=settingsDict, recordObject=recordObject,std=std.std, parent_window=self)
                sync_eqsl.start()
            try:
                tci.Tci_sender(settingsDict['tci-server'] + ":" + settingsDict['tci-port']).change_color_spot(call, freq)
            except:
                print ("LogFormInput: can't connect to TCI server (set spot)")

            logForm.inputCall.setFocus(True)

            self.inputCall.clear()
            self.inputRstS.setText('59')
            self.inputRstR.setText('59')
            self.inputName.clear()
            self.inputQth.clear()
            self.comments.clear()
            try:
                logSearch.tableWidget.clearContents()
                internetSearch.update_photo()
            except Exception:
                pass

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                if settingsDict['search-internet-window'] == 'true':
                    internetSearch.showMinimized()
                    settingsDict['search-internet-window'] = 'true'
                if settingsDict['log-search-window'] == 'true':
                    logSearch.showMinimized()
                    settingsDict['log-search-window'] = 'true'
                if settingsDict['log-window'] == 'true':
                    logWindow.showMinimized()
                    settingsDict['log-window'] = 'true'
                if settingsDict['telnet-cluster-window'] == 'true':
                    telnetCluster.showMinimized()
                    settingsDict['telnet-cluster-window'] = 'true'
            QWidget.changeEvent(self, event)

    def showEvent(self, event):
        #print("Show Event", settingsDict['log-window'])
        if settingsDict['log-window'] == 'true':
            #print("Show Event", settingsDict['log-window'])
            logWindow.showNormal()

        if settingsDict['log-search-window'] == 'true':
            logSearch.showNormal()
        if settingsDict['telnet-cluster-window'] == 'true':
            telnetCluster.showNormal()
        if settingsDict['search-internet-window'] == 'true':
            internetSearch.showNormal()
        #print ("Show normal")

    def closeEvent(self, event):
        '''
        This function recieve signal close() from logSearch window
        Save coordinate and size all window
        Close app
        '''
        self.parameter={}
        if settingsDict['log-window'] == 'true':

            logWindow_geometry = logWindow.geometry()
            self.parameter.update({'log-window-left': str(logWindow_geometry.left()),
                              'log-window-top': str(logWindow_geometry.top()),
                              'log-window-width': str(logWindow_geometry.width()),
                              'log-window-height': str(logWindow_geometry.height())
                              })

        if settingsDict['search-internet-window'] == 'true':

            internetSearch_geometry = internetSearch.geometry()
            self.parameter.update({'search-internet-left': str(internetSearch_geometry.left()),
                              'search-internet-top': str(internetSearch_geometry.top()),
                              'search-internet-width': str(internetSearch_geometry.width()),
                              'search-internet-height': str(internetSearch_geometry.height())
                              })
        if settingsDict['log-search-window'] == 'true':

            logSearch_geometry = logSearch.geometry()
            self.parameter.update({'log-search-window-left': str(logSearch_geometry.left()),
                              'log-search-window-top': str(logSearch_geometry.top()),
                              'log-search-window-width': str(logSearch_geometry.width()),
                              'log-search-window-height': str(logSearch_geometry.height())
                              })
        if settingsDict['log-form-window'] == 'true':

            logForm_geometry = logForm.geometry()
            self.parameter.update({'log-form-window-left': str(logForm_geometry.left()),
                              'log-form-window-top': str(logForm_geometry.top()),
                              'log-form-window-width': str(logForm_geometry.width()),
                              'log-form-window-height': str(logForm_geometry.height())
                              })
        if settingsDict['telnet-cluster-window'] == 'true':

            telnetCluster_geometry = telnetCluster.geometry()
            self.parameter.update({'telnet-cluster-window-left': str(telnetCluster_geometry.left()),
                              'telnet-cluster-window-top': str(telnetCluster_geometry.top()),
                              'telnet-cluster-window-width': str(telnetCluster_geometry.width()),
                              'telnet-cluster-window-height': str(telnetCluster_geometry.height())
                              })
        '''
        internetSearch_geometry = internetSearch.geometry()
        settingsDict['search-internet-left'] = str(internetSearch_geometry.left())
        settingsDict['search-internet-top'] = str(internetSearch_geometry.top())
        settingsDict['search-internet-width'] = str(internetSearch_geometry.width())
        settingsDict['search-internet-height'] = str(internetSearch_geometry.height())
        ###
        logWindow_geometry = logWindow.geometry()
        settingsDict['log-window-left'] = str(logWindow_geometry.left())
        settingsDict['log-window-top'] = str(logWindow_geometry.top())
        settingsDict['log-window-width'] = str(logWindow_geometry.width())
        settingsDict['log-window-height'] = str(logWindow_geometry.height())
        ###
        logSearch_geometry = logSearch.geometry()
        settingsDict['log-search-window-left'] = str(logSearch_geometry.left())
        settingsDict['log-search-window-top'] = str(logSearch_geometry.top())
        settingsDict['log-search-window-width'] = str(logSearch_geometry.width())
        settingsDict['log-search-window-height'] = str(logSearch_geometry.height())
        ###
        logForm_geometry = logForm.geometry()
        settingsDict['log-form-window-left'] = str(logForm_geometry.left())
        settingsDict['log-form-window-top'] = str(logForm_geometry.top())
        settingsDict['log-form-window-width'] = str(logForm_geometry.width())
        settingsDict['log-form-window-height'] = str(logForm_geometry.height())
        ###
        telnetCluster_geometry = telnetCluster.geometry()
        settingsDict['telnet-cluster-window-left'] = str(telnetCluster_geometry.left())
        settingsDict['telnet-cluster-window-top'] = str(telnetCluster_geometry.top())
        settingsDict['telnet-cluster-window-width'] = str(telnetCluster_geometry.width())
        settingsDict['telnet-cluster-window-height'] = str(telnetCluster_geometry.height())

        ###
        '''


        logWindow.close()
        internetSearch.close()
        logSearch.close()
        logForm.close()
        telnetCluster.close()


        #print(parameter)
        if menu.isEnabled():
            menu.close()
        if about_window.isEnabled():
            about_window.close()
        self.remember_in_cfg(self.parameter)

    def remember_in_cfg (self, parameter):
        '''
        This function reciev Dictionary parametr with key:value
        record key=value into config.cfg

        :param parameter:
        :return:
        '''
       # print(parameter)
        filename='settings.cfg'
        with open(filename,'r') as f:
            old_data = f.readlines()
        for line, string in enumerate(old_data):
            #print(line, string)
            for key in parameter:
                if key in string:
                    string = key+"="+parameter[key]+"\n"
                    old_data[line] = string
        with open(filename, 'w') as f:
            f.writelines(old_data)

    def empty(self):
        print('hi')

    def logSettings(self):
        print('logSettings')
        #menu_window.show()

        menu.show()
        # logSearch.close()

    def stat_cluster(self):

        if telnetCluster.isHidden():
            print('statTelnet')
            telnetCluster.show()
        elif telnetCluster.isEnabled():
            telnetCluster.hide()

    def stat_internet_search(self):
        if internetSearch.isHidden():
            print('internet_search')
            internetSearch.show()
        elif internetSearch.isEnabled():
            internetSearch.hide()

    def stat_repeat_qso(self):
        if logSearch.isHidden():
            print('internet_search')
            logSearch.show()
        elif logSearch.isEnabled():
            logSearch.hide()

    def set_band(self, band):
        #print("LogForm.set_band. input band:", band)
        indexMode = self.comboBand.findText(band)
        self.comboBand.setCurrentIndex(indexMode)

    def set_freq(self, freq):
        freq_string = str(freq)
        freq_string = freq_string.replace('.', '')
        len_freq=len(freq)
        freq_to_label = freq[0:len_freq - 6] + "." + freq[len_freq - 6:len_freq - 3] + "." + freq[len_freq - 3:len_freq]
        self.labelFreq.setText("Freq: "+str(freq_to_label))
        band = std.std().get_std_band(freq)
        #print(band)
        indexMode = self.comboBand.findText(band)
        self.comboBand.setCurrentIndex(indexMode)

    def set_call(self, call):
        self.inputCall.setText(str(call))

    def set_mode_tci(self, mode):
        if mode == "lsb" or mode == "usb":
            mode_string = 'SSB'
        if mode == "am" or mode == "sam":
            mode_string = 'AM'
        if mode == "dsb":
            mode_string = 'DSB'
        if mode == "cw":
            mode_string = 'CW'
        if mode == "nfm" or mode == "wfm":
            mode_string = 'FM'
        if mode == "digl" or mode == "digu" or mode == "drm":
            mode_string = 'DIGI'
        indexMode = self.comboMode.findText(mode_string)
        self.comboMode.setCurrentIndex(indexMode)

    def set_tci_stat(self, values , color="#57BD79"):
        self.labelStatusCat.setStyleSheet("color: "+color+"; font-weight: bold;")
        self.labelStatusCat.setText(values)

    def set_tci_label_found(self, values=''):
        self.labelStatusCat.setStyleSheet("color: #FF6C49; font-weight: bold;")
        self.labelStatusCat.setText("TCI Found "+values)
        time.sleep(0.55)
        self.labelStatusCat.setText("")

    def set_telnet_stat(self):
        self.labelStatusTelnet.setStyleSheet("color: #57BD79; font-weight: bold;")
        self.labelStatusTelnet.setText("✔ Telnet")
        time.sleep(0.15)
        self.labelStatusTelnet.setText("")

    def get_band(self):
        return self.comboBand.currentText()

    def get_freq(self):
        freq_string = self.labelFreq.text()
        if freq_string == '':
            band = self.get_band()
            if band == "160":
                freq_string = '1800000'
            elif band == "80":
                freq_string = '3500000'
            elif band == "40":
                freq_string = '7000000'
            elif band == "30":
                freq_string = '10000000'
            elif band == "20":
                freq_string = '14000000'
            elif band == "17":
                freq_string = '18000000'
            elif band == "15":
                freq_string = '21000000'
            elif band == "12":
                freq_string = '24000000'
            elif band == "10":
                freq_string = '28000000'
            elif band == "6":
                freq_string = '54000000'
            elif band == "144":
                freq_string = '144500000'
            else:
                freq_string = 'non'
        freq_string = freq_string.replace('Freq: ', '')
        freq_string = freq_string.replace('.', '')
        #if len(str(freq_string)) < 8 and len(str(freq_string)) >= 5:
        #    freq_string = freq_string + "00"
        #if len(str(freq_string)) < 5:
         #   freq_string = freq_string + "000"

        return freq_string

    ## updates methods

    def refresh_interface(self):
        self.labelMyCall.setText(settingsDict['my-call'])
        self.update_color_schemes()

    def update_color_schemes(self):
        style = "background-color:" + settingsDict['background-color'] + "; color:" + \
                settingsDict['color'] + ";"
        self.labelCall.setStyleSheet(style)
        self.labelRstR.setStyleSheet(style)
        self.labelRstS.setStyleSheet(style)
        self.labelName.setStyleSheet(style)
        self.labelQth.setStyleSheet(style)
        self.labelTime.setStyleSheet(style)
        self.labelFreq.setStyleSheet(style)
        self.labelMyCall.setStyleSheet(style)
        self.comboMode.setStyleSheet(style)
        self.comboBand.setStyleSheet(style)
        self.labelStatusCat.setStyleSheet(style)
        style_form = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + "; font: 12px"
        self.inputCall.setStyleSheet(style_form)
        self.inputRstR.setStyleSheet(style_form)
        self.inputRstS.setStyleSheet(style_form)
        self.inputName.setStyleSheet(style_form)
        self.inputQth.setStyleSheet(style_form)
        self.comments.setStyleSheet(style_form)


        self.setStyleSheet(style)

    def update_settings(self, new_settingsDict):
        settingsDict.update(new_settingsDict)
        #print(settingsDict['my-call'])

    def test(data):
        pass

    def diploms_init(self):
        self.diploms = self.get_diploms()

    def get_diploms(self):
        names_diploms=[]
        if settingsDict['diploms-json'] != '':
            list_string = json.loads(settingsDict['diploms-json'])
            for i in range(len(list_string)):
                list_string[i]['name_programm'] = ext.diplom(list_string[i]['name_programm']+".adi", list_string[i]['name_programm']+".rules")
                names_diploms.append(list_string[i]['name_programm'])
        #print("names_diploms:_>", names_diploms)
        return names_diploms


class clusterThread(QThread):
    def __init__(self, cluster_window, form_window, parent=None):
        super().__init__()
        self.telnetCluster = cluster_window
        self.form_window = form_window
        # self.run()

    def run(self):
        HOST = settingsDict['telnet-host']
        PORT = settingsDict['telnet-port']
        call = settingsDict['my-call']
        while 1:
            try:
                telnetObj = telnetlib.Telnet(HOST, PORT)
                break
            except:
                time.sleep(3)
                continue

        lastRow = 0
        message = (call + "\n").encode('ascii')
        telnetObj.write(message)
        message2 = (call + "\n").encode('ascii')
        telnetObj.write(message2)
        splitString = []
        cleanList = []
        i = 0
        print('Starting Telnet cluster:', HOST, ':', PORT, '\nCall:', call, '\n\n')
        while 1:
          try:
            output_data = telnetObj.read_some()


            if output_data != '':
                    lastRow = self.telnetCluster.tableWidget.rowCount()
                    self.form_window.set_telnet_stat()
                    #print (output_data)
                    if output_data[0:2].decode(settingsDict['encodeStandart']) == "DX":
                        splitString = output_data.decode(settingsDict['encodeStandart']).split(' ')
                        count_chars = len(splitString)
                        for i in range(count_chars):
                            if splitString[i] != '':
                                cleanList.append(splitString[i])
                        #color = QColor(100, 50, 50)
                        search_in_diplom_rules_flag = 0
                        call_dict = {'call': cleanList[int(settingsDict['telnet-call-position'])].strip(),
                                     'mode': 'cluster',
                                     'band': 'cluster'}
                        diplom_list = logForm.get_diploms()

                        for i in range(len(diplom_list)):

                            #print("get_color:_>", color)
                            #print ("cicle Diploms:", diplom_list[i])
                            if diplom_list[i].filter(call_dict):
                                color = diplom_list[i].get_color_bg()
                                search_in_diplom_rules_flag = 1
                      #  print("clean list", cleanList[int(settingsDict['telnet-call-position'])].strip())

                        if telnetCluster.cluster_filter(cleanList=cleanList):
    #####
                            #print(cleanList) # Check point - output List with data from cluster telnet-server


                            self.telnetCluster.tableWidget.insertRow(lastRow)

                            #self.telnetCluster.tableWidget
                            self.telnetCluster.tableWidget.setItem(lastRow, 0,
                                                                   QTableWidgetItem(
                                                                       strftime("%H:%M:%S", localtime())))

                            #self.telnetCluster.tableWidget.item(lastRow, 0).setBackground(color)
                            if search_in_diplom_rules_flag == 1:
                                self.telnetCluster.tableWidget.item(lastRow, 0).setBackground(color)
                            self.telnetCluster.tableWidget.setItem(lastRow, 1,
                                                                   QTableWidgetItem(
                                                                       strftime("%H:%M:%S", gmtime())))

                            if search_in_diplom_rules_flag == 1:
                                self.telnetCluster.tableWidget.item(lastRow, 1).setBackground(color)

                            if (len(cleanList) > 4):
                                self.telnetCluster.tableWidget.setItem(lastRow, 2,
                                                                       QTableWidgetItem(cleanList[int(settingsDict['telnet-call-position'])]))
                                if search_in_diplom_rules_flag == 1:
                                    self.telnetCluster.tableWidget.item(lastRow, 2).setBackground(color)

                                self.telnetCluster.tableWidget.setItem(lastRow, 3,
                                                                       QTableWidgetItem(cleanList[int(settingsDict['telnet-freq-position'])]))
                                if search_in_diplom_rules_flag == 1:
                                    self.telnetCluster.tableWidget.item(lastRow, 3).setBackground(color)

    #self.telnetCluster.tableWidget.resizeColumnsToContents()
                            self.telnetCluster.tableWidget.setItem(lastRow, 4,
                                                                   QTableWidgetItem(
                                                                      output_data.decode(settingsDict['encodeStandart'])))

                            if search_in_diplom_rules_flag == 1:
                                 self.telnetCluster.tableWidget.item(lastRow, 4).setBackground(color)

                            self.telnetCluster.tableWidget.resizeColumnsToContents()
                            self.telnetCluster.tableWidget.resizeRowsToContents()
                            self.telnetCluster.tableWidget.scrollToBottom()

                            if settingsDict['spot-to-pan'] == 'enable':
                                freq = std.std().std_freq(freq=cleanList[3])
                                try:
                                    tci.Tci_sender(settingsDict['tci-server']+":"+settingsDict['tci-port']).set_spot(cleanList[4], freq, color="19711680")
                                except:
                                    print("clusterThread: Except in Tci_sender.set_spot")
                        ####
                    # #print(output_data) # Check point - output input-string with data from cluster telnet-server
                    elif output_data[0:3].decode(settingsDict['encodeStandart']) == "WWV":
                        self.telnetCluster.labelIonosphereStat.setText(
                            "Ionosphere status: " + output_data.decode(settingsDict['encodeStandart']))
                        #print("Ionosphere status: ", output_data.decode(settingsDict['encodeStandart']))
                    del cleanList[0:len(cleanList)]
                    time.sleep(0.3)
          except:
              continue

class telnetCluster(QWidget):

    def __init__(self):
        super().__init__()
        # self.mainwindow = mainwindow

        self.host = settingsDict['telnet-host']
        self.port = settingsDict['telnet-port']
        self.call = settingsDict['my-call']
        self.tableWidget = QTableWidget()
        self.allRows = 0

        self.initUI()

    def initUI(self):
        '''
         Design of cluster window

        '''

        self.setGeometry(int(settingsDict['telnet-cluster-window-left']), int(settingsDict['telnet-cluster-window-top']),
                         int(settingsDict['telnet-cluster-window-width']), int(settingsDict['telnet-cluster-window-height']))
        self.setWindowTitle('Telnet cluster')
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowOpacity(float(settingsDict['clusterWindow-opacity']))
        style = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";"
        self.setStyleSheet(style)
        self.labelIonosphereStat = QLabel()
        self.labelIonosphereStat.setStyleSheet("font: 12px;")
        style_table = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + "; font: 12px;"
        self.tableWidget.setStyleSheet(style_table)
        fnt = self.tableWidget.font()
        fnt.setPointSize(9)
        self.tableWidget.setFont(fnt)
        self.tableWidget.setRowCount(0)
        #self.tableWidget.horizontalHeader().setStyleSheet("font: 12px;")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Time Loc", "Time GMT", "Call", "Freq", " Spot"])
        self.tableWidget.verticalHeader().hide()
        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellClicked.connect(self.click_to_spot)
        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelIonosphereStat)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # logForm.test('test')

        self.start_cluster()

    def stop_cluster(self):

        print("stop_cluster:", self.run_cluster.terminate())

    def start_cluster(self):
        self.run_cluster = clusterThread(cluster_window=self, form_window=logForm)
        self.run_cluster.start()

    def click_to_spot(self):
        row = self.tableWidget.currentItem().row()
        freq = self.tableWidget.item(row, 3).text()
        call = self.tableWidget.item(row, 2).text()
        self.isearch = internetworker.internetWorker(window=internetSearch, callsign=call, settings=settingsDict)
        self.isearch.start()
        freq = std.std().std_freq(freq)


        '''len_freq = len(freq)
        if len_freq < 8 and len_freq <= 5:
            while len_freq < 7:
                freq +="0"
                len_freq=len(freq)
            freq = "0"+freq
        if len(freq) < 8 and len(freq) > 5 and len(freq) != 7:
            while len_freq<8:
                freq +="0"
                len_freq=len(freq)

        '''
        logForm.set_freq(freq)
        logForm.set_call(call=call)
        logForm.activateWindow()

        if settingsDict['tci'] == 'enable':
            try:
                tci.Tci_sender(settingsDict['tci-server'] + ":" + settingsDict['tci-port']).set_freq(freq)
            except:
                print("Set_freq_cluster: Can't connection to server:", settingsDict['tci-server'], ":",
                      settingsDict['tci-port'])

        #print("click_to_spot: freq:",freq) # Chek point

    def cluster_filter(self, cleanList):
        flag = False
        if len(cleanList) >= 4:
            #print("cluster_filter: len(cleanList)", len(cleanList))
            #print("cluster_filter: inputlist", cleanList)
            #print("cluster_filter: call", cleanList[4])
            #print("cluster_filter: prefix", cleanList[4][0:2])
            if settingsDict['cluster-filter'] == 'enable':
                ### filtering by spot prefix
                filter_by_band = False
                filter_by_spotter_flag = False
                filter_by_prefix_flag = False

                if settingsDict['filter-by-prefix'] == 'enable':
                    list_prefix_spot=settingsDict['filter-prefix'].split(',')
                    if cleanList[4][0:2] in list_prefix_spot:
                        filter_by_prefix_flag = True
                else:
                    filter_by_prefix_flag = True
                ### filtering by prefix spotter
                if settingsDict['filter-by-prefix-spotter'] == "enable":
                    list_prefix_spotter=settingsDict['filter-prefix-spotter'].split(',')
                    if cleanList[2][0:2] in list_prefix_spotter:
                        filter_by_spotter_flag = True
                else:
                    filter_by_spotter_flag = True
                ### filtering by band
                if settingsDict['filter_by_band'] == "enable":
                    list_prefix_spotter = settingsDict['list-by-band'].split(',')
                    freq = std.std().std_freq(cleanList[3])
                    band = std.std().get_std_band(freq)
                    if band in list_prefix_spotter:
                        filter_by_band = True
                else:
                    filter_by_band = True
                #print("cluster_filter: filter_by_prefix_flag:",filter_by_prefix_flag,
                      #"\nfilter_by_spotter_flag:",filter_by_spotter_flag,"\nfilter_by_band", filter_by_band)
                if filter_by_prefix_flag and filter_by_spotter_flag and filter_by_band:
                    flag = True
                else:
                    flag = False


            else:
                flag = True
        return flag

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                settingsDict['telnet-cluster-window'] = 'false'
                print("telnet-cluster-window: changeEvent:_>", settingsDict['telnet-cluster-window'])
                    #telnetCluster.showMinimized()
            elif self.isVisible():
                settingsDict['telnet-cluster-window'] = 'true'
                print("telnet-cluster-window: changeEvent:_>", settingsDict['telnet-cluster-window'])

            QWidget.changeEvent(self, event)

    def refresh_interface(self):

        self.update_color_schemes()

    def update_color_schemes(self):
        style = "background-color:" + settingsDict['background-color'] + "; color:" + \
                settingsDict['color'] + ";"
        self.labelIonosphereStat.setStyleSheet(style)
        style_form = "background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + "; font: 12px"
        self.tableWidget.setStyleSheet(style_form)

        self.setStyleSheet(style)

class internetSearch(QWidget):

    def __init__(self):
        super().__init__()
        self.labelImage = QLabel(self)
        #self.pixmap=""
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("logo.png")
        self.labelImage = QLabel(self)
        self.labelImage.setAlignment(Qt.AlignCenter)
        self.labelImage.setPixmap(self.pixmap)
        hbox.addWidget(self.labelImage)
        self.setLayout(hbox)

        #self.move(100, 200)
        self.setGeometry(int(settingsDict['search-internet-left']),
                         int(settingsDict['search-internet-top']),
                         int(settingsDict['search-internet-width']),
                         int(settingsDict['search-internet-height']))
        self.setWindowTitle('Telnet cluster')
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('Image from internet')
        self.setWindowOpacity(float(settingsDict['searchInetWindow-opacity']))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        #self.show()

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                settingsDict['search-internet-window'] = 'false'
                print("search-internet-window: changeEvent:_>", settingsDict['search-internet-window'])
                    #telnetCluster.showMinimized()
            elif self.isVisible():
                settingsDict['search-internet-window'] = 'true'
                print("search-internet-window: changeEvent:_>", settingsDict['search-internet-window'])

            QWidget.changeEvent(self, event)

    def update_photo(self):
        pixmap = QPixmap("logo.png")
        #self.labelImage.setFixedWidth(self.settings['image-width'])
        self.labelImage.setPixmap(pixmap)

    def refresh_interface(self):
        self.update_color_schemes()

    def update_color_schemes(self):
        style = "background-color:" + settingsDict['background-color'] + "; color:" + \
                settingsDict['color'] + ";"
        self.labelImage.setStyleSheet(style)
        self.setStyleSheet(style)

class hello_window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        width_coordinate = (desktop.width()/2) - 200
        height_coordinate = (desktop.height()/2) - 125
        print("hello_window: ", desktop.width(), width_coordinate)

        self.setGeometry(width_coordinate, height_coordinate, 400, 250)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('Welcome to LinLog')
        style = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";"
        self.setStyleSheet(style)
        style_caption = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + "; font-size: 36px;"
        self.caption_label = QLabel("Hi friend")
        self.caption_label.setStyleSheet(style_caption)
        style_text = "background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + "; font-size: 12px;"
        self.welcome_text_label = QLabel("It's first runing.\nPlease enter you callsign")
        self.welcome_text_label.setStyleSheet(style_text)
        self.call_input = QLineEdit()
        self.call_input.setStyleSheet("QWidget{background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color-table'] + ";}")
        self.call_input.setFixedWidth(150)
        self.ok_button = QPushButton("GO")
        self.ok_button.clicked.connect(self.ok_button_push)
        #self.caption_label.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(self.caption_label)
        vbox.addWidget(self.welcome_text_label)
        vbox.addWidget(self.call_input)
        vbox.addWidget(self.ok_button)
        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)
        self.show()

    def ok_button_push(self):
        if self.call_input.text().strip() != "":
            settingsDict['my-call'] = self.call_input.text().strip().upper()
            settings_file.save_all_settings(self)
            hello_window.close()
            subprocess.call(["python3", "main.py"])
            #subprocess.call("./main")
            #app.exit()




        else:
            self.welcome_text_label.setText("Please enter you callsign")
        print ("Ok_button")

class settings_file:


    def save_all_settings(self):
        print ("save_all_settings")
        filename = 'settings.cfg'
        with open(filename, 'r') as f:
            old_data = f.readlines()
        for index, line in enumerate(old_data):
            key_from_line = line.split('=')[0]
            # print ("key_from_line:",key_from_line)
            for key in settingsDict:

                if key_from_line == key:
                    # print("key",key , "line", line)
                    old_data[index] = key + "=" + settingsDict[key] + "\n"
        with open(filename, 'w') as f:
            f.writelines(old_data)
        print("Save_and_Exit_button: ", old_data)





if __name__ == '__main__':

    APP_VERSION = '1.2'
    settingsDict = {}
    file = open('settings.cfg', "r")
    for configstring in file:
        if configstring != '' and configstring != ' ' and configstring[0] != '#':
            configstring = configstring.strip()
            configstring = configstring.replace("\r", "")
            configstring = configstring.replace("\n", "")
            splitString = configstring.split('=')
            settingsDict.update({splitString[0]: splitString[1]})

    file.close()





    global All_records
    All_records = []


    print(settingsDict)
    flag = 1

    app = QApplication(sys.argv)
    signal_complited = Communicate()

    if settingsDict['my-call'] == "":
        hello_window = hello_window()
        #print(hello_window)
    else:
        #log_window1 = log_Window()
        #logWindow = log_window1
        logWindow = log_Window()
        logSearch = logSearch()
        internetSearch = internetSearch()
        logForm = logForm()
        telnetCluster = telnetCluster()
        tci_recv = tci.tci_connect(settingsDict, log_form=logForm)
        #### work with diplom filter and packing exempler of class into list
        #ext.test()

        #diplom_1 = ext.diplom('1.adi', "rules.json")
        #diplom_2 = ext.diplom('2.adi', 'rules2.json')
        #diplom_list = logForm.get_diploms()
        ########
        adi_file = Adi_file()
        about_window = About_window("LinuxLog", "Version: "+APP_VERSION+"<br><br>Baston Sergey<br>UR4LGA<br>bastonsv@gmail.com")
        new_diploma = ext.Diplom_form(settingsDict=settingsDict, log_form=logForm, adi_file=adi_file)
       # check = internetworker.check_update(APP_VERSION, settingsDict=settingsDict, parrentWindow=logForm)

        #print(diplom_log.filter('ur4lga'))
        if settingsDict['log-window'] == 'true':
           #pass
            logWindow.show()
            # Log_window() logWindow()
        if settingsDict['log-search-window'] == 'true':
            logSearch.show()

        if settingsDict['search-internet-window'] == 'true':
            internetSearch.show()

        if settingsDict['log-form-window'] == 'true':
            logForm.show()
            #logForm.setFocus()
        if settingsDict['tci'] == 'enable':

            tci_recv.start_tci(settingsDict["tci-server"], settingsDict["tci-port"])

        if settingsDict['telnet-cluster-window'] == 'true':
            telnetCluster.show()

        menu = settings.Menu(settingsDict,
                             telnetCluster,
                             logForm,
                             logSearch,
                             logWindow,
                             internetSearch,
                             tci_recv)



    #Adi_file().record_all_qso(list)
    sys.exit(app.exec_())
