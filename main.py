from PyQt5.QtWidgets import QApplication

import sys
from os import path, getenv, getcwd

from common_gui.main_window import MainWindowUI


if __name__ == "__main__":
    root_path = getcwd()
    print(path.abspath(''))
    print(root_path)

    app = QApplication(sys.argv)
    easyDKP = MainWindowUI(root_path=root_path)
    easyDKP.setup_ui()
    easyDKP.show()

    sys.exit(app.exec())
