# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fitwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpinBox,
    QWidget)

class Ui_FitWidget(object):
    def setupUi(self, FitWidget):
        if not FitWidget.objectName():
            FitWidget.setObjectName(u"FitWidget")
        FitWidget.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(FitWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.fit_groupBox = QGroupBox(FitWidget)
        self.fit_groupBox.setObjectName(u"fit_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fit_groupBox.sizePolicy().hasHeightForWidth())
        self.fit_groupBox.setSizePolicy(sizePolicy)
        self.fit_groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.fit_groupBox.setFlat(False)
        self.fit_groupBox.setCheckable(False)
        self.formLayout_3 = QFormLayout(self.fit_groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.fitIterations_label = QLabel(self.fit_groupBox)
        self.fitIterations_label.setObjectName(u"fitIterations_label")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.fitIterations_label)

        self.fitIterations_spinBox = QSpinBox(self.fit_groupBox)
        self.fitIterations_spinBox.setObjectName(u"fitIterations_spinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fitIterations_spinBox.sizePolicy().hasHeightForWidth())
        self.fitIterations_spinBox.setSizePolicy(sizePolicy1)
        self.fitIterations_spinBox.setMinimum(1)
        self.fitIterations_spinBox.setMaximum(1000)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.fitIterations_spinBox)

        self.fitMaximumSubIterations_label = QLabel(self.fit_groupBox)
        self.fitMaximumSubIterations_label.setObjectName(u"fitMaximumSubIterations_label")
        self.fitMaximumSubIterations_label.setEnabled(False)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.fitMaximumSubIterations_label)

        self.fitMaximumSubIterations_spinBox = QSpinBox(self.fit_groupBox)
        self.fitMaximumSubIterations_spinBox.setObjectName(u"fitMaximumSubIterations_spinBox")
        self.fitMaximumSubIterations_spinBox.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.fitMaximumSubIterations_spinBox.sizePolicy().hasHeightForWidth())
        self.fitMaximumSubIterations_spinBox.setSizePolicy(sizePolicy1)
        self.fitMaximumSubIterations_spinBox.setMinimum(1)
        self.fitMaximumSubIterations_spinBox.setMaximum(1000)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.fitMaximumSubIterations_spinBox)

        self.fitUpdateReferenceState_checkBox = QCheckBox(self.fit_groupBox)
        self.fitUpdateReferenceState_checkBox.setObjectName(u"fitUpdateReferenceState_checkBox")
        sizePolicy.setHeightForWidth(self.fitUpdateReferenceState_checkBox.sizePolicy().hasHeightForWidth())
        self.fitUpdateReferenceState_checkBox.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.fitUpdateReferenceState_checkBox)


        self.horizontalLayout.addWidget(self.fit_groupBox)


        self.retranslateUi(FitWidget)

        QMetaObject.connectSlotsByName(FitWidget)
    # setupUi

    def retranslateUi(self, FitWidget):
        FitWidget.setWindowTitle(QCoreApplication.translate("FitWidget", u"Fit Widget", None))
        self.fit_groupBox.setTitle(QCoreApplication.translate("FitWidget", u"Fit", None))
        self.fitIterations_label.setText(QCoreApplication.translate("FitWidget", u"Iterations:", None))
#if QT_CONFIG(tooltip)
        self.fitIterations_spinBox.setToolTip(QCoreApplication.translate("FitWidget", u"<html><head/><body><p>Number of full iterations with reprojection of data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.fitMaximumSubIterations_label.setText(QCoreApplication.translate("FitWidget", u"Maximum subiterations:", None))
#if QT_CONFIG(tooltip)
        self.fitUpdateReferenceState_checkBox.setToolTip(QCoreApplication.translate("FitWidget", u"<html><head/><body><p>Advanced: Update reference state to coordinates at end of this step for applying subsequent strain and curvature penalties.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.fitUpdateReferenceState_checkBox.setText(QCoreApplication.translate("FitWidget", u"Update reference state", None))
    # retranslateUi

