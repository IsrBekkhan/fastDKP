from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QFrame, QPushButton
from PyQt5.QtCore import QMetaObject, QCoreApplication, QRect
from PyQt5.QtGui import QFont


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.__lbl_easydkp_description = None
        self.__horizontal_line = None
        self.__lbl_version = None
        self.__btn_ok = None

    def setup_ui(self):
        self.setObjectName("about_dialog")
        self.setFixedSize(310, 130)
        self.setModal(True)

        self.__lbl_easydkp_description = QLabel(self)
        self.__lbl_easydkp_description.setGeometry(QRect(10, 10, 301, 51))
        font = QFont()
        font.setPointSize(9)
        self.__lbl_easydkp_description.setFont(font)
        self.__lbl_easydkp_description.setObjectName("lbl_easydkp_description")

        self.__horizontal_line = QFrame(self)
        self.__horizontal_line.setGeometry(QRect(0, 60, 311, 8))
        self.__horizontal_line.setFrameShape(QFrame.HLine)
        self.__horizontal_line.setFrameShadow(QFrame.Sunken)
        self.__horizontal_line.setObjectName("horizontal_line")

        self.__lbl_version = QLabel(self)
        self.__lbl_version.setGeometry(QRect(90, 70, 151, 16))
        self.__lbl_version.setObjectName("lbl_version")

        self.__btn_ok = QPushButton(self)
        self.__btn_ok.setGeometry(QRect(120, 100, 75, 23))
        self.__btn_ok.setObjectName("btn_ok")

        self.__re_translate_ui()
        QMetaObject.connectSlotsByName(self)

        self.__btn_actions()

    def __re_translate_ui(self):
        _translate = QCoreApplication.translate

        self.setWindowTitle(_translate("Dialog", "о программе"))
        self.__lbl_easydkp_description.setText(
            _translate("Dialog", "    easyDKP - программа для быстрого создания\n"
                                 " договора купли/продажи объекта недвижимости")
        )
        self.__lbl_version.setText(_translate("Dialog", "Версия: 0.00 от 22.04.2023"))
        self.__btn_ok.setText(_translate("Dialog", "Ок"))

    def __btn_actions(self):
        self.__btn_ok.clicked.connect(self.close)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    about_dialog = AboutDialog()
    about_dialog.setup_ui()
    about_dialog.show()
    sys.exit(app.exec())
