
from PySide6 import QtWidgets
from .ui_fitwidget import Ui_FitWidget


class FitWidget(QtWidgets.QWidget, Ui_FitWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
