from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QDateEdit, \
    QDateTimeEdit, QFrame, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt, QMetaObject, QCoreApplication

from datetime import date, datetime
from os import path, getenv
import sys
from json import load
from typing import Tuple, Dict

from common_gui.passport_data_dialog import PassportDataUI
from common_gui.real_estate_data_dialog import RealEstateDataUi
from common_gui.settings_dialog import SettingsDialog
from common_gui.about_dialog import AboutDialog
from utils.contract_maker import contract_maker

from api_interaction.recognize_request import AdsSoft
from api_interaction.egrn_request import ApiEGRN


class MainWindowUI(QMainWindow):

    def __init__(self, root_path: str):
        super().__init__()
        self.__root_path = root_path

        self.__central_widget = None
        self.__menubar = None
        self.__menu = None
        self.__settings = None
        self.__about = None

        self.__lbl_sellers_full_name = None
        self.__lbl_buyers_full_name = None
        self.__lbl_contract_location = None
        self.__lbl_cadastral_number = None
        self.__lbl_contract_date = None
        self.__lbl_save_path = None

        self.__btn_sellers_data = None
        self.__btn_buyers_data = None
        self.__btn_real_estates_data = None
        self.__btn_save_path = None
        self.__btn_make_contract = None

        self.__le_contract_location = None
        self.__de_contract_date = None
        self.__le_save_path = None

        self.__horizontal_line_1 = None
        self.__horizontal_line_2 = None
        self.__horizontal_line_3 = None

        self.__sellers_data = None
        self.__buyers_data = None
        self.__real_estate_data = None

        self.__clr_yellow = 'background-color: rgb(255, 245, 92);'

    def setup_ui(self):
        self.setObjectName("easyDKP")
        self.setFixedSize(350, 550)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.__central_widget = QWidget(self)
        self.__central_widget.setStyleSheet("")
        self.__central_widget.setObjectName("central_widget")

        self.__lbl_sellers_full_name = QLabel(self.__central_widget)
        self.__lbl_sellers_full_name.setGeometry(QRect(0, 40, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_sellers_full_name.setFont(font)
        self.__lbl_sellers_full_name.setText('Продавец:')
        self.__lbl_sellers_full_name.setObjectName("lbl_sellers_full_name")

        self.__lbl_buyers_full_name = QLabel(self.__central_widget)
        self.__lbl_buyers_full_name.setGeometry(QRect(0, 130, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_buyers_full_name.setFont(font)
        self.__lbl_buyers_full_name.setText('Покупатель:')
        self.__lbl_buyers_full_name.setObjectName("lbl_buyers_full_name")

        self.__lbl_cadastral_number = QLabel(self.__central_widget)
        self.__lbl_cadastral_number.setGeometry(QRect(0, 220, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_cadastral_number.setFont(font)
        self.__lbl_cadastral_number.setText('Кадастровый номер:')
        self.__lbl_cadastral_number.setObjectName("lbl_cadastral_number")

        self.__lbl_contract_location = QLabel(self.__central_widget)
        self.__lbl_contract_location.setGeometry(QRect(40, 300, 171, 21))
        font = QFont()
        font.setPointSize(10)
        self.__lbl_contract_location.setFont(font)
        self.__lbl_contract_location.setObjectName("lbl_contract_location")

        self.__lbl_contract_date = QLabel(self.__central_widget)
        self.__lbl_contract_date.setGeometry(QRect(40, 350, 171, 21))
        font = QFont()
        font.setPointSize(10)
        self.__lbl_contract_date.setFont(font)
        self.__lbl_contract_date.setObjectName("lbl_contract_date")

        self.__lbl_save_path = QLabel(self.__central_widget)
        self.__lbl_save_path.setGeometry(QRect(40, 410, 171, 21))
        font = QFont()
        font.setPointSize(10)
        self.__lbl_save_path.setFont(font)
        self.__lbl_save_path.setObjectName("lbl_save_path")

        self.__btn_sellers_data = QPushButton(self.__central_widget)
        self.__btn_sellers_data.setGeometry(QRect(0, 0, 350, 30))
        font = QFont()
        font.setPointSize(10)
        self.__btn_sellers_data.setFont(font)
        self.__btn_sellers_data.setObjectName("btn_sellers_data")

        self.__btn_buyers_data = QPushButton(self.__central_widget)
        self.__btn_buyers_data.setGeometry(QRect(0, 89, 350, 30))
        font = QFont()
        font.setPointSize(10)
        self.__btn_buyers_data.setFont(font)
        self.__btn_buyers_data.setObjectName("btn_buyers_data")

        self.__btn_real_estates_data = QPushButton(self.__central_widget)
        self.__btn_real_estates_data.setGeometry(QRect(0, 180, 350, 30))
        font = QFont()
        font.setPointSize(10)
        self.__btn_real_estates_data.setFont(font)
        self.__btn_real_estates_data.setObjectName("btn_real_estates_data")

        self.__btn_save_path = QPushButton(self.__central_widget)
        self.__btn_save_path.setGeometry(QRect(264, 430, 61, 20))
        font = QFont()
        font.setPointSize(10)
        self.__btn_save_path.setFont(font)
        self.__btn_save_path.setObjectName("btn_save_path")

        self.__btn_make_contract = QPushButton(self.__central_widget)
        self.__btn_make_contract.setGeometry(QRect(110, 480, 151, 31))
        self.__btn_make_contract.setObjectName("btn_make_contract")

        self.__le_contract_location = QLineEdit(self.__central_widget)
        self.__le_contract_location.setGeometry(QRect(40, 320, 281, 20))
        self.__le_contract_location.setObjectName("le_contract_location")

        self.__de_contract_date = QDateEdit(self.__central_widget)
        self.__de_contract_date.setGeometry(QRect(40, 370, 110, 22))
        self.__de_contract_date.setLayoutDirection(Qt.LeftToRight)
        self.__de_contract_date.setCurrentSection(QDateTimeEdit.DaySection)
        self.__de_contract_date.setCalendarPopup(True)
        self.__de_contract_date.setObjectName("de_contract_date")
        self.__de_contract_date.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.__de_contract_date.setDate(date.today())

        self.__le_save_path = QLineEdit(self.__central_widget)
        self.__le_save_path.setGeometry(QRect(40, 430, 221, 20))
        self.__le_save_path.setObjectName("le_save_path")

        self.__horizontal_line_1 = QFrame(self.__central_widget)
        self.__horizontal_line_1.setGeometry(QRect(0, 70, 351, 16))
        self.__horizontal_line_1.setFrameShape(QFrame.HLine)
        self.__horizontal_line_1.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_1.setObjectName("horizontal_line_1")

        self.__horizontal_line_3 = QFrame(self.__central_widget)
        self.__horizontal_line_3.setGeometry(QRect(0, 260, 351, 16))
        self.__horizontal_line_3.setFrameShape(QFrame.HLine)
        self.__horizontal_line_3.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_3.setObjectName("horizontal_line_3")

        self.__horizontal_line_2 = QFrame(self.__central_widget)
        self.__horizontal_line_2.setGeometry(QRect(0, 160, 351, 16))
        self.__horizontal_line_2.setFrameShape(QFrame.HLine)
        self.__horizontal_line_2.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_2.setObjectName("horizontal_line_2")

        self.setTabOrder(self.__btn_sellers_data, self.__btn_buyers_data)
        self.setTabOrder(self.__btn_buyers_data, self.__btn_real_estates_data)
        self.setTabOrder(self.__btn_real_estates_data, self.__le_contract_location)
        self.setTabOrder(self.__le_contract_location, self.__de_contract_date)
        self.setTabOrder(self.__de_contract_date, self.__le_save_path)
        self.setTabOrder(self.__le_save_path, self.__btn_save_path)
        self.setTabOrder(self.__btn_save_path, self.__btn_make_contract)

        self.setCentralWidget(self.__central_widget)

        self.__menubar = QMenuBar(self)
        self.__menubar.setGeometry(QRect(0, 0, 350, 21))
        self.__menubar.setObjectName("menubar")

        self.__menu = QMenu(self.__menubar)
        self.__menu.setObjectName("menu")

        self.setMenuBar(self.__menubar)

        self.__settings = QAction(self)
        self.__settings.setObjectName("settings")

        self.__about = QAction(self)
        self.__about.setObjectName("about")

        self.__menu.addAction(self.__settings)
        self.__menu.addAction(self.__about)

        self.__menubar.addAction(self.__menu.menuAction())

        self.__re_translate_ui()
        QMetaObject.connectSlotsByName(self)

        self.__settings_checker()
        self.__btn_actions()

    def __re_translate_ui(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("easyDKP", "easyDKP"))

        self.__lbl_contract_location.setText(_translate("easyDKP", "место заключения договора"))
        self.__lbl_contract_date.setText(_translate("easyDKP", "дата заключения договора"))
        self.__lbl_save_path.setText(_translate("easyDKP", "сохранить в:"))

        self.__btn_sellers_data.setText(_translate("easyDKP", "Данные продавца"))
        self.__btn_buyers_data.setText(_translate("easyDKP", "Данные покупателя"))
        self.__btn_real_estates_data.setText(_translate("easyDKP", "Данные объекта недвижимости"))
        self.__btn_save_path.setText(_translate("easyDKP", "изменить"))
        self.__btn_make_contract.setText(_translate("easyDKP", "Сохранить договор"))

        self.__menu.setTitle(_translate("easyDKP", "Меню"))
        self.__settings.setText(_translate("easyDKP", "Настройки"))
        self.__about.setText(_translate("easyDKP", "О программе"))

    def __settings_checker(self):
        config_data_path = path.join(self.__root_path, 'config_data', 'config_data.json')

        if not path.exists(config_data_path):
            self.__settings_setter()

        if path.exists(config_data_path):
            self.__settings_getter(config_data_path)
        else:
            sys.exit()

    def __settings_setter(self):
        settings_dialog = SettingsDialog(root_path=self.__root_path)
        settings_dialog.setup_ui()
        settings_dialog.show()
        settings_dialog.exec()

    def __settings_getter(self, config_data_path: str):

        with open(config_data_path, 'r', encoding='utf-8') as config_data_file:
            config_data = load(config_data_file)

            AdsSoft.ads_token_setter(config_data['ads_token'])
            AdsSoft.ads_url_setter(config_data['ads_url'])

            ApiEGRN.token_setter(config_data['api_egrn_token'])
            ApiEGRN.host_setter(config_data['api_egrn_host'])
            ApiEGRN.url_setter(config_data['api_egrn_url'])

            self.__le_contract_location.setText(config_data['contract_location'])
            self.__le_save_path.setText(config_data['save_path'])

    def __btn_actions(self):
        self.__btn_sellers_data.clicked.connect(self.__dlg_sellers_data)
        self.__btn_buyers_data.clicked.connect(self.__dlg_buyers_data)
        self.__btn_real_estates_data.clicked.connect(self.__dlg_real_estate_data)
        self.__btn_save_path.clicked.connect(self.__save_path_setter)
        self.__btn_make_contract.clicked.connect(self.__data_checker)

        self.__about.triggered.connect(self.__about_dlg)
        self.__settings.triggered.connect(self.__settings_dlg)

    def __dlg_sellers_data(self):
        dlg_sellers_data = PassportDataUI(title='Данные продавца', root_path=self.__root_path, parent=self)
        dlg_sellers_data.setup_ui()
        dlg_sellers_data.show()
        dlg_sellers_data.exec()

        if dlg_sellers_data.passport_data:
            self.__sellers_data = dlg_sellers_data.passport_data
            lbl_text = ' '.join((
                'Продавец:',
                self.__sellers_data['firstname'],
                self.__sellers_data['name']
            ))
            self.__lbl_sellers_full_name.setText(lbl_text)

    def __dlg_buyers_data(self):
        dlg_buyers_data = PassportDataUI(title='Данные покупателя', root_path=self.__root_path, parent=self)
        dlg_buyers_data.setup_ui()
        dlg_buyers_data.show()
        dlg_buyers_data.exec()

        if dlg_buyers_data.passport_data:
            self.__buyers_data = dlg_buyers_data.passport_data
            lbl_text = ' '.join((
                'Покупатель:',
                self.__buyers_data['firstname'],
                self.__buyers_data['name']
            ))
            self.__lbl_buyers_full_name.setText(lbl_text)

    def __dlg_real_estate_data(self):
        dlg_real_estate_data = RealEstateDataUi(title='Данные недвижимости', parent=self)
        dlg_real_estate_data.setup_ui()
        dlg_real_estate_data.show()
        dlg_real_estate_data.exec()

        if dlg_real_estate_data.real_estate_data:
            self.__real_estate_data = dlg_real_estate_data.real_estate_data
            lbl_text = ' '.join((
                'Кадастровый номер:',
                self.__real_estate_data['cadastral_number']
            ))
            self.__lbl_cadastral_number.setText(lbl_text)

    def __data_checker(self):

        if self.__sellers_data:

            if self.__buyers_data:

                if self.__real_estate_data:

                    if len(self.__le_contract_location.text()) != 0:
                        self.__contract_maker()

                    else:
                        self.__le_contract_location.setStyleSheet(self.__clr_yellow)

                else:
                    self.__error_message_display('Сначала заполните данные объекта недвижимости')

            else:
                self.__error_message_display('Сначала заполните данные покупателя')

        else:
            self.__error_message_display('Сначала заполните данные продавца')

    @staticmethod
    def __error_message_display(error_message):
        dlg_error_message = QMessageBox()
        dlg_error_message.setWindowTitle('Внимание')
        dlg_error_message.setText(error_message)
        dlg_error_message.setIcon(QMessageBox.Warning)
        dlg_error_message.addButton('Ок', QMessageBox.YesRole)
        dlg_error_message.exec_()

    def __save_path_setter(self):
        desktop_path = path.join(getenv("userprofile"), "Desktop")
        save_path = QFileDialog.getExistingDirectory(
            parent=self,
            directory=desktop_path,
        )

        if save_path:
            self.__le_save_path.setText(save_path)

    def __settings_dlg(self):
        settings_dialog = SettingsDialog(root_path=self.__root_path)
        settings_dialog.setup_ui()
        settings_dialog.show()
        settings_dialog.exec()

    @staticmethod
    def __about_dlg():
        about_dialog = AboutDialog()
        about_dialog.setup_ui()
        about_dialog.show()
        about_dialog.exec()

    def __contract_maker(self):
        pattern_path = path.join(self.__root_path, 'utils', 'patterns', 'easy_dogovor.docx')

        contract_date = self.__date_tuple_to_str(self.__de_contract_date.date().getDate())
        save_path = self.__documents_title_maker(sellers_data=self.__sellers_data,
                                                 buyers_data=self.__buyers_data)

        contract_maker(pattern_path=pattern_path,
                       save_path=save_path,
                       contract_location=self.__le_contract_location.text(),
                       contract_date=contract_date,
                       sellers_data=self.__sellers_data,
                       buyers_data=self.__buyers_data,
                       real_estate_data=self.__real_estate_data)

        dlg_error_message = QMessageBox()
        dlg_error_message.setWindowTitle('Операция завершена')
        dlg_error_message.setText('Документ успешно сохранён!')
        dlg_error_message.setIcon(QMessageBox.Information)
        dlg_error_message.addButton('Ок', QMessageBox.YesRole)
        dlg_error_message.exec_()

    @staticmethod
    def __date_tuple_to_str(date_tuple: Tuple) -> str:

        if date_tuple[1] < 10:
            month = '0{}'.format(str(date_tuple[1]))
        else:
            month = str(date_tuple[1])

        return '.'.join((str(date_tuple[2]), month, str(date_tuple[0])))

    def __documents_title_maker(self, sellers_data: Dict, buyers_data: Dict) -> str:
        sellers_short_name = ''.join((sellers_data['firstname'].title(),
                                      ' ',
                                      sellers_data['name'][0].title(),
                                      '.',
                                      sellers_data['surname'][0].title(),
                                      '.'))

        buyers_short_name = ''.join((buyers_data['firstname'].title(),
                                      ' ',
                                      buyers_data['name'][0].title(),
                                      '.',
                                      buyers_data['surname'][0].title(),
                                      '.'))

        current_date = datetime.now()
        current_date_string = current_date.strftime('%d-%m-%y %H-%M-%S')
        documents_title = ' '.join((sellers_short_name, '--', buyers_short_name, current_date_string))
        documents_full_title = ''.join((documents_title, '.docx'))

        return path.join(self.__le_save_path.text(), documents_full_title)


if __name__ == "__main__":
    root_path_ = path.abspath('..')

    app = QApplication(sys.argv)
    easyDKP = MainWindowUI(root_path=root_path_)
    easyDKP.setup_ui()
    easyDKP.show()

    sys.exit(app.exec())
