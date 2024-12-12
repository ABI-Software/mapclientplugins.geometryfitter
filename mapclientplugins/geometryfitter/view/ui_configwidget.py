# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ConfigWidget(object):
    def setupUi(self, ConfigWidget):
        if not ConfigWidget.objectName():
            ConfigWidget.setObjectName(u"ConfigWidget")
        ConfigWidget.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(ConfigWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.config_groupBox = QGroupBox(ConfigWidget)
        self.config_groupBox.setObjectName(u"config_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.config_groupBox.sizePolicy().hasHeightForWidth())
        self.config_groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.config_groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.config_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.config_verticalSpacer)


        self.horizontalLayout.addWidget(self.config_groupBox)


        self.retranslateUi(ConfigWidget)

        QMetaObject.connectSlotsByName(ConfigWidget)
    # setupUi

    def retranslateUi(self, ConfigWidget):
        ConfigWidget.setWindowTitle(QCoreApplication.translate("ConfigWidget", u"Config", None))
        self.config_groupBox.setTitle(QCoreApplication.translate("ConfigWidget", u"Config", None))
    # retranslateUi

