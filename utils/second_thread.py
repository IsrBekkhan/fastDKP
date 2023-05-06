from PyQt5.QtCore import QThread, pyqtSignal
from typing import Callable, Union, Dict


class SecondThread(QThread):
    my_signal = pyqtSignal(str)

    def __init__(self, function: Callable, argument: str, parent=None):
        QThread.__init__(self, parent)
        self.__function = function
        self.__argument = argument
        self.__response = None

    def run(self):
        self.my_signal.emit('start')
        self.__response = self.__function(self.__argument)
        self.my_signal.emit('finish')

    @property
    def response(self) -> Union[Dict, bool]:
        if self.__response:
            return self.__response
        return False


