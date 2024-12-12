# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'alignwidget.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

class Ui_AlignWidget(object):
    def setupUi(self, AlignWidget):
        if not AlignWidget.objectName():
            AlignWidget.setObjectName(u"AlignWidget")
        AlignWidget.resize(396, 537)
        self.verticalLayout = QVBoxLayout(AlignWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.align_groupBox = QGroupBox(AlignWidget)
        self.align_groupBox.setObjectName(u"align_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.align_groupBox.sizePolicy().hasHeightForWidth())
        self.align_groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.align_groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.align_groupBox)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.alignAuto_radioButton = QRadioButton(self.groupBox)
        self.alignAuto_radioButton.setObjectName(u"alignAuto_radioButton")
        self.alignAuto_radioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.alignAuto_radioButton)

        self.alignManual_radioButton = QRadioButton(self.groupBox)
        self.alignManual_radioButton.setObjectName(u"alignManual_radioButton")

        self.horizontalLayout_2.addWidget(self.alignManual_radioButton)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.align_stackedWidget = QStackedWidget(self.align_groupBox)
        self.align_stackedWidget.setObjectName(u"align_stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.formLayout_2 = QFormLayout(self.page)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.alignGroups_label = QLabel(self.page)
        self.alignGroups_label.setObjectName(u"alignGroups_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.alignGroups_label)

        self.alignGroups_checkBox = QCheckBox(self.page)
        self.alignGroups_checkBox.setObjectName(u"alignGroups_checkBox")
        self.alignGroups_checkBox.setToolTipDuration(2)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.alignGroups_checkBox)

        self.alignMarkers_label = QLabel(self.page)
        self.alignMarkers_label.setObjectName(u"alignMarkers_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.alignMarkers_label)

        self.alignMarkers_checkBox = QCheckBox(self.page)
        self.alignMarkers_checkBox.setObjectName(u"alignMarkers_checkBox")
        sizePolicy.setHeightForWidth(self.alignMarkers_checkBox.sizePolicy().hasHeightForWidth())
        self.alignMarkers_checkBox.setSizePolicy(sizePolicy)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.alignMarkers_checkBox)

        self.alignScaleProportion_label = QLabel(self.page)
        self.alignScaleProportion_label.setObjectName(u"alignScaleProportion_label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.alignScaleProportion_label)

        self.alignScaleProportion_lineEdit = QLineEdit(self.page)
        self.alignScaleProportion_lineEdit.setObjectName(u"alignScaleProportion_lineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.alignScaleProportion_lineEdit)

        self.alignRotationAuto_label = QLabel(self.page)
        self.alignRotationAuto_label.setObjectName(u"alignRotationAuto_label")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.alignRotationAuto_label)

        self.alignRotationAutoValue_label = QLabel(self.page)
        self.alignRotationAutoValue_label.setObjectName(u"alignRotationAutoValue_label")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.alignRotationAutoValue_label)

        self.alignScaleAuto_label = QLabel(self.page)
        self.alignScaleAuto_label.setObjectName(u"alignScaleAuto_label")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.alignScaleAuto_label)

        self.alignScaleAutoValue_label = QLabel(self.page)
        self.alignScaleAutoValue_label.setObjectName(u"alignScaleAutoValue_label")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.alignScaleAutoValue_label)

        self.alignTranslationAuto_label = QLabel(self.page)
        self.alignTranslationAuto_label.setObjectName(u"alignTranslationAuto_label")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.alignTranslationAuto_label)

        self.alignTranslationAutoValue_label = QLabel(self.page)
        self.alignTranslationAutoValue_label.setObjectName(u"alignTranslationAutoValue_label")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.alignTranslationAutoValue_label)

        self.align_stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.formLayout_3 = QFormLayout(self.page_2)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.alignRotationManual_label = QLabel(self.page_2)
        self.alignRotationManual_label.setObjectName(u"alignRotationManual_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.alignRotationManual_label)

        self.alignRotationManual_lineEdit = QLineEdit(self.page_2)
        self.alignRotationManual_lineEdit.setObjectName(u"alignRotationManual_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.alignRotationManual_lineEdit.sizePolicy().hasHeightForWidth())
        self.alignRotationManual_lineEdit.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.alignRotationManual_lineEdit)

        self.alignScaleManual_label = QLabel(self.page_2)
        self.alignScaleManual_label.setObjectName(u"alignScaleManual_label")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.alignScaleManual_label)

        self.alignScaleManual_lineEdit = QLineEdit(self.page_2)
        self.alignScaleManual_lineEdit.setObjectName(u"alignScaleManual_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.alignScaleManual_lineEdit.sizePolicy().hasHeightForWidth())
        self.alignScaleManual_lineEdit.setSizePolicy(sizePolicy2)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.alignScaleManual_lineEdit)

        self.alignTranslationManual_label = QLabel(self.page_2)
        self.alignTranslationManual_label.setObjectName(u"alignTranslationManual_label")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.alignTranslationManual_label)

        self.alignTranslationManual_lineEdit = QLineEdit(self.page_2)
        self.alignTranslationManual_lineEdit.setObjectName(u"alignTranslationManual_lineEdit")
        sizePolicy2.setHeightForWidth(self.alignTranslationManual_lineEdit.sizePolicy().hasHeightForWidth())
        self.alignTranslationManual_lineEdit.setSizePolicy(sizePolicy2)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.alignTranslationManual_lineEdit)

        self.align_stackedWidget.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.align_stackedWidget)


        self.verticalLayout.addWidget(self.align_groupBox)


        self.retranslateUi(AlignWidget)

        self.align_stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AlignWidget)
    # setupUi

    def retranslateUi(self, AlignWidget):
        AlignWidget.setWindowTitle(QCoreApplication.translate("AlignWidget", u"Align Widget", None))
        self.align_groupBox.setTitle(QCoreApplication.translate("AlignWidget", u"Align", None))
        self.groupBox.setTitle(QCoreApplication.translate("AlignWidget", u"Mode", None))
#if QT_CONFIG(tooltip)
        self.alignAuto_radioButton.setToolTip(QCoreApplication.translate("AlignWidget", u"Use the groups and markers defined on both the mesh and the data to perform alignment.", None))
#endif // QT_CONFIG(tooltip)
        self.alignAuto_radioButton.setText(QCoreApplication.translate("AlignWidget", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.alignManual_radioButton.setToolTip(QCoreApplication.translate("AlignWidget", u"Align manually by either entering values directly or transforming with a mouse.", None))
#endif // QT_CONFIG(tooltip)
        self.alignManual_radioButton.setText(QCoreApplication.translate("AlignWidget", u"Manual", None))
        self.alignGroups_label.setText(QCoreApplication.translate("AlignWidget", u"Align groups:", None))
#if QT_CONFIG(tooltip)
        self.alignGroups_checkBox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.alignGroups_checkBox.setText("")
        self.alignMarkers_label.setText(QCoreApplication.translate("AlignWidget", u"Align markers:", None))
#if QT_CONFIG(tooltip)
        self.alignMarkers_checkBox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.alignMarkers_checkBox.setText("")
        self.alignScaleProportion_label.setText(QCoreApplication.translate("AlignWidget", u"Scale proportion:", None))
#if QT_CONFIG(tooltip)
        self.alignScaleProportion_lineEdit.setToolTip(QCoreApplication.translate("AlignWidget", u"<html><head/><body><p>With Align groups and Align markers: proportion of optimal scale to use.<br/>E.g. 0.9 makes the scale 90% of the optimal value. The allowed range of values is [0.5, 2.0].</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.alignScaleProportion_lineEdit.setText(QCoreApplication.translate("AlignWidget", u"1", None))
        self.alignRotationAuto_label.setText(QCoreApplication.translate("AlignWidget", u"Rotation:", None))
        self.alignRotationAutoValue_label.setText(QCoreApplication.translate("AlignWidget", u"[pending]", None))
        self.alignScaleAuto_label.setText(QCoreApplication.translate("AlignWidget", u"Scale:", None))
        self.alignScaleAutoValue_label.setText(QCoreApplication.translate("AlignWidget", u"[pending]", None))
        self.alignTranslationAuto_label.setText(QCoreApplication.translate("AlignWidget", u"Translation:", None))
        self.alignTranslationAutoValue_label.setText(QCoreApplication.translate("AlignWidget", u"[pending]", None))
        self.alignRotationManual_label.setText(QCoreApplication.translate("AlignWidget", u"Rotation:", None))
        self.alignRotationManual_lineEdit.setText(QCoreApplication.translate("AlignWidget", u"0, 0, 0", None))
        self.alignScaleManual_label.setText(QCoreApplication.translate("AlignWidget", u"Scale:", None))
        self.alignScaleManual_lineEdit.setText(QCoreApplication.translate("AlignWidget", u"1", None))
        self.alignTranslationManual_label.setText(QCoreApplication.translate("AlignWidget", u"Translation:", None))
        self.alignTranslationManual_lineEdit.setText(QCoreApplication.translate("AlignWidget", u"0, 0, 0", None))
    # retranslateUi

