#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QSizePolicy, QSpacerItem, QColorDialog, QTableWidget, QPushButton,QCalendarWidget, QLayout, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel, QCheckBox, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
import settings
import parse
import json
import main
import std
import os
class test:
    def __init__(self):
        list = [ { "call":
                     "EH8URT",
                 "score": "10"},
                 {"call": "Z81D",
                 "score": "10"},
                 {"call": "Z81D",
                  "score": "10"},
                 {"call": "VP8PJ",
                  "score": "10"},
                 {"call": "VP8LP",
                  "score": "10"}


                ]
        with open("rules.json", 'w') as f:
            f.write(json.dumps(list))
        #print("json.dumps", json.dumps(list))

class Diplom_form(QWidget):

    def __init__(self, settingsDict, log_form, adi_file, diplomname='', list_data=[]):
        super().__init__()
        #print("Diplom_form(QWidget) init_")
        self.logForm = log_form
        self.diplomname = diplomname
        self.settingsDict = settingsDict
        self.adi = adi_file
        self.list_data = list_data
        self.initUI()

    def initUI(self):
        if self.diplomname == '':
            self.setWindowTitle("Create diplom")
        else:
            self.setWindowTitle("Edit diplom "+self.diplomname)

            #rules = diplom.get_rules(diplom, self.diplomname+".rules")
        self.setGeometry(300, 500, 500, 300)
        #self.setFixedWidth(450)
        #self.setFixedHeight(450)
        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + self.settingsDict['background-color'] + "; color:" + self.settingsDict[
            'color'] + ";}"
        styleform = "background :" + self.settingsDict['form-background'] + "; font-weight: bold; color:"+ self.settingsDict['color-table']+";"
        self.setGeometry(int(self.settingsDict['log-form-window-left']), int(self.settingsDict['log-form-window-top']),
                         int(self.settingsDict['log-form-window-width']), int(self.settingsDict['log-form-window-height']))

        self.setStyleSheet(style)
        self.name_layout = QHBoxLayout()
        self.name_label = QLabel("Name diploma:")
        self.name_label.setFixedWidth(150)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(styleform)
        self.name_input.setFixedWidth(200)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)
        self.name_layout.addStretch(300)
        #








        #
        self.score_layout = QHBoxLayout()
        score_text = QLabel("How many points do you need")
        score_text.setStyleSheet(style)
        self.score_input = QLineEdit()
        self.score_input.setStyleSheet(styleform)
        self.score_input.setText("0")
        self.score_layout.addWidget(score_text)
        self.score_layout.addWidget(self.score_input)
        #
        self.repeat_layout = QHBoxLayout()
        self.text_repeat = QLabel("Repeats:")
        self.repeat_combo = QComboBox()
        self.repeat_combo.setFixedWidth(200)
        self.repeat_combo.addItems(["resolved other bands", "resolved others mod", "resolving other mods and bands", "not resolving"])
        self.repeat_layout.addWidget(self.text_repeat)
        self.repeat_layout.addWidget(self.repeat_combo)
        self.repeat_layout.addStretch(100)
        #
        self.sps_layout = QHBoxLayout()


        self.sps_text = QLabel("Special calls \n or prefix:")
        self.sps_table_widget = QTableWidget()
        self.sps_table_widget.setStyleSheet(styleform)
        self.sps_table_widget.setFixedWidth(240)
        self. sps_table_widget.setFixedHeight(200)
        self.sps_table_widget.setColumnCount(3)
        self.sps_table_widget.setColumnWidth(0, 80)
        self.sps_table_widget.setColumnWidth(1, 50)
        self.sps_table_widget.setColumnWidth(2, 70)
        self.sps_table_widget.setRowCount(10)
        self.sps_table_widget.setHorizontalHeaderLabels(['call', 'score', 'mode'])
        self.sps_table_widget.horizontalHeaderItem(0).setToolTip("Enter special call")
        self.sps_table_widget.horizontalHeaderItem(1).setToolTip("Enter scores for QSO")
        self.sps_table_widget.horizontalHeaderItem(2).setToolTip("Select mode")
        #self.combo_mode = QComboBox()
        #self.combo_mode2 = QComboBox()
        #self.combo_mode.addItems(['SSB', 'CW', 'DIGI'])
        #self.combo_mode2.addItems(['SSB', 'CW', 'DIGI'])
        row_count = self.sps_table_widget.rowCount()
        self.combo_mode_list = []
        if self.diplomname == '':


            for row in range(row_count):
                self.combo_mode_list.append({'combo'+str(row): QComboBox()})
                self.combo_mode_list[row]['combo' + str(row)].addItems(['SSB', 'CW', 'DIGI'])
                self.sps_table_widget.setCellWidget(row, 2, self.combo_mode_list[row]['combo'+str(row)])



        add_row = QPushButton("Add rows")
        add_row.clicked.connect(self.add_row)
        self.prefix_lay = QVBoxLayout()
        #self.prefix_lay.addWidget(self.prefix_check_box)
        self.prefix_lay.addWidget(self.sps_text)
        self.sps_layout.addLayout(self.prefix_lay)
        self.sps_layout.addWidget(self.sps_table_widget)
        self.sps_layout.addWidget(add_row)
        #
        self.button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.ok_button = QPushButton("Create diploma")
        self.ok_button.clicked.connect(self.save_diplom)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        #
        self.color_label = QLabel()
        self.color_label.setStyleSheet(style)
        self.color_label.setText("Select color for telnet highlight")
        self.color_button = QPushButton()
        #self.color_button.setFixedWidth(100)
        self.color_button.clicked.connect(self.select_color)
        if self.diplomname == '':
            self.color_button.setText("Select color")

        self.color_layout = QHBoxLayout()
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_button)
        #
        self.global_layout = QVBoxLayout()
        self.global_layout.addLayout(self.name_layout)
        #self.global_layout.addLayout(self.date_layout)
        #self.spaceItem = QSpacerItem(15, 10)
        #self.global_layout.addSpacerItem(self.spaceItem)
        self.global_layout.addLayout(self.color_layout)
        #self.global_layout.addSpacerItem(self.spaceItem)
        self.global_layout.addLayout(self.score_layout)
        self.global_layout.addLayout(self.repeat_layout)
        self.global_layout.addLayout(self.sps_layout)
        self.global_layout.addLayout(self.button_layout)
        self.setLayout(self.global_layout)
        if self.diplomname != '':
            self.add_info(self.list_data)

    def select_color(self):
        color = QColorDialog.getColor(initial=QColor(self.color_button.text()), parent=None, title="Select color for cluster highlight")
        if color.isValid():
            self.colorR = color.red()
            self.colorG = color.green()
            self.colorB = color.blue()
            self.color_name = color.name()
            self.color_button.setStyleSheet("background:"+color.name())
            self.color_button.setText(color.name())


    def add_info(self, list_data):
        #print ("list_data:_>",list_data)
        self.color_name = list_data[0]['color_name']
        self.colorR = list_data[0]['colorR']
        self.colorG = list_data[0]['colorG']
        self.colorB = list_data[0]['colorB']
        self.color_button.setStyleSheet("background:"+self.color_name)
        self.color_button.setText(self.color_name)
        self.name_input.setText(list_data[0]['name'])
        self.score_input.setText(list_data[0]['score_complite'])
        self.repeat_combo.setCurrentIndex(list_data[0]['repeats'])
        #if list_data[0]['date_e'] == 'y':
        #    self.date_checkbox.setChecked(True)
        #else:
        #    self.date_checkbox.setChecked(False)
        #if list_data[0]['prefix_only'] == 'y':
        #    self.prefix_check_box.setChecked(True)
        #else:
           #self.prefix_check_box.setChecked(False)

        rows = len(list_data)
        self.sps_table_widget.setRowCount(rows)
        for row in range(rows):
            self.sps_table_widget.setItem(row, 0, QTableWidgetItem(list_data[row]['call']))
            self.sps_table_widget.setItem(row, 1, QTableWidgetItem(list_data[row]['score']))
            self.combo_mode_list.append({'combo' + str(row): QComboBox()})
            self.combo_mode_list[row]['combo' + str(row)].addItems(['SSB', 'CW', 'DIGI'])
            self.combo_mode_list[row]['combo'+str(row)].setCurrentText(list_data[row]['mode'])
            self.sps_table_widget.setCellWidget(row, 2, self.combo_mode_list[row]['combo'+str(row)])
        self.sps_table_widget.resizeRowsToContents()


    def add_row(self):

        self.sps_table_widget.insertRow(self.sps_table_widget.rowCount())
        counter = self.sps_table_widget.rowCount()
        len(self.combo_mode_list)
        self.combo_mode_list.append({'combo' + str(counter - 1): QComboBox()})
        print ("all rows:_>", counter, len(self.combo_mode_list))
        self.combo_mode_list[len(self.combo_mode_list) - 1 ]['combo' + str(counter - 1)].addItems(['SSB', 'CW', 'DIGI'])
        self.sps_table_widget.setCellWidget(counter - 1 , 2, self.combo_mode_list[len(self.combo_mode_list) - 1]['combo' + str(counter - 1)])
        for i in range(len(self.combo_mode_list)):
            print("all keys:_>", self.combo_mode_list[i].keys())
        #pass

    def save_diplom(self):
        list_to_json = []
        settings_list = []
        flag = 0
        if self.name_input.text().strip() != '':
            flag = 1
        else:
            flag = 0
            self.name_input.setStyleSheet("border: 2px solid #DD5555;")
        print(self.color_button.text())
        if self.color_button.text() != 'Select color':
            flag = 1
        else:
            flag = 0
            self.color_button.setStyleSheet("border: 2px solid #DD5555;")
        if flag == 1:
            name_programm = self.name_input.text().strip()
            score_complite = self.score_input.text().strip()
            #if self.prefix_check_box.isEnabled():
             #   prefix_only = 'y'
           # else:
            #    prefix_only = 'n'

            #if self.date_checkbox.isChecked():
            #    date_enable = "y"
            #    date_start = self.start_date_input.text().strip()
            #    date_finish = self.end_date_input.text().strip()

            #else:
            #    date_enable = "n"
            #    date_start = ""
            #    date_finish = ""
            repeats = self.repeat_combo.currentIndex()
            count_sps = self.sps_table_widget.rowCount()
            #print("count_sps:_>", count_sps)
            for row in range(count_sps):

                if self.sps_table_widget.item(row,0) != None and \
                        self.sps_table_widget.item(row, 1) != None:
                   # print('Item content call', self.sps_table_widget.item(row, 0).text())
                    list_to_json.append({'call': self.sps_table_widget.item(row, 0).text().upper(),
                                      'score': self.sps_table_widget.item(row, 1).text(),
                                      'mode' : self.combo_mode_list[row]['combo'+str(row)].currentText(),
                                      'name': name_programm,
                                      'colorR':self.colorR,
                                      'colorG': self.colorG,
                                      'colorB': self.colorB,
                                      'color_name': self.color_name,
                                      'repeats':repeats, 'score_complite': score_complite,
                                      })
                    
            self.write_rules_to_file(list_to_json, name_output_file=name_programm)
            if self.settingsDict['diploms-json'] != "":
                settings_list = json.loads(self.settingsDict['diploms-json'])
                #print("settings_list", settings_list)
            else:
                print("settings list is empty")
                #settings_list.append({'name_programm': name_programm})
                self.settingsDict['diploms-json'] = json.dumps([{'name_programm': name_programm}])
                main.Settings_file.update_file_to_disk(self)
            if len(settings_list)>0:
                for i in range(len(settings_list)):
                    #name = str(settings_list[i]['name_programm'])
                    if name_programm == str(settings_list[i]['name_programm']) and self.diplomname == '':
                        std.std.message(self, "Programm with that name already exists", "Repeats")
                        repeat_flag = 1
                        break
                    else:
                        repeat_flag = 0
            else:
                repeat_flag = 0

            if repeat_flag == 0:
                if self.diplomname =='':
                    settings_list.append({'name_programm': name_programm})
                    self.settingsDict['diploms-json'] = json.dumps(settings_list)
                    main.Settings_file.update_file_to_disk(self)

                    self.logForm.menu_add(name_menu=self.name_input.text())
                    self.adi.create_adi(name_programm+".adi")
                    self.close()
                else:
                    programs = len(settings_list)
                    for i in range(programs):
                        if settings_list[i]['name_programm'] == self.diplomname:
                            self.adi.rename_adi(settings_list[i]['name_programm']+".adi", self.name_input.text() + ".adi")
                            settings_list[i]['name_programm'] = self.name_input.text()


                    #print(settings_list)
                    self.settingsDict['diploms-json'] = json.dumps(settings_list)
                    main.Settings_file.update_file_to_disk(self)

                    self.logForm.menu_rename_diplom()
                    self.logForm.diploms_init()
                    self.logForm.menu()
                    self.close()

            self.logForm.diploms_init()
        elif flag == 0:
            pass

    def write_rules_to_file(self, data_to_json, name_output_file):
        filename = str(name_output_file).strip()+'.rules'
        with open(filename, 'w') as f:
            f.write(json.dumps(data_to_json))


class diplom:
    '''
    This class work with extended functions for diplom module
    '''
    def __init__(self, file, file_rules):
        self.file = file
        self.file_rules = file_rules.strip()
        self.allCollumn = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT',
                           'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD']
        self.allRecord = parse.getAllRecord(self.allCollumn, self.file)
        #print("diplom:", self.allRecord)
        self.decode_data = self.get_rules(self.file_rules)

    def get_rules(self, name):
        with open(name, "r") as f:
             return json.load(f)

    def search_call_in_base(self, call):
        search_calls = []

        #records = parse.getAllRecord(self.allCollumn, self.file)
        record_count = len(self.allRecord)
        for record in range(record_count):
            if self.allRecord[record]['CALL'] == call:
                search_calls.append(self.allRecord[record])
                #print("AllRecords:_>", self.allRecord[record])
                #print("Search_call_in_base:_>", records[record])
        return search_calls

    def get_color_bg(self):
        color = QColor(int(self.decode_data[0]['colorR']),
                       int(self.decode_data[0]['colorG']),
                        int(self.decode_data[0]['colorB']))

        return color



    def filter (self, call_dict):
        flag = 'true'
        self.call = call_dict['call']
        #print("count_in_rules:_>",len(self.decode_data))
        for index_in_rules in range(len(self.decode_data)):
            #print("decode in filter", index_in_rules, " - ", self.decode_data[index_in_rules], "call", self.call)
            if call_dict['call'] == self.decode_data[index_in_rules]['call']:
                if call_dict['mode'] == 'cluster':
                    return True
                else:
                    found_records = self.search_call_in_base(self.call)
                    # 3 - not resolved
                    if str(self.decode_data[index_in_rules]['repeats']) == '3':
                        #print("Found Records:_>", found_records)
                        if not found_records:
                            return True
                            #flag = 'true'  #True
                            print("if not found_records", flag)
                        else:
                            print("else", flag)
                            flag = 'false' #False
                    # 0 - resolved other band
                    if str(self.decode_data[index_in_rules]['repeats']) == '0':
                        found_qso_count = len(found_records)
                        for i in range(found_qso_count):
                            if call_dict['band'] == found_records[i]['BAND']:
                                flag = 'false' # False

                    # 1 - resolved other mode
                    if str(self.decode_data[index_in_rules]['repeats']) == '1':
                        found_qso_count = len(found_records)
                        for i in range(found_qso_count):
                           if call_dict['mode'] == found_records[i]['MODE']:
                                flag = 'false'  # False

                    # 2 - resolved other mode and bands
                    if str(self.decode_data[index_in_rules]['repeats']) == '2':
                        found_qso_count = len(found_records)
                        for i in range(found_qso_count):
                            if call_dict['mode'] == found_records[i]['MODE'] or \
                                    call_dict['band'] == found_records[i]['BAND']:
                                flag = 'false'  # False
            else:
                print("else comparsion call", flag)
                flag = 'false'
        if flag == 'true':
            print("return", flag)
            return True

        if flag == 'false':
            print("return", flag)
            return False



    def add_qso(self, list_data):
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
        #print("List_data", list_data)
        index = len(list_data)
        with open(self.file, 'a') as file:


                stringToAdiFile = "<BAND:" + str(len(list_data['BAND'])) + ">" + list_data['BAND'] + "<CALL:" + \
                                  str(len(list_data['CALL'])) + ">"

                stringToAdiFile = stringToAdiFile + list_data['CALL'] + "<FREQ:" + str(
                    len(list_data['FREQ'])) + ">" + \
                                  list_data['FREQ']
                stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(list_data['MODE'])) + ">" + list_data[
                    'MODE'] + "<OPERATOR:" + str(len(list_data['OPERATOR']))
                stringToAdiFile = stringToAdiFile + ">" + list_data['OPERATOR'] + "<QSO_DATE:" + str(
                    len(list_data['QSO_DATE'])) + ">"
                stringToAdiFile = stringToAdiFile + list_data['QSO_DATE'] + "<TIME_ON:" + str(
                    len(list_data['TIME_ON'])) + ">"
                stringToAdiFile = stringToAdiFile + list_data['TIME_ON'] + "<RST_RCVD:" + \
                                  str(len(list_data['RST_RCVD'])) + ">" + list_data['RST_RCVD']
                stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(list_data['RST_SENT'])) + ">" + \
                                  list_data['RST_SENT'] + "<NAME:" + str(len(list_data['NAME'])) + ">" + \
                                  list_data['NAME'] + \
                                  "<QTH:" + str(len(list_data['QTH'])) + ">" + list_data['QTH'] + "<COMMENTS:" + \
                                  str(len(list_data['COMMENTS'])) + ">" + list_data['COMMENTS'] + "<TIME_OFF:" + \
                                  str(len(list_data['TIME_OFF'])) + ">" + list_data[
                                      'TIME_OFF'] + "<eQSL_QSL_RCVD:1>Y<EOR>\n"
                #print("string to ADI:", stringToAdiFile)
                file.write(stringToAdiFile)
                #print ("list_data:_>", list_data)
                self.allRecord.append(list_data)
    def get_count_qso(self):
        return len(self.allRecord)

    def get_all_qso(self):
        return self.allRecord

    def get_data(self):
        return self.decode_data

    def del_dilpom(self, name_diplom, settingsDict, logForm):
        self.settingsDict = settingsDict
        if self.settingsDict['diploms-json'] != '':
            list_string = json.loads(self.settingsDict['diploms-json'])
            #print(type(list_string))
            count_diploms = len(list_string)
            for i in range(count_diploms):
                if list_string[i]['name_programm'] == name_diplom:
                    del list_string[i]
            self.settingsDict['diploms-json'] = json.dumps(list_string)
            main.Settings_file.update_file_to_disk(self)


        print("del_dilpom", list_string)
        os.remove(name_diplom+'.rules')
        os.remove(name_diplom + '.adi')
        logForm.menu_rename_diplom()
        logForm.diploms_init()
        logForm.menu()

class static_diplom(QWidget):
    def __init__(self, diplom_name, settingsDict):
        super().__init__()
        self.diplom_name = diplom_name
        self.settingsDict = settingsDict
        self.initUI()
        self.update()

    def initUI(self):
        #self.setGeometry(300, 500, 500, 300)
        style = "QWidget{background-color:" + self.settingsDict['background-color'] + "; color:" + self.settingsDict[
            'color'] + ";}"
        styleform = "background :" + self.settingsDict['form-background'] + "; font-weight: 200;"
        self.setGeometry(int(self.settingsDict['diplom-statistic-window-left']), int(self.settingsDict['diplom-statistic-window-top']),
                         int(self.settingsDict['diplom-statistic-window-width']),
                         int(self.settingsDict['diplom-statistic-window-height']))

        self.setStyleSheet(style)
        self.setWindowTitle("Statistic diplom: " + str(self.diplom_name))

        self.score_final_label = QLabel()
        self.score_final_label.setStyleSheet("font-size: 12px;")
        self.score_total_label = QLabel()
        self.score_total_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.score_final_label)
        self.top_layout.addWidget(self.score_total_label)
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet(styleform)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.top_layout)
        self.vertical_layout.addWidget(self.table_widget)

        self.setLayout(self.vertical_layout)

    def update(self):
        self.all_column = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT',
                           'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD']
        self.rules = diplom.get_rules(diplom, self.diplom_name + '.rules')
        self.score_final_label.setText("Total score need: " + str(self.rules[0]['score_complite']))
        self.all_records = parse.getAllRecord(self.all_column, self.diplom_name+'.adi')
        records_count = len(self.all_records)
        column_count = len(self.all_column)
        self.table_widget.move(0, 0)
        fnt = self.table_widget.font()
        fnt.setPointSize(9)
        self.table_widget.setFont(fnt)
        self.table_widget.verticalHeader().hide()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setRowCount(records_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setHorizontalHeaderLabels(
            ["No", "   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
             "RST s", "      Name      ", "      QTH      ", " Comments ", " Time off ", " eQSL Rcvd "])
        for record in range(records_count):
            for column in range(column_count):
                self.table_widget.setItem(record, column,
                                      QTableWidgetItem(self.all_records[record][self.all_column[column]]))
        self.table_widget.resizeRowsToContents()
        self.table_widget.resizeColumnsToContents()
        total_score = 0
        for record in self.all_records:
            for i in range(len(self.rules)):
                if record['CALL'] == self.rules[i]['call'] and \
                        record['MODE'] == self.rules[i]['mode']:
                    total_score += int(self.rules[i]['score'])

        self.score_total_label.setText("Total score: " + str(total_score))









