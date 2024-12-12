
from PySide6 import QtWidgets, QtCore
from .ui_alignwidget import Ui_AlignWidget


class AlignWidget(QtWidgets.QWidget, Ui_AlignWidget):

    # Mode has changed, pass True if the mode is Manual else
    # pass False if the mode is Auto.
    modeChanged = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self._make_connections()

    def _make_connections(self):
        self.alignAuto_radioButton.clicked.connect(self._radio_button_clicked)
        self.alignManual_radioButton.clicked.connect(self._radio_button_clicked)

    def _radio_button_clicked(self):
        stacked_widget_index = 0 if self.sender() == self.alignAuto_radioButton else 1
        self.align_stackedWidget.setCurrentIndex(stacked_widget_index)
        self.modeChanged.emit(stacked_widget_index == 1)

    def set_mode(self, manual):
        self.align_stackedWidget.setCurrentIndex(1 if manual else 0)
        self.alignManual_radioButton.setChecked(manual)
        self.alignAuto_radioButton.setChecked(not manual)
