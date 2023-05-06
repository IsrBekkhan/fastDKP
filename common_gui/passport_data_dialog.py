from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QProgressDialog, QLabel, QLineEdit, QPlainTextEdit, \
    QDateEdit, QPushButton, QFrame, QFileDialog, QProgressBar
from PyQt5.QtGui import QPixmap, QFont, QIntValidator, QCloseEvent, QDragEnterEvent, QDropEvent, QRegExpValidator
from PyQt5.QtCore import QRect, Qt, QMetaObject, QCoreApplication, QRegExp

from PIL import Image, UnidentifiedImageError

from os import path, getenv, remove
import sys
import traceback

from datetime import date, timedelta
from typing import Tuple, Dict, Union
from re import search

from api_interaction.recognize_request import AdsSoft
from utils.second_thread import SecondThread


class PassportDataUI(QDialog):

    def __init__(self, title: str, root_path: str, parent=None):
        super().__init__(parent=parent)
        self.__title = title
        self.__root_path = root_path

        self.__lbl_passport_monitor = None  # lbl - сокращение от label
        self.__lbl_passport_issued_department = None
        self.__lbl_passport_issued_date = None
        self.__lbl_department_number = None
        self.__lbl_department_number_div = None
        self.__lbl_passport_id = None
        self.__lbl_firstname = None
        self.__lbl_name = None
        self.__lbl_surname = None
        self.__lbl_date_of_birth = None
        self.__lbl_birth_place = None
        self.__lbl_registration_address = None
        self.__lbl_registration_address_note = None

        self.__le_department_number_start = None  # le - сокращение от lineEdit
        self.__le_department_number_end = None
        self.__le_passport_id_serial = None
        self.__le_passport_id_number = None
        self.__le_firstname = None
        self.__le_name = None
        self.__le_surname = None

        self.__pte_passport_issued_department = None  # pte - сокращение от PlainTextEdit
        self.__pte_birth_place = None
        self.__pte_registration_address = None

        self.__de_passport_issued_date = None  # de - сокращение от dateEdit
        self.__de_date_of_birth = None

        self.__btn_passport_path = None  # btn - сокращение от button
        self.__btn_clear_all = None
        self.__btn_recognize = None
        self.__btn_save = None
        self.__btn_cancel = None

        self.__vertical_line = None
        self.__horizontal_line = None
        self.__short_horizontal_line = None

        self.__clr_light_gray = 'background-color: rgb(230, 229, 237);'  # clr - сокращение от colour
        self.__clr_yellow = 'background-color: rgb(255, 245, 92);'

        self.__text_lines_tuple = None

        self.__passports_image_path = None
        self.__passport_data = None

    def setup_ui(self):
        self.setObjectName("passport_data_dialog")
        self.setFixedSize(826, 685)
        self.setStyleSheet("background-color: rgb(210, 225, 241);")
        self.setModal(True)
        self.setAcceptDrops(True)

        # окно для вывода изображения паспорта
        self.__lbl_passport_monitor = QLabel(self)
        self.__lbl_passport_monitor.setGeometry(QRect(2, 2, 410, 574))
        self.__lbl_passport_monitor.setObjectName("lbl_passport_monitor")
        self.__default_image_setter()

        # метка - паспорт выдан
        self.__lbl_passport_issued_department = QLabel(self)
        self.__lbl_passport_issued_department.setGeometry(QRect(440, 10, 121, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_passport_issued_department.setFont(font)
        self.__lbl_passport_issued_department.setObjectName("lbl_passport_issued_department")

        # метка - дата выдачи
        self.__lbl_passport_issued_date = QLabel(self)
        self.__lbl_passport_issued_date.setGeometry(QRect(440, 110, 91, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_passport_issued_date.setFont(font)
        self.__lbl_passport_issued_date.setObjectName("lbl_passport_issued_date")

        # метка - код подразделения
        self.__lbl_department_number = QLabel(self)
        self.__lbl_department_number.setGeometry(QRect(670, 110, 141, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_department_number.setFont(font)
        self.__lbl_department_number.setObjectName("lbl_issued_number")

        # метка - дефис в коде подразделения
        self.__lbl_department_number_div = QLabel(self)
        self.__lbl_department_number_div.setGeometry(QRect(743, 130, 16, 16))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.__lbl_department_number_div.setFont(font)
        self.__lbl_department_number_div.setObjectName("lbl_department_number_div")

        # метка - серия и номер паспорта
        self.__lbl_passport_id = QLabel(self)
        self.__lbl_passport_id.setGeometry(QRect(540, 210, 181, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_passport_id.setFont(font)
        self.__lbl_passport_id.setObjectName("lbl_passport_id")

        # метка - фамилия
        self.__lbl_firstname = QLabel(self)
        self.__lbl_firstname.setGeometry(QRect(440, 320, 81, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_firstname.setFont(font)
        self.__lbl_firstname.setObjectName("lbl_firstname")

        # метка - имя
        self.__lbl_name = QLabel(self)
        self.__lbl_name.setGeometry(QRect(440, 350, 81, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_name.setFont(font)
        self.__lbl_name.setObjectName("lbl_name")

        # метка - отчество
        self.__lbl_surname = QLabel(self)
        self.__lbl_surname.setGeometry(QRect(440, 380, 81, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_surname.setFont(font)
        self.__lbl_surname.setObjectName("lbl_surname")

        # метка - дата рождения
        self.__lbl_date_of_birth = QLabel(self)
        self.__lbl_date_of_birth.setGeometry(QRect(510, 410, 121, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_date_of_birth.setFont(font)
        self.__lbl_date_of_birth.setObjectName("lbl_date_of_birth")

        # метка - место рождения
        self.__lbl_birth_place = QLabel(self)
        self.__lbl_birth_place.setGeometry(QRect(440, 440, 141, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_birth_place.setFont(font)
        self.__lbl_birth_place.setObjectName("lbl_birth_place")

        # метка - место жительства
        self.__lbl_registration_address = QLabel(self)
        self.__lbl_registration_address.setGeometry(QRect(440, 510, 131, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_registration_address.setFont(font)
        self.__lbl_registration_address.setObjectName("lbl_registration_address")

        # метка - заполняется вручную
        self.__lbl_registration_address_note = QLabel(self)
        self.__lbl_registration_address_note.setGeometry(QRect(570, 512, 151, 16))
        self.__lbl_registration_address_note.setObjectName("lbl_registration_address_note")

        # строчное поле - код подразделения (начало)
        self.__le_department_number_start = QLineEdit(self)
        self.__le_department_number_start.setGeometry(QRect(700, 130, 41, 20))
        self.__le_department_number_start.setStyleSheet(self.__clr_light_gray)
        self.__le_department_number_start.setObjectName("le_issued_number_start")
        self.__le_department_number_start.setValidator(QIntValidator(100, 999, parent=self))
        self.__le_department_number_start.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # строчное поле - код подразделения (конец)
        self.__le_department_number_end = QLineEdit(self)
        self.__le_department_number_end.setGeometry(QRect(762, 130, 41, 20))
        self.__le_department_number_end.setStyleSheet(self.__clr_light_gray)
        self.__le_department_number_end.setObjectName("le_issued_number_end")
        self.__le_department_number_end.setValidator(QIntValidator(100, 999, parent=self))

        # строчное поле - серия паспорта
        self.__le_passport_id_serial = QLineEdit(self)
        self.__le_passport_id_serial.setGeometry(QRect(540, 230, 61, 20))
        self.__le_passport_id_serial.setStyleSheet(self.__clr_light_gray)
        self.__le_passport_id_serial.setObjectName("le_passport_id_serial")
        self.__le_passport_id_serial.setValidator(QIntValidator(1000, 9999, parent=self))
        self.__le_passport_id_serial.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # строчное поле - номер паспорта
        self.__le_passport_id_number = QLineEdit(self)
        self.__le_passport_id_number.setGeometry(QRect(610, 230, 101, 20))
        self.__le_passport_id_number.setStyleSheet(self.__clr_light_gray)
        self.__le_passport_id_number.setObjectName("le_passport_id_number")
        self.__le_passport_id_number.setValidator(QIntValidator(100000, 999999, parent=self))

        name_validator = QRegExpValidator(QRegExp(r'[а-яА-Я-]*'), parent=self)

        # строчное поле - фамилия
        self.__le_firstname = QLineEdit(self)
        self.__le_firstname.setGeometry(QRect(530, 320, 261, 20))
        self.__le_firstname.setStyleSheet(self.__clr_light_gray)
        self.__le_firstname.setObjectName("le_firstname")
        self.__le_firstname.setValidator(name_validator)

        # строчное поле - имя
        self.__le_name = QLineEdit(self)
        self.__le_name.setGeometry(QRect(530, 350, 261, 20))
        self.__le_name.setStyleSheet(self.__clr_light_gray)
        self.__le_name.setObjectName("le_name")
        self.__le_name.setValidator(name_validator)

        # строчное поле - отчество
        self.__le_surname = QLineEdit(self)
        self.__le_surname.setGeometry(QRect(530, 380, 261, 20))
        self.__le_surname.setStyleSheet(self.__clr_light_gray)
        self.__le_surname.setObjectName("le_surname")
        self.__le_surname.setValidator(name_validator)

        # текстовое поле - паспорт выдан
        self.__pte_passport_issued_department = QPlainTextEdit(self)
        self.__pte_passport_issued_department.setGeometry(QRect(440, 30, 361, 60))
        font = QFont()
        font.setPointSize(10)
        self.__pte_passport_issued_department.setFont(font)
        self.__pte_passport_issued_department.setStyleSheet(self.__clr_light_gray)
        self.__pte_passport_issued_department.setObjectName("te_passport_issued_department")
        self.__pte_passport_issued_department.setTabChangesFocus(True)
        self.__pte_passport_issued_department.setAcceptDrops(False)

        # текстовое поле - место рождения
        self.__pte_birth_place = QPlainTextEdit(self)
        self.__pte_birth_place.setGeometry(QRect(440, 460, 351, 45))
        font = QFont()
        font.setPointSize(10)
        self.__pte_birth_place.setFont(font)
        self.__pte_birth_place.setStyleSheet(self.__clr_light_gray)
        self.__pte_birth_place.setObjectName("te_birth_place")
        self.__pte_birth_place.setTabChangesFocus(True)
        self.__pte_birth_place.setAcceptDrops(False)

        # текстовое поле - место жительства
        self.__pte_registration_address = QPlainTextEdit(self)
        self.__pte_registration_address.setGeometry(QRect(440, 530, 351, 45))
        font = QFont()
        font.setPointSize(10)
        self.__pte_registration_address.setFont(font)
        self.__pte_registration_address.setStyleSheet(self.__clr_light_gray)
        self.__pte_registration_address.setObjectName("te_registration_address")
        self.__pte_registration_address.setTabChangesFocus(True)
        self.__pte_registration_address.setAcceptDrops(False)

        # дата - дата выдачи
        self.__de_passport_issued_date = QDateEdit(self)
        self.__de_passport_issued_date.setGeometry(QRect(440, 130, 110, 22))
        self.__de_passport_issued_date.setStyleSheet(self.__clr_light_gray)
        self.__de_passport_issued_date.setCalendarPopup(True)
        self.__de_passport_issued_date.setObjectName("de_passport_issued_date")
        self.__de_passport_issued_date.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.__de_passport_issued_date.setDate(date.today())

        # дата - дата рождения
        self.__de_date_of_birth = QDateEdit(self)
        self.__de_date_of_birth.setGeometry(QRect(631, 410, 110, 22))
        self.__de_date_of_birth.setStyleSheet(self.__clr_light_gray)
        self.__de_date_of_birth.setCalendarPopup(True)
        self.__de_date_of_birth.setObjectName("de_date_of_birth")
        self.__de_date_of_birth.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.__de_date_of_birth.setDate(date.today())

        # кнопка - указать путь к скану
        self.__btn_passport_path = QPushButton(self)
        self.__btn_passport_path.setGeometry(QRect(140, 590, 130, 30))
        font = QFont()
        font.setPointSize(9)
        self.__btn_passport_path.setFont(font)
        self.__btn_passport_path.setStyleSheet("background-color: rgb(202, 229, 255);")
        self.__btn_passport_path.setObjectName("btn_passport_path")

        # кнопка - очистить все
        self.__btn_clear_all = QPushButton(self)
        self.__btn_clear_all.setGeometry(QRect(430, 610, 101, 21))
        font = QFont()
        font.setPointSize(9)
        self.__btn_clear_all.setFont(font)
        self.__btn_clear_all.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.__btn_clear_all.setObjectName("btn_clear_all")

        # кнопка - распознать
        self.__btn_recognize = QPushButton(self)
        self.__btn_recognize.setGeometry(QRect(690, 610, 121, 23))
        font = QFont()
        font.setPointSize(9)
        self.__btn_recognize.setFont(font)
        self.__btn_recognize.setStyleSheet("background-color: rgb(202, 229, 255);")
        self.__btn_recognize.setObjectName("btn_recognize")

        # кнопка - сохранить
        self.__btn_save = QPushButton(self)
        self.__btn_save.setGeometry(QRect(710, 650, 101, 23))
        font = QFont()
        font.setPointSize(9)
        self.__btn_save.setFont(font)
        self.__btn_save.setStyleSheet("background-color: rgb(202, 255, 202);")
        self.__btn_save.setObjectName("btn_save")

        # кнопка - отмена
        self.__btn_cancel = QPushButton(self)
        self.__btn_cancel.setGeometry(QRect(430, 650, 75, 23))
        font = QFont()
        font.setPointSize(9)
        self.__btn_cancel.setFont(font)
        self.__btn_cancel.setStyleSheet("background-color: rgb(205, 205, 205);")
        self.__btn_cancel.setObjectName("btn_cancel")

        self.__text_lines_tuple = (self.__pte_passport_issued_department,
                                   self.__le_department_number_start,
                                   self.__le_department_number_end,
                                   self.__le_passport_id_serial,
                                   self.__le_passport_id_number,
                                   self.__le_firstname,
                                   self.__le_name,
                                   self.__le_surname,
                                   self.__pte_birth_place,
                                   self.__pte_registration_address)

        self.__vertical_line = QFrame(self)
        self.__vertical_line.setGeometry(QRect(414, 0, 2, 580))
        self.__vertical_line.setFrameShape(QFrame.VLine)
        self.__vertical_line.setFrameShadow(QFrame.Sunken)
        self.__vertical_line.setObjectName("vertical_line")

        self.__horizontal_line = QFrame(self)
        self.__horizontal_line.setGeometry(QRect(0, 578, 826, 2))
        self.__horizontal_line.setFrameShape(QFrame.HLine)
        self.__horizontal_line.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line.setObjectName("horizontal_line")

        self.__short_horizontal_line = QFrame(self)
        self.__short_horizontal_line.setGeometry(QRect(415, 295, 412, 2))
        self.__short_horizontal_line.setFrameShape(QFrame.HLine)
        self.__short_horizontal_line.setFrameShadow(QFrame.Sunken)
        self.__short_horizontal_line.setObjectName("horizontal_line")

        self.setTabOrder(self.__btn_passport_path, self.__pte_passport_issued_department)
        self.setTabOrder(self.__pte_passport_issued_department, self.__de_passport_issued_date)
        self.setTabOrder(self.__de_passport_issued_date, self.__le_department_number_start)
        self.setTabOrder(self.__le_department_number_start, self.__le_department_number_end)
        self.setTabOrder(self.__le_department_number_end, self.__le_passport_id_serial)
        self.setTabOrder(self.__le_passport_id_serial, self.__le_passport_id_number)
        self.setTabOrder(self.__le_passport_id_number, self.__le_firstname)
        self.setTabOrder(self.__le_firstname, self.__le_name)
        self.setTabOrder(self.__le_name, self.__le_surname)
        self.setTabOrder(self.__le_surname, self.__de_date_of_birth)
        self.setTabOrder(self.__de_date_of_birth, self.__pte_birth_place)
        self.setTabOrder(self.__pte_birth_place, self.__pte_registration_address)
        self.setTabOrder(self.__pte_registration_address, self.__btn_recognize)
        self.setTabOrder(self.__btn_recognize, self.__btn_save)
        self.setTabOrder(self.__btn_save, self.__btn_clear_all)
        self.setTabOrder(self.__btn_clear_all, self.__btn_cancel)

        self.__re_translate_ui()
        QMetaObject.connectSlotsByName(self)

        self.__btn_actions()

    def __re_translate_ui(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("passport_data_dialog", self.__title))

        self.__lbl_passport_issued_department.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Паспорт выдан</span></p></body></html>"
        ))
        self.__lbl_passport_issued_date.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Дата выдачи</span></p></body></html>"
        ))
        self.__lbl_department_number.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Код подразделения</span></p></body></html>"
        ))
        self.__lbl_department_number_div.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p align=\"center\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10.5pt;"
            " color:#6e7173;\">–</span></p></body></html>"
        ))
        self.__lbl_passport_id.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Серия и номер пасспорта</span></p></body></html>"
        ))
        self.__lbl_firstname.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Фамилия</span></p></body></html>"
        ))
        self.__lbl_name.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Имя</span></p></body></html>"
        ))
        self.__lbl_surname.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Отчество</span></p></body></html>"
        ))
        self.__lbl_date_of_birth.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Дата рождения</span></p></body></html>"
        ))
        self.__lbl_birth_place.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Место рождения</span></p></body></html>"
        ))
        self.__lbl_registration_address.setText(_translate(
            "passport_data_dialog",
            "<html><head/><body><p><span style=\" color:#7d3e46;\">Место жительства</span></p></body></html>"
        ))
        self.__lbl_registration_address_note.setText(_translate("passport_data_dialog", "(заполняется вручную)"))

        self.__btn_passport_path.setText(_translate("passport_data_dialog", "Выбрать фото"))
        self.__btn_clear_all.setText(_translate("passport_data_dialog", "Очистить всё"))
        self.__btn_recognize.setText(_translate("passport_data_dialog", "Распознать"))
        self.__btn_save.setText(_translate("passport_data_dialog", "Сохранить"))
        self.__btn_cancel.setText(_translate("passport_data_dialog", "Отмена"))

    def __default_image_setter(self):
        default_image_path = path.join(self.__root_path, 'icons', 'passport_sketch.png')
        self.__lbl_passport_monitor.setPixmap(QPixmap(default_image_path))

    def __btn_actions(self):
        self.__btn_passport_path.clicked.connect(self.__passport_path_setter)
        self.__btn_recognize.clicked.connect(self.__recognize_starter)
        self.__btn_clear_all.clicked.connect(self.__all_lines_cleaner)
        self.__btn_cancel.clicked.connect(self.close)
        self.__btn_save.clicked.connect(self.__passport_data_saver)

    def __passport_path_setter(self):
        desktop_path = path.join(getenv("userprofile"), "Desktop")
        passport_path, file_extension = QFileDialog.getOpenFileName(
            QDialog(parent=self),
            caption='Выбор скана пасспорта',
            directory=desktop_path,
            filter='изображения (*.jpg *.jpeg *.bmp *.jp2 *.png)'
        )
        if passport_path:
            self.__image_display(passport_path)

    def dragEnterEvent(self, drag_enter: QDragEnterEvent) -> None:
        if drag_enter.mimeData().hasUrls():
            urls_list = drag_enter.mimeData().urls()
            if len(urls_list) == 1:
                url = urls_list[0].toLocalFile()
                if url.endswith(('.jpg', '.jpeg', '.bmp', '.jp2', '.png')):
                    drag_enter.accept()
        else:
            drag_enter.ignore()

    def dropEvent(self, drop_inside: QDropEvent) -> None:
        passport_path = drop_inside.mimeData().urls()[0].toLocalFile()
        self.__image_display(passport_path)

    def __image_display(self, passport_path):
        try:
            passport_image = Image.open(passport_path)
        except (UnidentifiedImageError, FileNotFoundError, AttributeError, PermissionError, OSError):
            self.__default_image_setter()
            self.passports_image_path = None
        else:
            resized_passports_image = passport_image.resize(size=(410, 574))
            temp_img_name = path.join(self.__root_path, 'temp', 'temp.jpg')
            sys.excepthook = self.__exception_hook

            try:
                resized_passports_image.save(temp_img_name)
            except OSError:
                error_message = 'Данный формат изображения не поддерживается'
                self.__error_message_display(error_message)
                self.passports_image_path = None
            else:
                self.__lbl_passport_monitor.setPixmap(QPixmap(temp_img_name))
                self.__passports_image_path = passport_path
                remove(temp_img_name)

    @staticmethod
    def __exception_hook(type_, value, tb):
        traceback.format_exception(type_)

    @staticmethod
    def __error_message_display(error_message):
        dlg_error_message = QMessageBox()
        dlg_error_message.setWindowTitle('Сообщение об ошибке')
        dlg_error_message.setText(error_message)
        dlg_error_message.setIcon(QMessageBox.Critical)
        dlg_error_message.addButton('Ок', QMessageBox.YesRole)
        dlg_error_message.exec_()

    def __recognize_starter(self):

        if self.__passports_image_path:

            if self.__is_all_lines_clean():
                self.__passports_image_recognizer()

            else:
                dlg_you_sure = QMessageBox()
                dlg_you_sure.setWindowTitle('Внимание')
                dlg_you_sure.setText('Все заполненные поля будут перезаписаны\nПродолжить?')
                dlg_you_sure.setIcon(QMessageBox.Warning)
                btn_yes = dlg_you_sure.addButton('Да', QMessageBox.YesRole)
                btn_cancel = dlg_you_sure.addButton('Отмена', QMessageBox.RejectRole)
                btn_cancel.setDefault(True)
                dlg_you_sure.exec_()

                if dlg_you_sure.clickedButton() == btn_yes:
                    self.__text_cleaner()
                    self.__colour_setter()
                    self.__passports_image_recognizer()

        else:
            dlg_error_message = QMessageBox()
            dlg_error_message.setWindowTitle('Внимание!')
            dlg_error_message.setText('Сначала выберите фотографию пасспорта')
            dlg_error_message.setIcon(QMessageBox.Warning)
            dlg_error_message.addButton('Ок', QMessageBox.YesRole)
            dlg_error_message.exec_()

    def __passports_image_recognizer(self):
        self.__second_thread = SecondThread(AdsSoft.image_recognizer, self.__passports_image_path)
        self.__progress_dlg_setter()
        self.__second_thread.my_signal.connect(self.__progress_dlg_display, Qt.QueuedConnection)
        self.__second_thread.start()

    def __progress_dlg_setter(self):
        self.__progress_dialog = QProgressDialog('Подождите несколько секунд...', None,
                                                 0, 0, parent=self)
        self.__progress_dialog.setWindowFlags(Qt.Window |
                                              Qt.CustomizeWindowHint |
                                              Qt.MSWindowsFixedSizeDialogHint)
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)
        progress_bar.setInvertedAppearance(True)

        self.__progress_dialog.setBar(progress_bar)
        self.__progress_dialog.setModal(True)

    def __progress_dlg_display(self, signal):
        if signal == 'start':
            self.__progress_dialog.show()
        elif signal == 'finish':
            self.__progress_dialog.close()
            if self.__second_thread.response:
                self.__response_handler(self.__second_thread.response)

    def __response_handler(self, response):

        if isinstance(response, dict):
            passport_data = AdsSoft.passport_data_getter(deserialized_response=response)

            if isinstance(passport_data, dict):
                self.__passport_data_display(passport_data)

            elif isinstance(passport_data, str):
                self.__error_message_display(passport_data)

        elif isinstance(response, str):
            self.__error_message_display(response)

    def __passport_data_display(self, passport_data: Dict):

        # проверка 'пасспорт выдан'
        passport_issued_department = passport_data.get('passport_issued_department')

        if passport_issued_department:
            self.__pte_passport_issued_department.setPlainText(passport_issued_department)
        else:
            self.__pte_passport_issued_department.setStyleSheet(self.__clr_yellow)

        # проверка даты выдачи
        issued_date_temp = passport_data.get('passport_issued_date')

        if issued_date_temp:
            issued_date_list = issued_date_temp.split('-')

            try:
                issued_date = date(day=int(issued_date_list[2]),
                                   month=int(issued_date_list[1]),
                                   year=int(issued_date_list[0]))
            except ValueError:
                self.__de_passport_issued_date.setStyleSheet(self.__clr_yellow)
            else:
                self.__de_passport_issued_date.setDate(issued_date)
        else:
            self.__de_passport_issued_date.setStyleSheet(self.__clr_yellow)

        # проверка кода подразделения
        department_number = passport_data.get('issued_number')

        if department_number:
            department_number_list = department_number.split('-')

            if self.__department_number_checker(department_number_list[0]):
                self.__le_department_number_start.setText(department_number_list[0])
            else:
                self.__le_department_number_start.setStyleSheet(self.__clr_yellow)

            if self.__department_number_checker(department_number_list[1]):
                self.__le_department_number_end.setText(department_number_list[1])
            else:
                self.__le_department_number_end.setStyleSheet(self.__clr_yellow)

        else:
            self.__le_department_number_start.setStyleSheet(self.__clr_yellow)
            self.__le_department_number_end.setStyleSheet(self.__clr_yellow)

        # проверка серии и номера пасспорта
        passport_id_temp = passport_data.get('passport_id')

        if passport_id_temp:
            passport_id = passport_id_temp.split()

            if self.__passport_serial_checker(passport_id[0]):
                self.__le_passport_id_serial.setText(passport_id[0])
            else:
                self.__le_passport_id_serial.setStyleSheet(self.__clr_yellow)

            if self.__passport_number_checker(passport_id[1]):
                self.__le_passport_id_number.setText(passport_id[1])
            else:
                self.__le_passport_id_number.setStyleSheet(self.__clr_yellow)

        else:
            self.__le_passport_id_serial.setStyleSheet(self.__clr_yellow)
            self.__le_passport_id_number.setStyleSheet(self.__clr_yellow)

        # проверка фамилии
        first_name = passport_data.get('firstname')

        if first_name:

            if self.__str_lines_checker(first_name):
                self.__le_firstname.setText(first_name)
            else:
                self.__le_firstname.setStyleSheet(self.__clr_yellow)

        else:
            self.__le_firstname.setStyleSheet(self.__clr_yellow)

        # проверка имени
        name = passport_data.get('name')

        if name:
            if self.__str_lines_checker(name):
                self.__le_name.setText(name)
            else:
                self.__le_name.setStyleSheet(self.__clr_yellow)

        else:
            self.__le_name.setStyleSheet(self.__clr_yellow)

        # проверка отчества
        surname = passport_data.get('surname')

        if surname:

            if self.__str_lines_checker(surname):
                self.__le_surname.setText(surname)
            else:
                self.__le_surname.setStyleSheet(self.__clr_yellow)

        else:
            self.__le_surname.setStyleSheet(self.__clr_yellow)

        # проверка даты рождения
        date_of_birth_temp = passport_data.get('date_of_birth')

        if date_of_birth_temp:
            date_of_birth_list = date_of_birth_temp.split('-')
            try:
                date_of_birth = date(day=int(date_of_birth_list[2]),
                                     month=int(date_of_birth_list[1]),
                                     year=int(date_of_birth_list[0]))
            except ValueError:
                self.__de_date_of_birth.setStyleSheet(self.__clr_yellow)
            else:
                self.__de_date_of_birth.setDate(date_of_birth)

        else:
            self.__de_date_of_birth.setStyleSheet(self.__clr_yellow)

        # проверка 'место рождения'
        birth_place = passport_data.get('birth_place')

        if birth_place:
            self.__pte_birth_place.setPlainText(birth_place)
        else:
            self.__pte_birth_place.setStyleSheet(self.__clr_yellow)

    @staticmethod
    def __department_number_checker(int_value: str) -> bool:
        if int_value.isdigit():
            if int(int_value) < 1000:
                if len(int_value) == 3:
                    return True
        return False

    @staticmethod
    def __passport_serial_checker(int_value: str) -> bool:
        if int_value.isdigit():
            if int(int_value) < 10000:
                if len(int_value) == 4:
                    return True
        return False

    @staticmethod
    def __passport_number_checker(int_value: str) -> bool:
        if int_value.isdigit():
            if int(int_value) < 1000000:
                if len(int_value) == 6:
                    return True
        return False

    @staticmethod
    def __str_lines_checker(str_value: str) -> bool:

        if len(str_value) != 0:
            check_result = search(r'[а-яА-Я- ]*', str_value)

            if check_result.group(0) == str_value:
                return True
            return False

        return False

    def __passport_data_saver(self):
        is_all_right = True

        text_edit_list = [self.__pte_passport_issued_department,
                          self.__pte_birth_place,
                          self.__pte_registration_address]

        str_line_edit_list = [self.__le_firstname,
                              self.__le_name,
                              self.__le_surname]

        int_line_edit_list = [self.__le_department_number_start,
                              self.__le_department_number_end,
                              self.__le_passport_id_serial,
                              self.__le_passport_id_number]

        passport_issued_date_tuple = self.__de_passport_issued_date.date().getDate()
        passport_issued_date = date(day=passport_issued_date_tuple[2],
                                    month=passport_issued_date_tuple[1],
                                    year=passport_issued_date_tuple[0])
        date_of_birth_tuple = self.__de_date_of_birth.date().getDate()
        date_of_birth = date(day=date_of_birth_tuple[2],
                             month=date_of_birth_tuple[1],
                             year=date_of_birth_tuple[0])

        if passport_issued_date > date.today():
            self.__de_passport_issued_date.setStyleSheet(self.__clr_yellow)
            is_all_right = False
        else:
            self.__de_passport_issued_date.setStyleSheet(self.__clr_light_gray)

        if date_of_birth > date.today() - timedelta(days=6574):
            self.__de_date_of_birth.setStyleSheet(self.__clr_yellow)
            is_all_right = False
        else:
            self.__de_date_of_birth.setStyleSheet(self.__clr_light_gray)

        for text_edit in text_edit_list:
            if len(text_edit.toPlainText()) < 9:
                text_edit.setStyleSheet(self.__clr_yellow)
                is_all_right = False
            else:
                text_edit.setStyleSheet(self.__clr_light_gray)

        for line_edit in str_line_edit_list:

            if not self.__str_lines_checker(line_edit.text()):
                line_edit.setStyleSheet(self.__clr_yellow)
                is_all_right = False
            else:
                line_edit.setStyleSheet(self.__clr_light_gray)

        for line_edit in int_line_edit_list:
            if not line_edit.text().isdigit():
                line_edit.setStyleSheet(self.__clr_yellow)
                is_all_right = False
            else:
                line_edit.setStyleSheet(self.__clr_light_gray)

        department_number = '-'.join((str(self.__le_department_number_start.text()),
                                      str(self.__le_department_number_end.text())))

        if is_all_right:
            passport_id = ''.join((self.__le_passport_id_serial.text(),
                                   ' №',
                                   self.__le_passport_id_number.text()))

            self.__passport_data = {
                'passport_issued_department': self.__pte_passport_issued_department.toPlainText(),
                'passport_issued_date': self.__date_tuple_to_str(self.__de_passport_issued_date.date().getDate()),
                'department_number': department_number,
                'passport_id': passport_id,
                'firstname': self.__le_firstname.text().title(),
                'name': self.__le_name.text().title(),
                'surname': self.__le_surname.text().title(),
                'date_of_birth': self.__date_tuple_to_str(self.__de_date_of_birth.date().getDate()),
                'birth_place': self.__pte_birth_place.toPlainText(),
                'registration_address': self.__pte_registration_address.toPlainText()
            }

            self.close()

    def __all_lines_cleaner(self):

        if not self.__is_all_lines_clean():
            dlg_you_sure = QMessageBox()
            dlg_you_sure.setWindowTitle('Очистить все поля')
            dlg_you_sure.setText('Вы уверены?')
            dlg_you_sure.setIcon(QMessageBox.Warning)
            btn_yes = dlg_you_sure.addButton('Да', QMessageBox.YesRole)
            btn_cancel = dlg_you_sure.addButton('Отмена', QMessageBox.RejectRole)
            btn_cancel.setDefault(True)
            dlg_you_sure.exec_()

            if dlg_you_sure.clickedButton() == btn_yes:
                self.__text_cleaner()
                self.__colour_setter()

        else:
            self.__colour_setter()

    def __text_cleaner(self):

        for line in self.__text_lines_tuple:
            line.clear()

        self.__de_passport_issued_date.setDate(date.today())
        self.__de_date_of_birth.setDate(date.today())

    def __colour_setter(self):

        for line in self.__text_lines_tuple:
            line.setStyleSheet(self.__clr_light_gray)

        self.__de_passport_issued_date.setStyleSheet(self.__clr_light_gray)
        self.__de_date_of_birth.setStyleSheet(self.__clr_light_gray)

    def __is_all_lines_clean(self):
        issued_date_tuple = self.__de_passport_issued_date.date().getDate()
        issued_date = date(day=issued_date_tuple[2],
                           month=issued_date_tuple[1],
                           year=issued_date_tuple[0])

        date_of_birth_tuple = self.__de_date_of_birth.date().getDate()
        date_of_birth = date(day=date_of_birth_tuple[2],
                             month=date_of_birth_tuple[1],
                             year=date_of_birth_tuple[0])

        is_all_lines_clean = (len(self.__pte_passport_issued_department.toPlainText()) == 0,
                              len(self.__le_department_number_start.text()) == 0,
                              len(self.__le_department_number_end.text()) == 0,
                              len(self.__le_passport_id_serial.text()) == 0,
                              len(self.__le_passport_id_number.text()) == 0,
                              len(self.__le_firstname.text()) == 0,
                              len(self.__le_name.text()) == 0,
                              len(self.__le_surname.text()) == 0,
                              len(self.__pte_birth_place.toPlainText()) == 0,
                              len(self.__pte_registration_address.toPlainText()) == 0,
                              issued_date >= date.today(),
                              date_of_birth >= date.today())

        if all(is_all_lines_clean):
            return True

        return False

    def closeEvent(self, close_event: QCloseEvent) -> None:
        if not isinstance(self.__passport_data, dict):
            if not self.__is_all_lines_clean():
                dlg_you_sure = QMessageBox()
                dlg_you_sure.setWindowTitle('Отмена операции')
                dlg_you_sure.setText('Внимание! Вы потеряете введенные данные.\nВы точно хотите закрыть окно?')
                dlg_you_sure.setIcon(QMessageBox.Warning)
                btn_yes = dlg_you_sure.addButton('Да', QMessageBox.YesRole)
                btn_cancel = dlg_you_sure.addButton('Отмена', QMessageBox.RejectRole)
                btn_cancel.setDefault(True)
                dlg_you_sure.exec_()

                if dlg_you_sure.clickedButton() == btn_cancel:
                    close_event.ignore()
            else:
                close_event.accept()
        else:
            close_event.accept()

    @staticmethod
    def __date_tuple_to_str(date_tuple: Tuple) -> str:

        if date_tuple[1] < 10:
            month = '0{}'.format(str(date_tuple[1]))
        else:
            month = str(date_tuple[1])

        return '.'.join((str(date_tuple[2]), month, str(date_tuple[0])))

    @property
    def passport_data(self) -> Union[Dict, bool]:
        if self.__passport_data:
            return self.__passport_data
        return False


if __name__ == "__main__":
    root_path_ = path.abspath('..')

    app = QApplication(sys.argv)
    dlg_passport_data = PassportDataUI(title='Данные покупателя', root_path=root_path_)
    dlg_passport_data.setup_ui()
    dlg_passport_data.show()
    sys.exit(app.exec_())



