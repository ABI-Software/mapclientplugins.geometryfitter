
from PySide6 import QtWidgets
from .ui_groupsettingswidget import Ui_GroupSettingsWidget


class GroupSettingsWidget(QtWidgets.QWidget, Ui_GroupSettingsWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
