# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'initialconfigwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

from cmlibs.widgets.fieldchooserwidget import FieldChooserWidget

class Ui_InitialConfigWidget(object):
    def setupUi(self, InitialConfigWidget):
        if not InitialConfigWidget.objectName():
            InitialConfigWidget.setObjectName(u"InitialConfigWidget")
        InitialConfigWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(InitialConfigWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.configInitial_groupBox = QGroupBox(InitialConfigWidget)
        self.configInitial_groupBox.setObjectName(u"configInitial_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configInitial_groupBox.sizePolicy().hasHeightForWidth())
        self.configInitial_groupBox.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.configInitial_groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.configModelCoordinates_label = QLabel(self.configInitial_groupBox)
        self.configModelCoordinates_label.setObjectName(u"configModelCoordinates_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.configModelCoordinates_label)

        self.configModelCoordinates_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configModelCoordinates_fieldChooser.setObjectName(u"configModelCoordinates_fieldChooser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.configModelCoordinates_fieldChooser.sizePolicy().hasHeightForWidth())
        self.configModelCoordinates_fieldChooser.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.configModelCoordinates_fieldChooser)

        self.configModelFitGrouplabel = QLabel(self.configInitial_groupBox)
        self.configModelFitGrouplabel.setObjectName(u"configModelFitGrouplabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.configModelFitGrouplabel)

        self.configModelFitGroup_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configModelFitGroup_fieldChooser.setObjectName(u"configModelFitGroup_fieldChooser")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.configModelFitGroup_fieldChooser)

        self.configFlattenGroup_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configFlattenGroup_fieldChooser.setObjectName(u"configFlattenGroup_fieldChooser")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.configFlattenGroup_fieldChooser)

        self.configFlattenGroup_label = QLabel(self.configInitial_groupBox)
        self.configFlattenGroup_label.setObjectName(u"configFlattenGroup_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.configFlattenGroup_label)

        self.configFibreOrientation_label = QLabel(self.configInitial_groupBox)
        self.configFibreOrientation_label.setObjectName(u"configFibreOrientation_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.configFibreOrientation_label)

        self.configFibreOrientation_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configFibreOrientation_fieldChooser.setObjectName(u"configFibreOrientation_fieldChooser")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.configFibreOrientation_fieldChooser)

        self.configDataCoordinates_label = QLabel(self.configInitial_groupBox)
        self.configDataCoordinates_label.setObjectName(u"configDataCoordinates_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.configDataCoordinates_label)

        self.configDataCoordinates_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configDataCoordinates_fieldChooser.setObjectName(u"configDataCoordinates_fieldChooser")
        sizePolicy1.setHeightForWidth(self.configDataCoordinates_fieldChooser.sizePolicy().hasHeightForWidth())
        self.configDataCoordinates_fieldChooser.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.configDataCoordinates_fieldChooser)

        self.configDiagnosticLevel_label = QLabel(self.configInitial_groupBox)
        self.configDiagnosticLevel_label.setObjectName(u"configDiagnosticLevel_label")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.configDiagnosticLevel_label)

        self.configMarkerGroup_label = QLabel(self.configInitial_groupBox)
        self.configMarkerGroup_label.setObjectName(u"configMarkerGroup_label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.configMarkerGroup_label)

        self.configMarkerGroup_fieldChooser = FieldChooserWidget(self.configInitial_groupBox)
        self.configMarkerGroup_fieldChooser.setObjectName(u"configMarkerGroup_fieldChooser")
        sizePolicy1.setHeightForWidth(self.configMarkerGroup_fieldChooser.sizePolicy().hasHeightForWidth())
        self.configMarkerGroup_fieldChooser.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.configMarkerGroup_fieldChooser)

        self.configDiagnosticLevel_spinBox = QSpinBox(self.configInitial_groupBox)
        self.configDiagnosticLevel_spinBox.setObjectName(u"configDiagnosticLevel_spinBox")
        self.configDiagnosticLevel_spinBox.setMaximum(2)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.configDiagnosticLevel_spinBox)


        self.verticalLayout.addWidget(self.configInitial_groupBox)


        self.retranslateUi(InitialConfigWidget)

        QMetaObject.connectSlotsByName(InitialConfigWidget)
    # setupUi

    def retranslateUi(self, InitialConfigWidget):
        InitialConfigWidget.setWindowTitle(QCoreApplication.translate("InitialConfigWidget", u"InitialConfig", None))
        self.configInitial_groupBox.setTitle(QCoreApplication.translate("InitialConfigWidget", u"Initial", None))
        self.configModelCoordinates_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Model coordinates:", None))
#if QT_CONFIG(tooltip)
        self.configModelCoordinates_fieldChooser.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Model coordinate field to fit.<br/>Output fitted field takes name of this field preceded by &quot;fitted &quot;.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.configModelFitGrouplabel.setText(QCoreApplication.translate("InitialConfigWidget", u"Model fit group:", None))
#if QT_CONFIG(tooltip)
        self.configModelFitGroup_fieldChooser.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Optional subset of model to fit.<br/>If not set, whole model is fitted.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.configFlattenGroup_fieldChooser.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Optional surface or line group to constrain to z = 0.</p><p>Data weight for this group scales flattening term.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.configFlattenGroup_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Flatten group:", None))
        self.configFibreOrientation_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Fibre orientation:", None))
#if QT_CONFIG(tooltip)
        self.configFibreOrientation_fieldChooser.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Optional field supplying Euler angles to rotate local 'fibre' axes on which strain and curvature penalties are applied. Clear to apply on global x, y, z axes.</p><p>Required for applying strain and curvature penalties on 2D mesh fits with 3 coordinate components.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.configDataCoordinates_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Data coordinates:", None))
#if QT_CONFIG(tooltip)
        self.configDataCoordinates_fieldChooser.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Field giving coordinates of data points.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.configDiagnosticLevel_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Diagnostic level:", None))
        self.configMarkerGroup_label.setText(QCoreApplication.translate("InitialConfigWidget", u"Marker group:", None))
#if QT_CONFIG(tooltip)
        self.configDiagnosticLevel_spinBox.setToolTip(QCoreApplication.translate("InitialConfigWidget", u"<html><head/><body><p>Increase to 1 to see diagnostic output, 2 to see more verbose optimization diagnostic output.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

