from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QFrame, QApplication, \
    QProgressDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import QRect, Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont, QCloseEvent

from utils.second_thread import SecondThread
from api_interaction.egrn_request import ApiEGRN
from utils.num_to_word import num2text

from typing import Dict, Union


class RealEstateDataUi(QDialog):

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.__title = title

        self.__lbl_cadastral_number = None  # lbl - сокращение от label
        self.__lbl_service_message = None
        self.__lbl_address = None
        self.__lbl_square = None
        self.__lbl_square_unit = None
        self.__lbl_lands_category = None
        self.__lbl_permitted_use_type = None
        self.__lbl_state_registration_date_and_number = None
        self.__lbl_registration_reason = None
        self.__lbl_registration_reason_note = None
        self.__lbl_price = None
        self.__lbl_price_unit = None
        self.__lbl_price_note = None

        self.__le_cadastral_number = None  # le - сокращение от lineEdit
        self.__pte_address = None  # pte = сокращение от PlainTextEdit
        self.__le_square = None
        self.__le_lands_category = None
        self.__le_permitted_use_type = None
        self.__le_state_registration_date_and_number = None
        self.__le_registration_reason = None
        self.__le_price = None

        self.__btn_request = None  # btn - сокращение от button
        self.__btn_cancel = None
        self.__btn_clear_all = None
        self.__btn_save = None

        self.__horizontal_line = None

        self.__clr_white = "background-color: rgb(255, 255, 255);"
        self.__clr_yellow = 'background-color: rgb(255, 245, 92);'

        self.__real_estate_data = None

    def setup_ui(self):
        self.setObjectName("dlg_real_estate_data")
        self.setFixedSize(370, 550)
        self.setStyleSheet("background-color: rgb(248, 248, 216);")
        self.setModal(True)

        self.__lbl_cadastral_number = QLabel(self)
        self.__lbl_cadastral_number.setGeometry(QRect(50, 10, 141, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_cadastral_number.setFont(font)
        self.__lbl_cadastral_number.setStyleSheet("color: rgb(127, 63, 0);")
        self.__lbl_cadastral_number.setObjectName("lbl_cadastral_number")

        self.__lbl_service_message = QLabel(self)
        self.__lbl_service_message.setGeometry(QRect(10, 70, 351, 16))
        self.__lbl_service_message.setText("")
        self.__lbl_service_message.setObjectName("lbl_service_message")

        self.__lbl_address = QLabel(self)
        self.__lbl_address.setGeometry(QRect(10, 110, 51, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_address.setFont(font)
        self.__lbl_address.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_address.setObjectName("lbl_address")

        self.__lbl_square = QLabel(self)
        self.__lbl_square.setGeometry(QRect(10, 186, 71, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_square.setFont(font)
        self.__lbl_square.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_square.setObjectName("lbl_square")

        self.__lbl_square_unit = QLabel(self)
        self.__lbl_square_unit.setGeometry(QRect(94, 210, 31, 16))
        font = QFont()
        font.setPointSize(10)
        self.__lbl_square_unit.setFont(font)
        self.__lbl_square_unit.setObjectName("lbl_square_unit")

        self.__lbl_lands_category = QLabel(self)
        self.__lbl_lands_category.setGeometry(QRect(10, 236, 131, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_lands_category.setFont(font)
        self.__lbl_lands_category.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_lands_category.setObjectName("lbl_lands_category")

        self.__lbl_permitted_use_type = QLabel(self)
        self.__lbl_permitted_use_type.setGeometry(QRect(10, 286, 241, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_permitted_use_type.setFont(font)
        self.__lbl_permitted_use_type.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_permitted_use_type.setObjectName("lbl_permitted_use_type")

        self.__lbl_state_registration_date_and_number = QLabel(self)
        self.__lbl_state_registration_date_and_number.setGeometry(QRect(10, 336, 301, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_state_registration_date_and_number.setFont(font)
        self.__lbl_state_registration_date_and_number.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_state_registration_date_and_number.setObjectName("lbl_state_registration_date_and_number")

        self.__lbl_registration_reason = QLabel(self)
        self.__lbl_registration_reason.setGeometry(QRect(10, 386, 281, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_registration_reason.setFont(font)
        self.__lbl_registration_reason.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_registration_reason.setObjectName("lbl_registration_reason")

        self.__lbl_registration_reason_note = QLabel(self)
        self.__lbl_registration_reason_note.setGeometry(QRect(240, 428, 121, 14))
        font = QFont()
        font.setPointSize(8)
        self.__lbl_registration_reason_note.setFont(font)
        self.__lbl_registration_reason_note.setObjectName("lbl_registration_reason_note")

        self.__lbl_price = QLabel(self)
        self.__lbl_price.setGeometry(QRect(10, 434, 151, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__lbl_price.setFont(font)
        self.__lbl_price.setStyleSheet("color: rgb(0, 75, 0);")
        self.__lbl_price.setObjectName("lbl_price")

        self.__lbl_price_unit = QLabel(self)
        self.__lbl_price_unit.setGeometry(QRect(164, 458, 31, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.__lbl_price_unit.setFont(font)
        self.__lbl_price_unit.setObjectName("lbl_price_unit")

        self.__lbl_price_note = QLabel(self)
        self.__lbl_price_note.setGeometry(QRect(40, 475, 121, 14))
        font = QFont()
        font.setPointSize(8)
        self.__lbl_price_note.setFont(font)
        self.__lbl_price_note.setObjectName("lbl_price_note")

        self.__le_cadastral_number = QLineEdit(self)
        self.__le_cadastral_number.setGeometry(QRect(50, 30, 135, 20))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.__le_cadastral_number.setFont(font)
        self.__le_cadastral_number.setStyleSheet(self.__clr_white)
        self.__le_cadastral_number.setObjectName("le_cadastral_number")
        self.__le_cadastral_number.setInputMask('99:99:9999999:999;_')
        self.__le_cadastral_number.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.__pte_address = QPlainTextEdit(self)
        self.__pte_address.setGeometry(QRect(10, 130, 351, 41))
        font = QFont()
        font.setPointSize(9)
        self.__pte_address.setFont(font)
        self.__pte_address.setStyleSheet(self.__clr_white)
        self.__pte_address.setTabChangesFocus(True)
        self.__pte_address.setObjectName("pte_address")

        self.__le_square = QLineEdit(self)
        self.__le_square.setGeometry(QRect(10, 206, 81, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_square.setFont(font)
        self.__le_square.setStyleSheet(self.__clr_white)
        self.__le_square.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.__le_square.setObjectName("le_square")

        self.__le_lands_category = QLineEdit(self)
        self.__le_lands_category.setGeometry(QRect(10, 256, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_lands_category.setFont(font)
        self.__le_lands_category.setStyleSheet(self.__clr_white)
        self.__le_lands_category.setObjectName("le_lands_category")

        self.__le_permitted_use_type = QLineEdit(self)
        self.__le_permitted_use_type.setGeometry(QRect(10, 306, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_permitted_use_type.setFont(font)
        self.__le_permitted_use_type.setStyleSheet(self.__clr_white)
        self.__le_permitted_use_type.setObjectName("le_permitted_use_type")

        self.__le_state_registration_date_and_number = QLineEdit(self)
        self.__le_state_registration_date_and_number.setGeometry(QRect(10, 356, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_state_registration_date_and_number.setFont(font)
        self.__le_state_registration_date_and_number.setStyleSheet(self.__clr_white)
        self.__le_state_registration_date_and_number.setObjectName("le_state_registration_date_and_number")

        self.__le_registration_reason = QLineEdit(self)
        self.__le_registration_reason.setGeometry(QRect(10, 406, 351, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_registration_reason.setFont(font)
        self.__le_registration_reason.setStyleSheet(self.__clr_white)
        self.__le_registration_reason.setObjectName("le_registration_reason")

        self.__le_price = QLineEdit(self)
        self.__le_price.setGeometry(QRect(10, 454, 151, 20))
        font = QFont()
        font.setPointSize(9)
        self.__le_price.setFont(font)
        self.__le_price.setStyleSheet(self.__clr_white)
        self.__le_price.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.__le_price.setObjectName("le_price")

        self.__btn_request = QPushButton(self)
        self.__btn_request.setGeometry(QRect(210, 29, 101, 22))
        font = QFont()
        font.setPointSize(10)
        self.__btn_request.setFont(font)
        self.__btn_request.setStyleSheet("background-color: rgb(202, 229, 255);")
        self.__btn_request.setObjectName("btn_request")

        self.__btn_cancel = QPushButton(self)
        self.__btn_cancel.setGeometry(QRect(14, 520, 75, 23))
        font = QFont()
        font.setPointSize(9)
        self.__btn_cancel.setFont(font)
        self.__btn_cancel.setStyleSheet("background-color: rgb(205, 205, 205);")
        self.__btn_cancel.setObjectName("btn_cancel")

        self.__btn_clear_all = QPushButton(self)
        self.__btn_clear_all.setGeometry(QRect(100, 520, 91, 23))
        font = QFont()
        font.setPointSize(9)
        self.__btn_clear_all.setFont(font)
        self.__btn_clear_all.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.__btn_clear_all.setObjectName("btn_clear_all")

        self.__btn_save = QPushButton(self)
        self.__btn_save.setGeometry(QRect(260, 512, 101, 31))
        font = QFont()
        font.setPointSize(10)
        self.__btn_save.setFont(font)
        self.__btn_save.setStyleSheet("background-color: rgb(202, 255, 202);")
        self.__btn_save.setObjectName("btn_save")

        self.__horizontal_line = QFrame(self)
        self.__horizontal_line.setGeometry(QRect(0, 100, 381, 8))
        self.__horizontal_line.setFrameShape(QFrame.HLine)
        self.__horizontal_line.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line.setObjectName("horizontal_line")

        self.setTabOrder(self.__le_cadastral_number, self.__btn_request)
        self.setTabOrder(self.__btn_request, self.__pte_address)
        self.setTabOrder(self.__pte_address, self.__le_square)
        self.setTabOrder(self.__le_square, self.__le_lands_category)
        self.setTabOrder(self.__le_lands_category, self.__le_permitted_use_type)
        self.setTabOrder(self.__le_permitted_use_type, self.__le_state_registration_date_and_number)
        self.setTabOrder(self.__le_state_registration_date_and_number, self.__le_registration_reason)
        self.setTabOrder(self.__le_registration_reason, self.__le_price)
        self.setTabOrder(self.__le_price, self.__btn_save)
        self.setTabOrder(self.__btn_save, self.__btn_clear_all)
        self.setTabOrder(self.__btn_clear_all, self.__btn_cancel)

        self.__re_translate_ui()
        QMetaObject.connectSlotsByName(self)

        self.__btn_actions()

    def __re_translate_ui(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("dlg_real_estate_data", self.__title))

        self.__lbl_cadastral_number.setText(_translate("dlg_real_estate_data", "кадастровый номер"))
        self.__lbl_address.setText(_translate("dlg_real_estate_data", "адрес"))
        self.__lbl_square.setText(_translate("dlg_real_estate_data", "площадь"))
        self.__lbl_square_unit.setText(_translate("dlg_real_estate_data", "кв.м"))
        self.__lbl_lands_category.setText(_translate("dlg_real_estate_data", "категория земель"))
        self.__lbl_permitted_use_type.setText(_translate("dlg_real_estate_data", "вид разрешенного использования"))
        self.__lbl_state_registration_date_and_number.setText(
            _translate("dlg_real_estate_data", "дата и время государственной регистрации")
        )
        self.__lbl_registration_reason.setText(
            _translate("dlg_real_estate_data", "основание государственной регистрации")
        )
        self.__lbl_registration_reason_note.setText(_translate("dlg_real_estate_data", "(заполняется вручную)"))
        self.__lbl_price.setText(_translate("dlg_real_estate_data", "цена купли/продажи"))
        self.__lbl_price_unit.setText(_translate("dlg_real_estate_data", "руб."))
        self.__lbl_price_note.setText(_translate("dlg_real_estate_data", "(заполняется вручную)"))

        self.__btn_request.setText(_translate("dlg_real_estate_data", "Запросить "))
        self.__btn_cancel.setText(_translate("dlg_real_estate_data", "Отмена"))
        self.__btn_clear_all.setText(_translate("dlg_real_estate_data", "Очистить всё"))
        self.__btn_save.setText(_translate("dlg_real_estate_data", "Сохранить"))

    def __btn_actions(self):
        self.__btn_request.clicked.connect(self.__real_estate_data_requester)
        self.__btn_cancel.clicked.connect(self.close)
        self.__btn_clear_all.clicked.connect(self.__all_lines_cleaner)
        self.__btn_save.clicked.connect(self.__real_estate_data_saver)

    def __real_estate_data_requester(self):
        if len(self.__le_cadastral_number.text()) > 13:
            self.__second_thread = SecondThread(ApiEGRN.real_estate_data_request, self.__le_cadastral_number.text())
            self.__progress_dlg_setter()
            self.__second_thread.my_signal.connect(self.__progress_dlg_display, Qt.QueuedConnection)
            self.__second_thread.start()
        else:
            self.__le_cadastral_number.setStyleSheet(self.__clr_yellow)

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
            real_estate_data = ApiEGRN.real_estate_data_getter(deserialized_response=response)

            if isinstance(real_estate_data, dict):
                self.__real_estate_data_display(real_estate_data)

            elif isinstance(real_estate_data, str):
                self.__error_message_display(real_estate_data)

        elif isinstance(response, str):
            self.__error_message_display(response)

    def __real_estate_data_display(self, real_estate_data: Dict):

        # проверка наличия адреса
        if real_estate_data['address']:
            self.__pte_address.setPlainText(real_estate_data['address'])
        else:
            self.__pte_address.setStyleSheet(self.__clr_yellow)

        # проверка наличия площади
        if real_estate_data['square']:
            self.__le_square.setText(real_estate_data['square'])
        else:
            self.__le_square.setStyleSheet(self.__clr_yellow)

        # проверка наличия категории земель
        if real_estate_data['lands_category']:
            self.__le_lands_category.setText(real_estate_data['lands_category'].lower())
        else:
            self.__le_lands_category.setStyleSheet(self.__clr_yellow)

        # проверка наличия разрешенное использование
        if real_estate_data['permitted_use_type']:
            self.__le_permitted_use_type.setText(real_estate_data['permitted_use_type'].lower())
        else:
            self.__le_permitted_use_type.setStyleSheet(self.__clr_yellow)

        # проверка наличия даты и номера регистрации
        if real_estate_data['state_registration_date_and_number']:
            self.__le_state_registration_date_and_number.setText(real_estate_data['state_registration_date_and_number'])
        else:
            self.__le_state_registration_date_and_number.setStyleSheet(self.__clr_yellow)

    def __real_estate_data_saver(self):
        is_all_right = True
        text_lines_tuple = (self.__le_square,
                            self.__le_lands_category,
                            self.__le_permitted_use_type,
                            self.__le_state_registration_date_and_number,
                            self.__le_registration_reason,
                            self.__le_price)

        for line in text_lines_tuple:
            if len(line.text()) == 0:
                line.setStyleSheet(self.__clr_yellow)
                is_all_right = False

        if len(self.__pte_address.toPlainText()) == 0:
            self.__pte_address.setStyleSheet(self.__clr_yellow)
            is_all_right = False

        if is_all_right:
            price = int(self.__le_price.text())
            price_string = num2text(price)
            self.__real_estate_data = {
                'cadastral_number': self.__le_cadastral_number.text(),
                'address': self.__pte_address.toPlainText(),
                'square': self.__le_square.text(),
                'lands_category': self.__le_lands_category.text(),
                'permitted_use_type': self.__le_permitted_use_type.text(),
                'state_registration_date_and_number': self.__le_state_registration_date_and_number.text(),
                'registration_reason': self.__le_registration_reason.text(),
                'price': self.__le_price.text(),
                'price_string': price_string
            }

            self.close()

    def __all_lines_cleaner(self):
        text_lines_tuple = (self.__pte_address,
                            self.__le_square,
                            self.__le_lands_category,
                            self.__le_permitted_use_type,
                            self.__le_state_registration_date_and_number,
                            self.__le_registration_reason,
                            self.__le_price)

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

                for line in text_lines_tuple:
                    line.clear()
                    line.setStyleSheet(self.__clr_white)

        else:

            for line in text_lines_tuple:
                line.setStyleSheet(self.__clr_white)

    def __is_all_lines_clean(self) -> bool:
        is_all_lines_clean_tuple = (len(self.__pte_address.toPlainText()) == 0,
                                    len(self.__le_square.text()) == 0,
                                    len(self.__le_lands_category.text()) == 0,
                                    len(self.__le_permitted_use_type.text()) == 0,
                                    len(self.__le_state_registration_date_and_number.text()) == 0,
                                    len(self.__le_registration_reason.text()) == 0,
                                    len(self.__le_price.text()) == 0)

        if all(is_all_lines_clean_tuple):
            return True

        return False

    def closeEvent(self, event: QCloseEvent) -> None:
        if not isinstance(self.__real_estate_data, dict):

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
                    event.ignore()
            else:
                event.accept()
        else:
            event.accept()

    def __error_message_display(self, message):
        dlg_error_message = QMessageBox(parent=self)
        dlg_error_message.setWindowTitle('Сообщение об ошибке')
        dlg_error_message.setText(message)
        dlg_error_message.setIcon(QMessageBox.Critical)
        dlg_error_message.addButton('Ок', QMessageBox.YesRole)
        dlg_error_message.exec_()

    @property
    def real_estate_data(self) -> Union[Dict, bool]:
        if self.__real_estate_data:
            return self.__real_estate_data
        return False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg_real_estate_data = RealEstateDataUi('Данные недвижимости')
    dlg_real_estate_data.setup_ui()
    dlg_real_estate_data.show()
    sys.exit(app.exec_())
