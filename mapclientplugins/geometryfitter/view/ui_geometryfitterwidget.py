# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geometryfitterwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDockWidget, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

from mapclientplugins.geometryfitter.view.alignwidget import AlignWidget
from cmlibs.widgets.basesceneviewerwidget import BaseSceneviewerWidget
from cmlibs.widgets.draggablelistwidget import DraggableListWidget
from cmlibs.widgets.fieldchooserwidget import FieldChooserWidget
from mapclientplugins.geometryfitter.view.fitwidget import FitWidget
from mapclientplugins.geometryfitter.view.groupsettingswidget import GroupSettingsWidget
from mapclientplugins.geometryfitter.view.initialconfigwidget import InitialConfigWidget
from mapclientplugins.geometryfitter.view.configwidget import ConfigWidget

class Ui_GeometryFitterWidget(object):
    def setupUi(self, GeometryFitterWidget):
        if not GeometryFitterWidget.objectName():
            GeometryFitterWidget.setObjectName(u"GeometryFitterWidget")
        GeometryFitterWidget.resize(1329, 1260)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeometryFitterWidget.sizePolicy().hasHeightForWidth())
        GeometryFitterWidget.setSizePolicy(sizePolicy)
        GeometryFitterWidget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(GeometryFitterWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dockWidget = QDockWidget(GeometryFitterWidget)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy)
        self.dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable|QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.identifier_label = QLabel(self.dockWidgetContents)
        self.identifier_label.setObjectName(u"identifier_label")
        sizePolicy.setHeightForWidth(self.identifier_label.sizePolicy().hasHeightForWidth())
        self.identifier_label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.identifier_label)

        self.steps_groupBox = QGroupBox(self.dockWidgetContents)
        self.steps_groupBox.setObjectName(u"steps_groupBox")
        sizePolicy.setHeightForWidth(self.steps_groupBox.sizePolicy().hasHeightForWidth())
        self.steps_groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.steps_groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stepsAddDelete_frame = QFrame(self.steps_groupBox)
        self.stepsAddDelete_frame.setObjectName(u"stepsAddDelete_frame")
        self.stepsAddDelete_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.stepsAddDelete_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.stepsAddDelete_frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.stepsAddAlign_pushButton = QPushButton(self.stepsAddDelete_frame)
        self.stepsAddAlign_pushButton.setObjectName(u"stepsAddAlign_pushButton")

        self.horizontalLayout_10.addWidget(self.stepsAddAlign_pushButton)

        self.stepsAddConfig_pushButton = QPushButton(self.stepsAddDelete_frame)
        self.stepsAddConfig_pushButton.setObjectName(u"stepsAddConfig_pushButton")

        self.horizontalLayout_10.addWidget(self.stepsAddConfig_pushButton)

        self.stepsAddFit_pushButton = QPushButton(self.stepsAddDelete_frame)
        self.stepsAddFit_pushButton.setObjectName(u"stepsAddFit_pushButton")

        self.horizontalLayout_10.addWidget(self.stepsAddFit_pushButton)

        self.stepsDelete_pushButton = QPushButton(self.stepsAddDelete_frame)
        self.stepsDelete_pushButton.setObjectName(u"stepsDelete_pushButton")

        self.horizontalLayout_10.addWidget(self.stepsDelete_pushButton)


        self.verticalLayout_2.addWidget(self.stepsAddDelete_frame)

        self.steps_listWidget = DraggableListWidget(self.steps_groupBox)
        self.steps_listWidget.setObjectName(u"steps_listWidget")

        self.verticalLayout_2.addWidget(self.steps_listWidget)

        self.stepedit_scrollArea = QScrollArea(self.steps_groupBox)
        self.stepedit_scrollArea.setObjectName(u"stepedit_scrollArea")
        sizePolicy.setHeightForWidth(self.stepedit_scrollArea.sizePolicy().hasHeightForWidth())
        self.stepedit_scrollArea.setSizePolicy(sizePolicy)
        self.stepedit_scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.stepedit_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.stepedit_scrollArea.setWidgetResizable(True)
        self.stepedit_scrollAreaWidgetContents = QWidget()
        self.stepedit_scrollAreaWidgetContents.setObjectName(u"stepedit_scrollAreaWidgetContents")
        self.stepedit_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 435, 382))
        self.verticalLayout_3 = QVBoxLayout(self.stepedit_scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.initialConfig_widget = InitialConfigWidget(self.stepedit_scrollAreaWidgetContents)
        self.initialConfig_widget.setObjectName(u"initialConfig_widget")

        self.verticalLayout_3.addWidget(self.initialConfig_widget)

        self.align_widget = AlignWidget(self.stepedit_scrollAreaWidgetContents)
        self.align_widget.setObjectName(u"align_widget")

        self.verticalLayout_3.addWidget(self.align_widget)

        self.fit_widget = FitWidget(self.stepedit_scrollAreaWidgetContents)
        self.fit_widget.setObjectName(u"fit_widget")

        self.verticalLayout_3.addWidget(self.fit_widget)

        self.config_widget = ConfigWidget(self.stepedit_scrollAreaWidgetContents)
        self.config_widget.setObjectName(u"config_widget")

        self.verticalLayout_3.addWidget(self.config_widget)

        self.groupSettings_widget = GroupSettingsWidget(self.stepedit_scrollAreaWidgetContents)
        self.groupSettings_widget.setObjectName(u"groupSettings_widget")

        self.verticalLayout_3.addWidget(self.groupSettings_widget)

        self.stepedit_scrollArea.setWidget(self.stepedit_scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.stepedit_scrollArea)


        self.verticalLayout.addWidget(self.steps_groupBox)

        self.controls_tabWidget = QTabWidget(self.dockWidgetContents)
        self.controls_tabWidget.setObjectName(u"controls_tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.controls_tabWidget.sizePolicy().hasHeightForWidth())
        self.controls_tabWidget.setSizePolicy(sizePolicy2)
        self.display_tab = QWidget()
        self.display_tab.setObjectName(u"display_tab")
        self.verticalLayout_7 = QVBoxLayout(self.display_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.displayMisc_frame = QFrame(self.display_tab)
        self.displayMisc_frame.setObjectName(u"displayMisc_frame")
        self.displayMisc_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayMisc_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.displayMisc_frame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.displayAxes_checkBox = QCheckBox(self.displayMisc_frame)
        self.displayAxes_checkBox.setObjectName(u"displayAxes_checkBox")

        self.horizontalLayout_8.addWidget(self.displayAxes_checkBox)

        self.displayMisc_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.displayMisc_horizontalSpacer)

        self.displayGroup_label = QLabel(self.displayMisc_frame)
        self.displayGroup_label.setObjectName(u"displayGroup_label")

        self.horizontalLayout_8.addWidget(self.displayGroup_label)

        self.displayGroup_fieldChooser = FieldChooserWidget(self.displayMisc_frame)
        self.displayGroup_fieldChooser.setObjectName(u"displayGroup_fieldChooser")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.displayGroup_fieldChooser.sizePolicy().hasHeightForWidth())
        self.displayGroup_fieldChooser.setSizePolicy(sizePolicy3)

        self.horizontalLayout_8.addWidget(self.displayGroup_fieldChooser)


        self.verticalLayout_7.addWidget(self.displayMisc_frame)

        self.displayMarker_frame = QFrame(self.display_tab)
        self.displayMarker_frame.setObjectName(u"displayMarker_frame")
        self.displayMarker_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayMarker_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.displayMarker_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.displayMarkerDataNames_checkBox = QCheckBox(self.displayMarker_frame)
        self.displayMarkerDataNames_checkBox.setObjectName(u"displayMarkerDataNames_checkBox")

        self.gridLayout.addWidget(self.displayMarkerDataNames_checkBox, 0, 1, 1, 1)

        self.displayMarkerDataPoints_checkBox = QCheckBox(self.displayMarker_frame)
        self.displayMarkerDataPoints_checkBox.setObjectName(u"displayMarkerDataPoints_checkBox")

        self.gridLayout.addWidget(self.displayMarkerDataPoints_checkBox, 0, 0, 1, 1)

        self.displayMarkerNames_checkBox = QCheckBox(self.displayMarker_frame)
        self.displayMarkerNames_checkBox.setObjectName(u"displayMarkerNames_checkBox")

        self.gridLayout.addWidget(self.displayMarkerNames_checkBox, 3, 1, 1, 1)

        self.displayMarkerPoints_checkBox = QCheckBox(self.displayMarker_frame)
        self.displayMarkerPoints_checkBox.setObjectName(u"displayMarkerPoints_checkBox")

        self.gridLayout.addWidget(self.displayMarkerPoints_checkBox, 3, 0, 1, 1)

        self.displayMarkerDataProjections_checkBox = QCheckBox(self.displayMarker_frame)
        self.displayMarkerDataProjections_checkBox.setObjectName(u"displayMarkerDataProjections_checkBox")

        self.gridLayout.addWidget(self.displayMarkerDataProjections_checkBox, 0, 2, 1, 1)


        self.verticalLayout_7.addWidget(self.displayMarker_frame)

        self.displayData_frame = QFrame(self.display_tab)
        self.displayData_frame.setObjectName(u"displayData_frame")
        self.displayData_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayData_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.displayData_frame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.displayDataPoints_checkBox = QCheckBox(self.displayData_frame)
        self.displayDataPoints_checkBox.setObjectName(u"displayDataPoints_checkBox")

        self.horizontalLayout_9.addWidget(self.displayDataPoints_checkBox)

        self.displayDataProjections_checkBox = QCheckBox(self.displayData_frame)
        self.displayDataProjections_checkBox.setObjectName(u"displayDataProjections_checkBox")

        self.horizontalLayout_9.addWidget(self.displayDataProjections_checkBox)

        self.displayDataProjectionPoints_checkBox = QCheckBox(self.displayData_frame)
        self.displayDataProjectionPoints_checkBox.setObjectName(u"displayDataProjectionPoints_checkBox")

        self.horizontalLayout_9.addWidget(self.displayDataProjectionPoints_checkBox)

        self.displayData_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.displayData_horizontalSpacer)


        self.verticalLayout_7.addWidget(self.displayData_frame)

        self.displayNodes_frame = QFrame(self.display_tab)
        self.displayNodes_frame.setObjectName(u"displayNodes_frame")
        self.displayNodes_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayNodes_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.displayNodes_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.displayNodePoints_checkBox = QCheckBox(self.displayNodes_frame)
        self.displayNodePoints_checkBox.setObjectName(u"displayNodePoints_checkBox")

        self.horizontalLayout_6.addWidget(self.displayNodePoints_checkBox)

        self.displayNodeNumbers_checkBox = QCheckBox(self.displayNodes_frame)
        self.displayNodeNumbers_checkBox.setObjectName(u"displayNodeNumbers_checkBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.displayNodeNumbers_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeNumbers_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.displayNodeNumbers_checkBox)

        self.displayNodeDerivatives_checkBox = QCheckBox(self.displayNodes_frame)
        self.displayNodeDerivatives_checkBox.setObjectName(u"displayNodeDerivatives_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivatives_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivatives_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.displayNodeDerivatives_checkBox)

        self.displayNodes_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.displayNodes_horizontalSpacer)


        self.verticalLayout_7.addWidget(self.displayNodes_frame)

        self.displayNodeDerivativeLabels_frame = QFrame(self.display_tab)
        self.displayNodeDerivativeLabels_frame.setObjectName(u"displayNodeDerivativeLabels_frame")
        self.displayNodeDerivativeLabels_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayNodeDerivativeLabels_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.displayNodeDerivativeLabels_frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.displayNodeDerivativeLabels_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.displayNodeDerivativeLabels_horizontalSpacer)

        self.displayNodeDerivativeLabelsD1_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD1_checkBox.setObjectName(u"displayNodeDerivativeLabelsD1_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD1_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD1_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD1_checkBox)

        self.displayNodeDerivativeLabelsD2_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD2_checkBox.setObjectName(u"displayNodeDerivativeLabelsD2_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD2_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD2_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD2_checkBox)

        self.displayNodeDerivativeLabelsD3_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD3_checkBox.setObjectName(u"displayNodeDerivativeLabelsD3_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD3_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD3_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD3_checkBox)

        self.displayNodeDerivativeLabelsD12_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD12_checkBox.setObjectName(u"displayNodeDerivativeLabelsD12_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD12_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD12_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD12_checkBox)

        self.displayNodeDerivativeLabelsD13_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD13_checkBox.setObjectName(u"displayNodeDerivativeLabelsD13_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD13_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD13_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD13_checkBox)

        self.displayNodeDerivativeLabelsD23_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD23_checkBox.setObjectName(u"displayNodeDerivativeLabelsD23_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD23_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD23_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD23_checkBox)

        self.displayNodeDerivativeLabelsD123_checkBox = QCheckBox(self.displayNodeDerivativeLabels_frame)
        self.displayNodeDerivativeLabelsD123_checkBox.setObjectName(u"displayNodeDerivativeLabelsD123_checkBox")
        sizePolicy4.setHeightForWidth(self.displayNodeDerivativeLabelsD123_checkBox.sizePolicy().hasHeightForWidth())
        self.displayNodeDerivativeLabelsD123_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.displayNodeDerivativeLabelsD123_checkBox)


        self.verticalLayout_7.addWidget(self.displayNodeDerivativeLabels_frame)

        self.displayElements_frame = QFrame(self.display_tab)
        self.displayElements_frame.setObjectName(u"displayElements_frame")
        self.displayElements_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayElements_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.displayElements_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.displayElementNumbers_checkBox = QCheckBox(self.displayElements_frame)
        self.displayElementNumbers_checkBox.setObjectName(u"displayElementNumbers_checkBox")

        self.horizontalLayout_4.addWidget(self.displayElementNumbers_checkBox)

        self.displayElementAxes_checkBox = QCheckBox(self.displayElements_frame)
        self.displayElementAxes_checkBox.setObjectName(u"displayElementAxes_checkBox")
        sizePolicy4.setHeightForWidth(self.displayElementAxes_checkBox.sizePolicy().hasHeightForWidth())
        self.displayElementAxes_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.displayElementAxes_checkBox)

        self.displayElements_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.displayElements_horizontalSpacer)


        self.verticalLayout_7.addWidget(self.displayElements_frame)

        self.displayLines_frame = QFrame(self.display_tab)
        self.displayLines_frame.setObjectName(u"displayLines_frame")
        self.displayLines_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displayLines_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.displayLines_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.displayLines_checkBox = QCheckBox(self.displayLines_frame)
        self.displayLines_checkBox.setObjectName(u"displayLines_checkBox")

        self.horizontalLayout_5.addWidget(self.displayLines_checkBox)

        self.displayLinesExterior_checkBox = QCheckBox(self.displayLines_frame)
        self.displayLinesExterior_checkBox.setObjectName(u"displayLinesExterior_checkBox")
        sizePolicy4.setHeightForWidth(self.displayLinesExterior_checkBox.sizePolicy().hasHeightForWidth())
        self.displayLinesExterior_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.displayLinesExterior_checkBox)

        self.displayLines_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.displayLines_horizontalSpacer)


        self.verticalLayout_7.addWidget(self.displayLines_frame)

        self.displaySurfaces_frame = QFrame(self.display_tab)
        self.displaySurfaces_frame.setObjectName(u"displaySurfaces_frame")
        self.displaySurfaces_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.displaySurfaces_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.displaySurfaces_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.displaySurfaces_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfaces_checkBox.setObjectName(u"displaySurfaces_checkBox")

        self.horizontalLayout_3.addWidget(self.displaySurfaces_checkBox)

        self.displaySurfacesExterior_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesExterior_checkBox.setObjectName(u"displaySurfacesExterior_checkBox")
        sizePolicy4.setHeightForWidth(self.displaySurfacesExterior_checkBox.sizePolicy().hasHeightForWidth())
        self.displaySurfacesExterior_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.displaySurfacesExterior_checkBox)

        self.displaySurfacesTranslucent_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesTranslucent_checkBox.setObjectName(u"displaySurfacesTranslucent_checkBox")
        sizePolicy4.setHeightForWidth(self.displaySurfacesTranslucent_checkBox.sizePolicy().hasHeightForWidth())
        self.displaySurfacesTranslucent_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.displaySurfacesTranslucent_checkBox)

        self.displaySurfacesWireframe_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesWireframe_checkBox.setObjectName(u"displaySurfacesWireframe_checkBox")
        sizePolicy4.setHeightForWidth(self.displaySurfacesWireframe_checkBox.sizePolicy().hasHeightForWidth())
        self.displaySurfacesWireframe_checkBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.displaySurfacesWireframe_checkBox)

        self.displaySurfaces_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.displaySurfaces_horizontalSpacer)


        self.verticalLayout_7.addWidget(self.displaySurfaces_frame)

        self.controls_tabWidget.addTab(self.display_tab, "")
        self.error_statistics_tab = QWidget()
        self.error_statistics_tab.setObjectName(u"error_statistics_tab")
        self.verticalLayout_12 = QVBoxLayout(self.error_statistics_tab)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.error_group_frame = QFrame(self.error_statistics_tab)
        self.error_group_frame.setObjectName(u"error_group_frame")
        self.error_group_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.error_group_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_2 = QFormLayout(self.error_group_frame)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.displayRMSError_label = QLabel(self.error_group_frame)
        self.displayRMSError_label.setObjectName(u"displayRMSError_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.displayRMSError_label)

        self.displayRMSError_lineEdit = QLineEdit(self.error_group_frame)
        self.displayRMSError_lineEdit.setObjectName(u"displayRMSError_lineEdit")
        self.displayRMSError_lineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.displayRMSError_lineEdit)

        self.displayMaxError_label = QLabel(self.error_group_frame)
        self.displayMaxError_label.setObjectName(u"displayMaxError_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.displayMaxError_label)

        self.displayMaxError_lineEdit = QLineEdit(self.error_group_frame)
        self.displayMaxError_lineEdit.setObjectName(u"displayMaxError_lineEdit")
        self.displayMaxError_lineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.displayMaxError_lineEdit)


        self.verticalLayout_12.addWidget(self.error_group_frame)

        self.controls_tabWidget.addTab(self.error_statistics_tab, "")

        self.verticalLayout.addWidget(self.controls_tabWidget)

        self.bottom_frame = QFrame(self.dockWidgetContents)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.bottom_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.pushButtonDocumentation = QPushButton(self.bottom_frame)
        self.pushButtonDocumentation.setObjectName(u"pushButtonDocumentation")

        self.horizontalLayout_2.addWidget(self.pushButtonDocumentation)

        self.viewAll_pushButton = QPushButton(self.bottom_frame)
        self.viewAll_pushButton.setObjectName(u"viewAll_pushButton")

        self.horizontalLayout_2.addWidget(self.viewAll_pushButton)

        self.stdViews_pushButton = QPushButton(self.bottom_frame)
        self.stdViews_pushButton.setObjectName(u"stdViews_pushButton")

        self.horizontalLayout_2.addWidget(self.stdViews_pushButton)

        self.done_pushButton = QPushButton(self.bottom_frame)
        self.done_pushButton.setObjectName(u"done_pushButton")
        sizePolicy4.setHeightForWidth(self.done_pushButton.sizePolicy().hasHeightForWidth())
        self.done_pushButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.done_pushButton)


        self.verticalLayout.addWidget(self.bottom_frame)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.horizontalLayout.addWidget(self.dockWidget)

        self.baseSceneviewerWidget = BaseSceneviewerWidget(GeometryFitterWidget)
        self.baseSceneviewerWidget.setObjectName(u"baseSceneviewerWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.baseSceneviewerWidget.sizePolicy().hasHeightForWidth())
        self.baseSceneviewerWidget.setSizePolicy(sizePolicy5)
        self.baseSceneviewerWidget.setAutoFillBackground(False)

        self.horizontalLayout.addWidget(self.baseSceneviewerWidget)


        self.retranslateUi(GeometryFitterWidget)

        self.controls_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GeometryFitterWidget)
    # setupUi

    def retranslateUi(self, GeometryFitterWidget):
        GeometryFitterWidget.setWindowTitle(QCoreApplication.translate("GeometryFitterWidget", u"Geometry Fitter", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("GeometryFitterWidget", u"Control Panel", None))
        self.identifier_label.setText(QCoreApplication.translate("GeometryFitterWidget", u"Identifier", None))
        self.steps_groupBox.setTitle(QCoreApplication.translate("GeometryFitterWidget", u"Steps:", None))
        self.stepsAddAlign_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Add Align", None))
        self.stepsAddConfig_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Add Config", None))
        self.stepsAddFit_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Add Fit", None))
        self.stepsDelete_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Delete", None))
        self.displayAxes_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Axes", None))
        self.displayGroup_label.setText(QCoreApplication.translate("GeometryFitterWidget", u"Group:", None))
#if QT_CONFIG(tooltip)
        self.displayGroup_fieldChooser.setToolTip(QCoreApplication.translate("GeometryFitterWidget", u"<html><head/><body><p>Optional group to limit display of model and data to.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.displayMarkerDataNames_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Marker data names", None))
        self.displayMarkerDataPoints_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Marker data points", None))
        self.displayMarkerNames_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Marker names", None))
        self.displayMarkerPoints_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Marker points", None))
        self.displayMarkerDataProjections_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Marker projections", None))
        self.displayDataPoints_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Data points", None))
        self.displayDataProjections_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Data projections", None))
        self.displayDataProjectionPoints_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Data projection tangents", None))
        self.displayNodePoints_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Node points", None))
        self.displayNodeNumbers_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Node numbers", None))
        self.displayNodeDerivatives_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Node derivatives", None))
        self.displayNodeDerivativeLabelsD1_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D1", None))
        self.displayNodeDerivativeLabelsD2_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D2", None))
        self.displayNodeDerivativeLabelsD3_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D3", None))
        self.displayNodeDerivativeLabelsD12_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D12", None))
        self.displayNodeDerivativeLabelsD13_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D13", None))
        self.displayNodeDerivativeLabelsD23_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D23", None))
        self.displayNodeDerivativeLabelsD123_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"D123", None))
        self.displayElementNumbers_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Element numbers", None))
        self.displayElementAxes_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Element axes", None))
        self.displayLines_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Lines", None))
        self.displayLinesExterior_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Exterior", None))
        self.displaySurfaces_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Surfaces", None))
        self.displaySurfacesExterior_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Exterior", None))
        self.displaySurfacesTranslucent_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Transluc.", None))
        self.displaySurfacesWireframe_checkBox.setText(QCoreApplication.translate("GeometryFitterWidget", u"Wireframe", None))
        self.controls_tabWidget.setTabText(self.controls_tabWidget.indexOf(self.display_tab), QCoreApplication.translate("GeometryFitterWidget", u"Display", None))
        self.displayRMSError_label.setText(QCoreApplication.translate("GeometryFitterWidget", u"RMS error:", None))
        self.displayMaxError_label.setText(QCoreApplication.translate("GeometryFitterWidget", u"Maximum error:", None))
        self.controls_tabWidget.setTabText(self.controls_tabWidget.indexOf(self.error_statistics_tab), QCoreApplication.translate("GeometryFitterWidget", u"Error Statistics", None))
        self.pushButtonDocumentation.setText(QCoreApplication.translate("GeometryFitterWidget", u"Online Documentation", None))
        self.viewAll_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"View All", None))
        self.stdViews_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Std. Views", None))
        self.done_pushButton.setText(QCoreApplication.translate("GeometryFitterWidget", u"Done", None))
    # retranslateUi

