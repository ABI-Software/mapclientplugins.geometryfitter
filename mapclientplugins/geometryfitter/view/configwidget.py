
from PySide6 import QtWidgets
from .ui_configwidget import Ui_ConfigWidget


class ConfigWidget(QtWidgets.QWidget, Ui_ConfigWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
