
from PySide6 import QtWidgets
from .ui_initialconfigwidget import Ui_InitialConfigWidget


class InitialConfigWidget(QtWidgets.QWidget, Ui_InitialConfigWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
