# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupsettingswidget.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

from cmlibs.widgets.fieldchooserwidget import FieldChooserWidget

class Ui_GroupSettingsWidget(object):
    def setupUi(self, GroupSettingsWidget):
        if not GroupSettingsWidget.objectName():
            GroupSettingsWidget.setObjectName(u"GroupSettingsWidget")
        GroupSettingsWidget.resize(365, 319)
        self.horizontalLayout = QHBoxLayout(GroupSettingsWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupSettings_groupBox = QGroupBox(GroupSettingsWidget)
        self.groupSettings_groupBox.setObjectName(u"groupSettings_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupSettings_groupBox.sizePolicy().hasHeightForWidth())
        self.groupSettings_groupBox.setSizePolicy(sizePolicy)
        self.groupSettings_Layout = QFormLayout(self.groupSettings_groupBox)
        self.groupSettings_Layout.setObjectName(u"groupSettings_Layout")
        self.groupSettings_Layout.setContentsMargins(-1, -1, -1, 0)
        self.groupSettings_label = QLabel(self.groupSettings_groupBox)
        self.groupSettings_label.setObjectName(u"groupSettings_label")

        self.groupSettings_Layout.setWidget(1, QFormLayout.LabelRole, self.groupSettings_label)

        self.groupSettings_fieldChooser = FieldChooserWidget(self.groupSettings_groupBox)
        self.groupSettings_fieldChooser.setObjectName(u"groupSettings_fieldChooser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupSettings_fieldChooser.sizePolicy().hasHeightForWidth())
        self.groupSettings_fieldChooser.setSizePolicy(sizePolicy1)

        self.groupSettings_Layout.setWidget(1, QFormLayout.FieldRole, self.groupSettings_fieldChooser)

        self.groupConfigCentralProjection_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupConfigCentralProjection_checkBox.setObjectName(u"groupConfigCentralProjection_checkBox")

        self.groupSettings_Layout.setWidget(2, QFormLayout.LabelRole, self.groupConfigCentralProjection_checkBox)

        self.groupConfigCentralProjectionSet_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupConfigCentralProjectionSet_checkBox.setObjectName(u"groupConfigCentralProjectionSet_checkBox")
        self.groupConfigCentralProjectionSet_checkBox.setTristate(False)

        self.groupSettings_Layout.setWidget(2, QFormLayout.FieldRole, self.groupConfigCentralProjectionSet_checkBox)

        self.groupConfigDataProportion_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupConfigDataProportion_checkBox.setObjectName(u"groupConfigDataProportion_checkBox")
        self.groupConfigDataProportion_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(4, QFormLayout.LabelRole, self.groupConfigDataProportion_checkBox)

        self.groupConfigDataProportion_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupConfigDataProportion_lineEdit.setObjectName(u"groupConfigDataProportion_lineEdit")

        self.groupSettings_Layout.setWidget(4, QFormLayout.FieldRole, self.groupConfigDataProportion_lineEdit)

        self.groupConfigOutlierLength_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupConfigOutlierLength_checkBox.setObjectName(u"groupConfigOutlierLength_checkBox")

        self.groupSettings_Layout.setWidget(5, QFormLayout.LabelRole, self.groupConfigOutlierLength_checkBox)

        self.groupConfigOutlierLength_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupConfigOutlierLength_lineEdit.setObjectName(u"groupConfigOutlierLength_lineEdit")

        self.groupSettings_Layout.setWidget(5, QFormLayout.FieldRole, self.groupConfigOutlierLength_lineEdit)

        self.groupFitDataWeight_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitDataWeight_checkBox.setObjectName(u"groupFitDataWeight_checkBox")
        self.groupFitDataWeight_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(7, QFormLayout.LabelRole, self.groupFitDataWeight_checkBox)

        self.groupFitDataWeight_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupFitDataWeight_lineEdit.setObjectName(u"groupFitDataWeight_lineEdit")

        self.groupSettings_Layout.setWidget(7, QFormLayout.FieldRole, self.groupFitDataWeight_lineEdit)

        self.groupFitDataSlidingFactor_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitDataSlidingFactor_checkBox.setObjectName(u"groupFitDataSlidingFactor_checkBox")
        self.groupFitDataSlidingFactor_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(8, QFormLayout.LabelRole, self.groupFitDataSlidingFactor_checkBox)

        self.groupFitDataSlidingFactor_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupFitDataSlidingFactor_lineEdit.setObjectName(u"groupFitDataSlidingFactor_lineEdit")

        self.groupSettings_Layout.setWidget(8, QFormLayout.FieldRole, self.groupFitDataSlidingFactor_lineEdit)

        self.groupFitDataStretch_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitDataStretch_checkBox.setObjectName(u"groupFitDataStretch_checkBox")
        self.groupFitDataStretch_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(9, QFormLayout.LabelRole, self.groupFitDataStretch_checkBox)

        self.groupFitDataStretchSet_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitDataStretchSet_checkBox.setObjectName(u"groupFitDataStretchSet_checkBox")

        self.groupSettings_Layout.setWidget(9, QFormLayout.FieldRole, self.groupFitDataStretchSet_checkBox)

        self.groupFitStrainPenalty_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitStrainPenalty_checkBox.setObjectName(u"groupFitStrainPenalty_checkBox")
        self.groupFitStrainPenalty_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(10, QFormLayout.LabelRole, self.groupFitStrainPenalty_checkBox)

        self.groupFitStrainPenalty_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupFitStrainPenalty_lineEdit.setObjectName(u"groupFitStrainPenalty_lineEdit")

        self.groupSettings_Layout.setWidget(10, QFormLayout.FieldRole, self.groupFitStrainPenalty_lineEdit)

        self.groupFitCurvaturePenalty_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupFitCurvaturePenalty_checkBox.setObjectName(u"groupFitCurvaturePenalty_checkBox")
        self.groupFitCurvaturePenalty_checkBox.setTristate(True)

        self.groupSettings_Layout.setWidget(11, QFormLayout.LabelRole, self.groupFitCurvaturePenalty_checkBox)

        self.groupFitCurvaturePenalty_lineEdit = QLineEdit(self.groupSettings_groupBox)
        self.groupFitCurvaturePenalty_lineEdit.setObjectName(u"groupFitCurvaturePenalty_lineEdit")

        self.groupSettings_Layout.setWidget(11, QFormLayout.FieldRole, self.groupFitCurvaturePenalty_lineEdit)

        self.groupConfigProjectionSubgroup_checkBox = QCheckBox(self.groupSettings_groupBox)
        self.groupConfigProjectionSubgroup_checkBox.setObjectName(u"groupConfigProjectionSubgroup_checkBox")

        self.groupSettings_Layout.setWidget(6, QFormLayout.LabelRole, self.groupConfigProjectionSubgroup_checkBox)

        self.groupConfigProjectionSubgroup_fieldChooser = FieldChooserWidget(self.groupSettings_groupBox)
        self.groupConfigProjectionSubgroup_fieldChooser.setObjectName(u"groupConfigProjectionSubgroup_fieldChooser")

        self.groupSettings_Layout.setWidget(6, QFormLayout.FieldRole, self.groupConfigProjectionSubgroup_fieldChooser)


        self.horizontalLayout.addWidget(self.groupSettings_groupBox)


        self.retranslateUi(GroupSettingsWidget)

        QMetaObject.connectSlotsByName(GroupSettingsWidget)
    # setupUi

    def retranslateUi(self, GroupSettingsWidget):
        GroupSettingsWidget.setWindowTitle(QCoreApplication.translate("GroupSettingsWidget", u"Group Settings", None))
        self.groupSettings_groupBox.setTitle(QCoreApplication.translate("GroupSettingsWidget", u"Group settings", None))
        self.groupSettings_label.setText(QCoreApplication.translate("GroupSettingsWidget", u"Group:", None))
        self.groupConfigCentralProjection_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Central projection:", None))
#if QT_CONFIG(tooltip)
        self.groupConfigCentralProjectionSet_checkBox.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>When set, data projections are made as if centroid of group data has been moved to centroid of model group they project on to.</p><p>Use early in fit for groups that are not near their data, but generally unset later.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupConfigCentralProjectionSet_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Set", None))
        self.groupConfigDataProportion_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Data proportion:", None))
#if QT_CONFIG(tooltip)
        self.groupConfigDataProportion_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Value from 0.0 to 1.0 giving proportion of data included in fit expression.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupConfigOutlierLength_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Outlier length:", None))
#if QT_CONFIG(tooltip)
        self.groupConfigOutlierLength_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Value for excluding outlier data points based on projection length:</p><p>&lt; 0.0: Proportion of maximum projection length to exclude e.g. -0.1 removes data points with projections within 10% of maximum.</p><p>0.0: No outlier exclusion applied.</p><p>&gt;0.0: Positive absolute projection length above which data points are excluded.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupFitDataWeight_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Data weight:", None))
#if QT_CONFIG(tooltip)
        self.groupFitDataWeight_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Real value multiplying the data projection error; higher values make the group fit closer relative to other groups</p><p>It is recommended that the default group data weight be kept at 1.0 and other weights or penalties changed relative to it.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupFitDataSlidingFactor_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Data sliding factor:", None))
#if QT_CONFIG(tooltip)
        self.groupFitDataSlidingFactor_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Factor multiplying group weight in sliding directions.</p><p>Default value 0.1 gives some sliding resistance.</p><p>Value 0.0 gives zero sliding resistance. Note a small positive value &lt;&lt; 1.0 may aid stability in the absence of other constraints.</p><p>Higher values increasingly apply stretch to span of data, but also limit movement which can cause tangential wrinkling.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupFitDataStretch_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Stretch to data:", None))
#if QT_CONFIG(tooltip)
        self.groupFitDataStretchSet_checkBox.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Default On stretches model to span of data by applying full data weight in projection tangent direction where projections have a non-negligible tangent component.</p><p>Set to Off for groups cut to variable lengths between specimens so feature is oriented but keeps reference length from model.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupFitDataStretchSet_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Set", None))
        self.groupFitStrainPenalty_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Strain penalty", None))
#if QT_CONFIG(tooltip)
        self.groupFitStrainPenalty_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Penalty on finite (Lagrange) strains relative to last reference state.</p><p>Up to 9 values for 3D model fit, 4 for 2D, 1 for 1D.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupFitCurvaturePenalty_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Curvature penalty", None))
#if QT_CONFIG(tooltip)
        self.groupFitCurvaturePenalty_lineEdit.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Penalty on curvature (gradient of displacement gradient) relative to last reference state.</p><p>Up to 9 values per coordinate component for 3D model fit, 4 for 2D, 1 for 1D.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupConfigProjectionSubgroup_checkBox.setText(QCoreApplication.translate("GroupSettingsWidget", u"Projection subgroup:", None))
#if QT_CONFIG(tooltip)
        self.groupConfigProjectionSubgroup_fieldChooser.setToolTip(QCoreApplication.translate("GroupSettingsWidget", u"<html><head/><body><p>Optional subgroup to restrict projections to its intersection with the main group.</p><p>Must be a 1-D or 2-D group and may be lower dimension than the main group.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

