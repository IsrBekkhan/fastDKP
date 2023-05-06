from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QLineEdit, QPushButton, QFrame, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication

import sys
from os import path, getenv
from json import dump


class SettingsDialog(QDialog):

    def __init__(self, root_path: str):
        super().__init__()
        self.__root_path = root_path

        self.__lbl_main_menu_settings = None
        self.__lbl_default_contact_location = None
        self.__lbl_default_save_path = None
        self.__lbl_ads_settings = None
        self.__lbl_ads_token = None
        self.__lbl_ads_url = None
        self.__lbl_api_egrn_settings = None
        self.__lbl_api_egrn_token = None
        self.__lbl_api_egrn_host = None
        self.__lbl_api_egrn_url = None

        self.__le_default_contact_location = None
        self.__le_default_save_path = None
        self.__le_ads_token = None
        self.__le_ads_url = None
        self.__le_api_egrn_token = None
        self.__le_api_egrn_host = None
        self.__le_api_egrn_url = None

        self.__btn_save_path = None
        self.__btn_save = None
        self.__btn_cancel = None

        self.__horizontal_line_1 = None
        self.__horizontal_line_2 = None
        self.__horizontal_line_3 = None

    def setup_ui(self):
        self.setObjectName("settings_dialog")
        self.setFixedSize(431, 499)
        self.setModal(True)

        self.__lbl_main_menu_settings = QLabel(self)
        self.__lbl_main_menu_settings.setGeometry(QRect(20, 10, 221, 20))
        font = QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.__lbl_main_menu_settings.setFont(font)
        self.__lbl_main_menu_settings.setObjectName("lbl_main_menu_settings")

        self.__lbl_default_contact_location = QLabel(self)
        self.__lbl_default_contact_location.setGeometry(QRect(70, 40, 261, 16))
        font = QFont()
        font.setPointSize(9)
        font.setWeight(50)
        self.__lbl_default_contact_location.setFont(font)
        self.__lbl_default_contact_location.setObjectName("lbl_default_contact_location")

        self.__lbl_default_save_path = QLabel(self)
        self.__lbl_default_save_path.setGeometry(QRect(70, 90, 261, 16))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_default_save_path.setFont(font)
        self.__lbl_default_save_path.setObjectName("lbl_default_save_path")

        self.__lbl_ads_settings = QLabel(self)
        self.__lbl_ads_settings.setGeometry(QRect(20, 150, 401, 20))
        font = QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.__lbl_ads_settings.setFont(font)
        self.__lbl_ads_settings.setObjectName("lbl_ads_settings")

        self.__lbl_ads_token = QLabel(self)
        self.__lbl_ads_token.setGeometry(QRect(50, 182, 41, 16))
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.__lbl_ads_token.setFont(font)
        self.__lbl_ads_token.setObjectName("lbl_ads_token")

        self.__lbl_ads_url = QLabel(self)
        self.__lbl_ads_url.setGeometry(QRect(60, 220, 31, 16))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_ads_url.setFont(font)
        self.__lbl_ads_url.setObjectName("lbl_ads_url")

        self.__lbl_api_egrn_settings = QLabel(self)
        self.__lbl_api_egrn_settings.setGeometry(QRect(20, 280, 391, 31))
        font = QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.__lbl_api_egrn_settings.setFont(font)
        self.__lbl_api_egrn_settings.setObjectName("lbl_api_egrn_settings_start")

        self.__lbl_api_egrn_token = QLabel(self)
        self.__lbl_api_egrn_token.setGeometry(QRect(50, 332, 41, 16))
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.__lbl_api_egrn_token.setFont(font)
        self.__lbl_api_egrn_token.setObjectName("lbl_api_egrn_token")

        self.__lbl_api_egrn_host = QLabel(self)
        self.__lbl_api_egrn_host.setGeometry(QRect(60, 370, 31, 16))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_api_egrn_host.setFont(font)
        self.__lbl_api_egrn_host.setObjectName("lbl_api_egrn_host")

        self.__lbl_api_egrn_url = QLabel(self)
        self.__lbl_api_egrn_url.setGeometry(QRect(60, 410, 31, 16))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_api_egrn_url.setFont(font)
        self.__lbl_api_egrn_url.setObjectName("lbl_api_egrn_url")

        self.__le_default_contact_location = QLineEdit(self)
        self.__le_default_contact_location.setGeometry(QRect(70, 60, 341, 20))
        self.__le_default_contact_location.setObjectName("le_default_contact_location")

        self.__le_default_save_path = QLineEdit(self)
        self.__le_default_save_path.setGeometry(QRect(70, 110, 271, 20))
        self.__le_default_save_path.setObjectName("le_default_save_path")

        self.__le_ads_token = QLineEdit(self)
        self.__le_ads_token.setGeometry(QRect(100, 180, 311, 20))
        self.__le_ads_token.setObjectName("le_ads_token")

        self.__le_ads_url = QLineEdit(self)
        self.__le_ads_url.setGeometry(QRect(100, 220, 311, 20))
        self.__le_ads_url.setObjectName("le_ads_url")

        self.__le_api_egrn_token = QLineEdit(self)
        self.__le_api_egrn_token.setGeometry(QRect(100, 330, 311, 20))
        self.__le_api_egrn_token.setObjectName("le_api_egrn_token")

        self.__le_api_egrn_host = QLineEdit(self)
        self.__le_api_egrn_host.setGeometry(QRect(100, 370, 311, 20))
        self.__le_api_egrn_host.setObjectName("le_api_egrn_host")

        self.__le_api_egrn_url = QLineEdit(self)
        self.__le_api_egrn_url.setGeometry(QRect(100, 410, 311, 20))
        self.__le_api_egrn_url.setObjectName("le_api_egrn_url")

        self.__btn_save_path = QPushButton(self)
        self.__btn_save_path.setGeometry(QRect(350, 109, 61, 23))
        self.__btn_save_path.setObjectName("btn_save_path")

        self.__btn_save = QPushButton(self)
        self.__btn_save.setGeometry(QRect(330, 460, 75, 23))
        self.__btn_save.setObjectName("btn_save")

        self.__btn_cancel = QPushButton(self)
        self.__btn_cancel.setGeometry(QRect(10, 460, 75, 23))
        self.__btn_cancel.setObjectName("btn_cancel")

        self.__horizontal_line_1 = QFrame(self)
        self.__horizontal_line_1.setGeometry(QRect(0, 140, 431, 8))
        self.__horizontal_line_1.setFrameShape(QFrame.HLine)
        self.__horizontal_line_1.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_1.setObjectName("horizontal_line_1")

        self.__horizontal_line_2 = QFrame(self)
        self.__horizontal_line_2.setGeometry(QRect(0, 260, 431, 8))
        self.__horizontal_line_2.setFrameShape(QFrame.HLine)
        self.__horizontal_line_2.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_2.setObjectName("horizontal_line_2")

        self.__horizontal_line_3 = QFrame(self)
        self.__horizontal_line_3.setGeometry(QRect(0, 440, 431, 8))
        self.__horizontal_line_3.setFrameShape(QFrame.HLine)
        self.__horizontal_line_3.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line_3.setObjectName("horizontal_line_3")

        self.setTabOrder(self.__le_default_contact_location, self.__le_default_save_path)
        self.setTabOrder(self.__le_default_save_path, self.__btn_save_path)
        self.setTabOrder(self.__btn_save_path, self.__le_ads_token)
        self.setTabOrder(self.__le_ads_token, self.__le_ads_url)
        self.setTabOrder(self.__le_ads_url, self.__le_api_egrn_token)
        self.setTabOrder(self.__le_api_egrn_token, self.__le_api_egrn_host)
        self.setTabOrder(self.__le_api_egrn_host, self.__le_api_egrn_url)
        self.setTabOrder(self.__le_api_egrn_url, self.__btn_save)
        self.setTabOrder(self.__btn_save, self.__btn_cancel)

        self.__re_translate_ui()
        QMetaObject.connectSlotsByName(self)

        self.__btn_actions()
        self.__default_params_setter()

    def __re_translate_ui(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("settings_dialog", "Настройки"))

        self.__lbl_main_menu_settings.setText(_translate("settings_dialog", "Настройки элементов главного окна"))
        self.__lbl_default_contact_location.setText(
            _translate("settings_dialog", "место заключения договора по умолчанию"))
        self.__lbl_default_save_path.setText(_translate("settings_dialog", "папка сохранения договора по умолчанию"))
        self.__lbl_ads_settings.setText(_translate("settings_dialog",
                                                   "Настройки сервиса распознования фотографий паспорта ads-soft.ru"))
        self.__lbl_ads_token.setText(_translate("settings_dialog", "Tокен"))
        self.__lbl_ads_url.setText(_translate("settings_dialog", "URL"))
        self.__lbl_api_egrn_settings.setText(
            _translate("settings_dialog", "Настройки сервиса предоставления спраочной информации\n"
                                          "по объектам недвижимости api-egrn.ru "))
        self.__lbl_api_egrn_token.setText(_translate("settings_dialog", "Tокен"))
        self.__lbl_api_egrn_host.setText(_translate("settings_dialog", "Host"))
        self.__lbl_api_egrn_url.setText(_translate("settings_dialog", "URL"))

        self.__btn_save_path.setText(_translate("settings_dialog", "Изменить"))
        self.__btn_save.setText(_translate("settings_dialog", "Сохранить"))
        self.__btn_cancel.setText(_translate("settings_dialog", "Отмена"))

    def __default_params_setter(self):
        self.__le_default_contact_location.setText('г. Урус-Мартан')
        desktop_path = path.join(getenv("userprofile"), "Desktop")
        self.__le_default_save_path.setText(desktop_path)

        self.__le_ads_token.setText('6e85fcbc5cba696d39c4cdd5caa6ebd5')
        self.__le_ads_url.setText('https://api.ocr.ads-soft.ru/recognition')

        self.__le_api_egrn_token.setText('PY86-UAU0-TD5N-KFD5')
        self.__le_api_egrn_host.setText('apiegrn.ru')
        self.__le_api_egrn_url.setText('https://apiegrn.ru/api/cadaster/objectInfoFull')

    def __btn_actions(self):
        self.__btn_save_path.clicked.connect(self.__save_path_setter)
        self.__btn_cancel.clicked.connect(self.close)
        self.__btn_save.clicked.connect(self.__settings_saver)

    def __save_path_setter(self):
        desktop_path = path.join(getenv("userprofile"), "Desktop")
        save_path = QFileDialog.getExistingDirectory(
            parent=self,
            directory=desktop_path,
        )

        if save_path:
            self.__le_default_save_path.setText(save_path)

    def __settings_saver(self):
        config_data = {'contract_location': self.__le_default_contact_location.text(),
                       'save_path': self.__le_default_save_path.text(),
                       'ads_token': self.__le_ads_token.text(),
                       'ads_url': self.__le_ads_url.text(),
                       'api_egrn_token': self.__le_api_egrn_token.text(),
                       'api_egrn_host': self.__le_api_egrn_host.text(),
                       'api_egrn_url': self.__le_api_egrn_url.text()}

        config_data_path = path.join(self.__root_path, 'config_data', 'config_data.json')

        with open(config_data_path, 'w', encoding='utf-8') as config_data_file:
            dump(config_data, config_data_file, indent=4)

        self.close()


if __name__ == "__main__":
    root_path_ = path.abspath('..')

    app = QApplication(sys.argv)
    settings_dialog = SettingsDialog(root_path=root_path_)
    settings_dialog.setup_ui()
    settings_dialog.show()
    sys.exit(app.exec())
