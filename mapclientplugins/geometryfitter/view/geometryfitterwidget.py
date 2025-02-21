"""
User interface for github.com/ABI-Software/scaffoldfitter
"""
import logging
import webbrowser

from PySide6 import QtCore, QtWidgets

from cmlibs.maths.vectorops import dot, magnitude, mult, normalize, sub
from cmlibs.utils.zinc.field import field_is_managed_coordinates, field_is_managed_group, \
    field_is_managed_real_1_to_3_components, field_is_managed_group_mesh, get_group_list
from cmlibs.widgets.handlers.modelalignment import ModelAlignment
from cmlibs.widgets.handlers.scenemanipulation import SceneManipulation
from cmlibs.widgets.utils import parse_real_non_negative, parse_vector_3, parse_vector, parse_real, set_wait_cursor
from cmlibs.zinc.field import Field, FieldGroup

from scaffoldfitter.fitterstepalign import FitterStepAlign
from scaffoldfitter.fitterstepconfig import FitterStepConfig
from scaffoldfitter.fitterstepfit import FitterStepFit

from mapclientplugins.geometryfitter.view.ui_geometryfitterwidget import Ui_GeometryFitterWidget

logger = logging.getLogger(__name__)


def _documentation_button_clicked():
    webbrowser.open("https://abi-mapping-tools.readthedocs.io/en/latest/mapclientplugins.geometryfitter/docs/index.html")


class GeometryFitterWidget(QtWidgets.QWidget):
    """
    User interface for github.com/ABI-Software/scaffoldfitter
    """

    def __init__(self, model, parent=None):
        """
        """
        super(GeometryFitterWidget, self).__init__(parent)
        self._ui = Ui_GeometryFitterWidget()
        self._ui.setupUi(self)
        self._ui.baseSceneviewerWidget.set_grab_focus(True)
        self._ui.baseSceneviewerWidget.set_context(model.getContext())
        self._ui.baseSceneviewerWidget.register_handler(SceneManipulation())
        self._align_model_handler = ModelAlignment(QtCore.Qt.Key.Key_A)
        self._align_model_handler.set_model(model)
        self._ui.baseSceneviewerWidget.register_handler(self._align_model_handler)
        self._model = model
        self._fitter = self._model.getFitter()
        self._currentFitterStep = self._fitter.getInitialFitterStepConfig()  # always exists
        self._callback = None
        self._setupConfigWidgets()
        self._setupGroupSettingWidgets()
        self._updateGeneralWidgets()
        self._updateDisplayWidgets()
        self._makeConnections()

    def _graphics_ready(self):
        """
        Callback for when SceneviewerWidget is initialised
        """
        self._sceneChanged()
        sceneviewer = self._ui.baseSceneviewerWidget.get_zinc_sceneviewer()
        if sceneviewer is not None:
            sceneviewer.setTransparencyMode(sceneviewer.TRANSPARENCY_MODE_SLOW)
            self._autoPerturbLines()
            sceneviewer.viewAll()

    def _sceneChanged(self):
        """
        Set custom scene from model.
        """
        self._setupConfigWidgets()
        self._setupGroupSettingWidgets()
        self._updateGroupSettingWidgets()  # needed because group is generally reset to None
        sceneviewer = self._ui.baseSceneviewerWidget.get_zinc_sceneviewer()
        if sceneviewer is not None:
            self._model.createGraphics()
            self._setupDisplayGroupWidgets()
            sceneviewer.setScene(self._model.getScene())
            self._refreshGraphics()
            groupName = self._getGroupSettingsGroupName()
            if groupName:
                self._model.setSelectHighlightGroupByName(groupName)

    def _refreshGraphics(self):
        """
        Autorange spectrum and force redraw of graphics.
        Also show up-to-date error estimates.
        """
        self._model.autorangeSpectrum()
        self._displayErrors()

    def _makeConnections(self):
        self._ui.baseSceneviewerWidget.graphics_initialized.connect(self._graphics_ready)
        self._makeConnectionsGeneral()
        self._makeConnectionsDisplay()
        self._makeConnectionsGroup()
        self._makeConnectionsConfig()
        self._makeConnectionsAlign()
        self._makeConnectionsFit()

    def registerDoneExecution(self, callback):
        self._callback = callback

    def _autoPerturbLines(self):
        """
        Enable scene viewer perturb lines iff solid surfaces are drawn with lines.
        Call whenever lines, surfaces or translucency changes
        """
        sceneviewer = self._ui.baseSceneviewerWidget.get_zinc_sceneviewer()
        if sceneviewer is not None:
            sceneviewer.setPerturbLinesFlag(self._model.needPerturbLines())

    # === general widgets ===

    def _makeConnectionsGeneral(self):
        self._ui.stepsAddAlign_pushButton.clicked.connect(self._stepsAddAlignClicked)
        self._ui.stepsAddConfig_pushButton.clicked.connect(self._stepsAddConfigClicked)
        self._ui.stepsAddFit_pushButton.clicked.connect(self._stepsAddFitClicked)
        self._ui.stepsDelete_pushButton.clicked.connect(self._stepsDeleteClicked)
        self._ui.steps_listWidget.itemClicked.connect(self._stepsListItemClicked)
        self._ui.pushButtonDocumentation.clicked.connect(_documentation_button_clicked)
        self._ui.done_pushButton.clicked.connect(self._doneButtonClicked)
        self._ui.stdViews_pushButton.clicked.connect(self._stdViewsButtonClicked)
        self._ui.viewAll_pushButton.clicked.connect(self._viewAllButtonClicked)

    def _updateGeneralWidgets(self):
        self._ui.identifier_label.setText("Identifier:  " + self._model.getIdentifier())
        self._buildStepsList()

    def _stepsAddAlignClicked(self):
        """
        Add a new align step.
        """
        self._change_fitter_step(FitterStepAlign())
        self._fitter.addFitterStep(self._currentFitterStep)  # Future: , lastFitterStep
        self._buildStepsList()

    def _stepsAddConfigClicked(self):
        """
        Add a new config step.
        """
        self._change_fitter_step(FitterStepConfig())
        self._fitter.addFitterStep(self._currentFitterStep)  # Future: , lastFitterStep
        self._buildStepsList()

    def _stepsAddFitClicked(self):
        """
        Add a new fit step.
        """
        self._change_fitter_step(FitterStepFit())
        self._fitter.addFitterStep(self._currentFitterStep)  # Future: , lastFitterStep
        self._buildStepsList()

    def runToStep(self, endStep):
        """
        Run fitter steps up to specified end step.
        """
        fitterSteps = self._fitter.getFitterSteps()
        endIndex = fitterSteps.index(endStep)
        sceneChanged = self._run_fitter(endStep, stem=self._model.getOutputModelFileNameStem())
        self._reloadSteps(sceneChanged, endIndex)

    def _reloadSteps(self, sceneChanged, endIndex):
        fitterSteps = self._fitter.getFitterSteps()
        if sceneChanged:
            for index in range(endIndex + 1, len(fitterSteps)):
                self._refreshStepItem(fitterSteps[index])
            self._sceneChanged()
        else:
            for index in range(1, endIndex + 1):
                self._refreshStepItem(fitterSteps[index])
            self._model.createGraphics()
            self._refreshGraphics()

    def _stepsDeleteClicked(self):
        """
        Delete the currently selected step, except for initial config.
        Select next step after, or before if none.
        """
        assert self._currentFitterStep is not self._fitter.getInitialFitterStepConfig()
        if self._currentFitterStep.hasRun():
            # reload and run to step before current
            fitterSteps = self._fitter.getFitterSteps()
            index = fitterSteps.index(self._currentFitterStep)
            self._fitter.run(fitterSteps[index - 1])
            self._sceneChanged()
        self._currentFitterStep = self._fitter.removeFitterStep(self._currentFitterStep)
        self._buildStepsList()

    def _change_fitter_step(self, step):
        self._currentFitterStep = step
        if isinstance(self._currentFitterStep, FitterStepAlign):
            self._model.setAlignStep(self._currentFitterStep)
            self._ui.align_widget.set_mode(step.isAlignManually())
            self._model.setAlignSettingsUIUpdateCallback(self._updateAlignWidgets)
            self._model.setAlignSettingsChangeCallback(self._alignCallback)
        else:
            self._align_model_handler.set_enabled(False)

    def _stepsListItemClicked(self, item):
        """
        Changes current step and possibly changes checked/run status.
        """
        clickedIndex = self._ui.steps_listWidget.row(item)
        fitterSteps = self._fitter.getFitterSteps()
        step = fitterSteps[clickedIndex]
        if step != self._currentFitterStep:
            self._change_fitter_step(step)
            self._updateFitterStepWidgets()
        isInitialConfig = step is self._fitter.getInitialFitterStepConfig()
        isChecked = True if isInitialConfig else (item.checkState() == QtCore.Qt.CheckState.Checked)
        if step.hasRun() != isChecked:
            if isChecked:
                endStep = step
            else:
                index = fitterSteps.index(step)
                endStep = fitterSteps[index - 1]
            self.runToStep(endStep)

    def _buildStepsList(self):
        """
        Fill the steps list widget with the list of steps
        """
        if self._ui.steps_listWidget is not None:
            self._ui.steps_listWidget.clear()  # Must clear or holds on to steps references
        firstStep = True
        fitterSteps = self._fitter.getFitterSteps()
        for step in fitterSteps:
            if isinstance(step, FitterStepAlign):
                name = "Align"
            elif isinstance(step, FitterStepConfig):
                name = "Config"
            elif isinstance(step, FitterStepFit):
                name = "Fit"
            else:
                assert False, "GeometricFitWidget.  Unknown FitterStep type"
            item = QtWidgets.QListWidgetItem(name)
            if firstStep:
                firstStep = False
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsDragEnabled)
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.CheckState.Checked if step.hasRun() else QtCore.Qt.CheckState.Unchecked)
            self._ui.steps_listWidget.addItem(item)
            if step == self._currentFitterStep:
                self._ui.steps_listWidget.setCurrentItem(item)
        self._ui.steps_listWidget.registerDropCallback(self._onStepsListItemChanged)
        self._ui.steps_listWidget.show()
        self._updateFitterStepWidgets()

    def _onStepsListItemChanged(self, prevRow, newRow):
        """
        For steps list drag and drop event.
        Update the order of steps in fitterSteps.
        """
        if newRow != prevRow:
            if newRow != 0 and prevRow != 0:
                sceneChanged, endIndex = self._fitter.moveFitterStep(prevRow, newRow, self._model.getOutputModelFileNameStem())
                self._reloadSteps(sceneChanged, endIndex)
                fitterSteps = self._fitter.getFitterSteps()
                self._currentFitterStep = fitterSteps[newRow]
            self._buildStepsList()

    def _refreshStepItem(self, step):
        """
        Update check state and selection of step in steps list view.
        :param step: Row index of item in step items.
        """
        index = self._fitter.getFitterSteps().index(step)
        item = self._ui.steps_listWidget.item(index)
        if step is not self._fitter.getInitialFitterStepConfig():
            item.setCheckState(QtCore.Qt.CheckState.Checked if step.hasRun() else QtCore.Qt.CheckState.Unchecked)
            if isinstance(step, FitterStepAlign):
                self._updateAlignWidgets(align=step)
        if step == self._currentFitterStep:
            self._ui.steps_listWidget.setCurrentItem(item)

    def _updateFitterStepWidgets(self):
        """
        Update and display widgets for currentFitterStep
        """
        isInitialConfig = self._currentFitterStep == self._fitter.getInitialFitterStepConfig()
        isAlign = isinstance(self._currentFitterStep, FitterStepAlign)
        isConfig = isinstance(self._currentFitterStep, FitterStepConfig)
        isFit = isinstance(self._currentFitterStep, FitterStepFit)
        if isAlign:
            self._updateAlignWidgets()
        elif isConfig:
            self._updateConfigWidgets()
        elif isFit:
            self._updateFitWidgets()
        self._ui.initialConfig_widget.setVisible(isInitialConfig)
        self._ui.config_widget.setVisible(False)
        self._ui.align_widget.setVisible(isAlign)
        self._ui.fit_widget.setVisible(isFit)
        self._ui.groupSettings_widget.setVisible(not isAlign)
        self._ui.stepsDelete_pushButton.setEnabled(not isInitialConfig)

    def _doneButtonClicked(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            self._model.done()
            self._ui.dockWidget.setFloating(False)
            self._callback()
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def _stdViewsButtonClicked(self):
        sceneviewer = self._ui.baseSceneviewerWidget.get_zinc_sceneviewer()
        if sceneviewer is not None:
            result, eyePosition, lookatPosition, upVector = sceneviewer.getLookatParameters()
            upVector = normalize(upVector)
            viewVector = sub(lookatPosition, eyePosition)
            viewDistance = magnitude(viewVector)
            viewVector = normalize(viewVector)
            # viewX = dot(viewVector, [1.0, 0.0, 0.0])
            viewY = dot(viewVector, [0.0, 1.0, 0.0])
            viewZ = dot(viewVector, [0.0, 0.0, 1.0])
            # upX = dot(upVector, [1.0, 0.0, 0.0])
            upY = dot(upVector, [0.0, 1.0, 0.0])
            upZ = dot(upVector, [0.0, 0.0, 1.0])
            if (viewZ < -0.999) and (upY > 0.999):
                # XY -> XZ
                viewVector = [0.0, 1.0, 0.0]
                upVector = [0.0, 0.0, 1.0]
            elif (viewY > 0.999) and (upZ > 0.999):
                # XZ -> YZ
                viewVector = [-1.0, 0.0, 0.0]
                upVector = [0.0, 0.0, 1.0]
            else:
                # XY
                viewVector = [0.0, 0.0, -1.0]
                upVector = [0.0, 1.0, 0.0]
            eyePosition = sub(lookatPosition, mult(viewVector, viewDistance))
            sceneviewer.setLookatParametersNonSkew(eyePosition, lookatPosition, upVector)

    def _viewAllButtonClicked(self):
        self._ui.baseSceneviewerWidget.view_all()

    # === display widgets ===

    def _makeConnectionsDisplay(self):
        self._ui.displayAxes_checkBox.clicked.connect(self._displayAxesClicked)
        self._ui.displayMarkerDataPoints_checkBox.clicked.connect(self._displayMarkerDataPointsClicked)
        self._ui.displayMarkerDataNames_checkBox.clicked.connect(self._displayMarkerDataNamesClicked)
        self._ui.displayMarkerDataProjections_checkBox.clicked.connect(self._displayMarkerDataProjectionsClicked)
        self._ui.displayMarkerPoints_checkBox.clicked.connect(self._displayMarkerPointsClicked)
        self._ui.displayMarkerNames_checkBox.clicked.connect(self._displayMarkerNamesClicked)
        self._ui.displayDataPoints_checkBox.clicked.connect(self._displayDataPointsClicked)
        self._ui.displayDataProjections_checkBox.clicked.connect(self._displayDataProjectionsClicked)
        self._ui.displayDataProjectionPoints_checkBox.clicked.connect(self._displayDataProjectionPointsClicked)
        self._ui.displayNodePoints_checkBox.clicked.connect(self._displayNodePointsClicked)
        self._ui.displayNodeNumbers_checkBox.clicked.connect(self._displayNodeNumbersClicked)
        self._ui.displayNodeDerivativeLabelsD1_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD1Clicked)
        self._ui.displayNodeDerivativeLabelsD2_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD2Clicked)
        self._ui.displayNodeDerivativeLabelsD3_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD3Clicked)
        self._ui.displayNodeDerivativeLabelsD12_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD12Clicked)
        self._ui.displayNodeDerivativeLabelsD13_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD13Clicked)
        self._ui.displayNodeDerivativeLabelsD23_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD23Clicked)
        self._ui.displayNodeDerivativeLabelsD123_checkBox.clicked.connect(self._displayNodeDerivativeLabelsD123Clicked)
        self._ui.displayNodeDerivatives_checkBox.clicked.connect(self._displayNodeDerivativesClicked)
        self._ui.displayElementAxes_checkBox.clicked.connect(self._displayElementAxesClicked)
        self._ui.displayElementNumbers_checkBox.clicked.connect(self._displayElementNumbersClicked)
        self._ui.displayLines_checkBox.clicked.connect(self._displayLinesClicked)
        self._ui.displayLinesExterior_checkBox.clicked.connect(self._displayLinesExteriorClicked)
        self._ui.displaySurfaces_checkBox.clicked.connect(self._displaySurfacesClicked)
        self._ui.displaySurfacesExterior_checkBox.clicked.connect(self._displaySurfacesExteriorClicked)
        self._ui.displaySurfacesTranslucent_checkBox.clicked.connect(self._displaySurfacesTranslucentClicked)
        self._ui.displaySurfacesWireframe_checkBox.clicked.connect(self._displaySurfacesWireframeClicked)
        self._ui.displayZeroJacobianContours_checkBox.clicked.connect(self._displayZeroJacobianContoursClicked)
        self._setupDisplayGroupWidgets()

    def _setupDisplayGroupWidgets(self):
        """
        Set up group display widgets and display values from fitter object.
        """
        self._ui.displayGroup_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.displayGroup_fieldChooser.setNullObjectName("- All -")
        self._ui.displayGroup_fieldChooser.setConditional(field_is_managed_group)
        displayGroupField = self._model.getGraphicsDisplaySubgroupField()
        if displayGroupField:
            self._ui.displayGroup_fieldChooser.setField(displayGroupField)

    def _updateDisplayWidgets(self):
        """
        Update display widgets to display settings for model graphics display.
        """
        self._ui.displayAxes_checkBox.setChecked(self._model.isDisplayAxes())
        self._ui.displayGroup_fieldChooser.currentIndexChanged.connect(self._displayGroupChanged)
        self._ui.displayMarkerDataPoints_checkBox.setChecked(self._model.isDisplayMarkerDataPoints())
        self._ui.displayMarkerDataNames_checkBox.setChecked(self._model.isDisplayMarkerDataNames())
        self._ui.displayMarkerDataProjections_checkBox.setChecked(self._model.isDisplayMarkerDataProjections())
        self._ui.displayMarkerPoints_checkBox.setChecked(self._model.isDisplayMarkerPoints())
        self._ui.displayMarkerNames_checkBox.setChecked(self._model.isDisplayMarkerNames())
        self._ui.displayDataPoints_checkBox.setChecked(self._model.isDisplayDataPoints())
        self._ui.displayDataProjections_checkBox.setChecked(self._model.isDisplayDataProjections())
        self._ui.displayDataProjectionPoints_checkBox.setChecked(self._model.isDisplayDataProjectionPoints())
        self._ui.displayNodePoints_checkBox.setChecked(self._model.isDisplayNodePoints())
        self._ui.displayNodeNumbers_checkBox.setChecked(self._model.isDisplayNodeNumbers())
        self._ui.displayNodeDerivativeLabelsD1_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D1"))
        self._ui.displayNodeDerivativeLabelsD2_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D2"))
        self._ui.displayNodeDerivativeLabelsD3_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D3"))
        self._ui.displayNodeDerivativeLabelsD12_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D12"))
        self._ui.displayNodeDerivativeLabelsD13_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D13"))
        self._ui.displayNodeDerivativeLabelsD23_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D23"))
        self._ui.displayNodeDerivativeLabelsD123_checkBox.setChecked(self._model.isDisplayNodeDerivativeLabels("D123"))
        self._ui.displayNodeDerivatives_checkBox.setChecked(self._model.isDisplayNodeDerivatives())
        self._ui.displayElementNumbers_checkBox.setChecked(self._model.isDisplayElementNumbers())
        self._ui.displayElementAxes_checkBox.setChecked(self._model.isDisplayElementAxes())
        self._ui.displayLines_checkBox.setChecked(self._model.isDisplayLines())
        self._ui.displayLinesExterior_checkBox.setChecked(self._model.isDisplayLinesExterior())
        self._ui.displaySurfaces_checkBox.setChecked(self._model.isDisplaySurfaces())
        self._ui.displaySurfacesExterior_checkBox.setChecked(self._model.isDisplaySurfacesExterior())
        self._ui.displaySurfacesTranslucent_checkBox.setChecked(self._model.isDisplaySurfacesTranslucent())
        self._ui.displaySurfacesWireframe_checkBox.setChecked(self._model.isDisplaySurfacesWireframe())
        self._ui.displayZeroJacobianContours_checkBox.setChecked(self._model.isDisplayZeroJacobianContours())
        self._displayErrors()

    def _displayErrors(self):
        rmsError, maxError = self._fitter.getDataRMSAndMaximumProjectionError()
        element_id, value = self._fitter.getLowestElementJacobian()
        rms_error_text = "-" if rmsError is None else f"{rmsError}"
        self._ui.displayRMSError_lineEdit.setText(rms_error_text)
        self._ui.displayRMSError_lineEdit.setCursorPosition(0)
        max_error_text = "-" if maxError is None else f"{maxError}"
        self._ui.displayMaxError_lineEdit.setText(max_error_text)
        self._ui.displayMaxError_lineEdit.setCursorPosition(0)
        minimum_jacobian_determinant = "-" if value is None else f"{value:.8g}"
        self._ui.displayMinimumJacobianDeterminant_lineEdit.setText(minimum_jacobian_determinant)
        self._ui.displayMinimumJacobianDeterminant_lineEdit.setCursorPosition(0)
        logger.info(f"RMS Error: {rms_error_text}, Max. Error: {max_error_text}, Min. Jacobian Det.: {minimum_jacobian_determinant}")

    def _displayGroupChanged(self, index):
        """
        Callback for change in display group field chooser widget.
        """
        displayGroupField = self._ui.displayGroup_fieldChooser.getField()
        self._model.setGraphicsDisplaySubgroupField(displayGroupField)

    def _displayAxesClicked(self):
        self._model.setDisplayAxes(self._ui.displayAxes_checkBox.isChecked())

    def _displayMarkerDataPointsClicked(self):
        self._model.setDisplayMarkerDataPoints(self._ui.displayMarkerDataPoints_checkBox.isChecked())

    def _displayMarkerDataNamesClicked(self):
        self._model.setDisplayMarkerDataNames(self._ui.displayMarkerDataNames_checkBox.isChecked())

    def _displayMarkerDataProjectionsClicked(self):
        self._model.setDisplayMarkerDataProjections(self._ui.displayMarkerDataProjections_checkBox.isChecked())

    def _displayMarkerPointsClicked(self):
        self._model.setDisplayMarkerPoints(self._ui.displayMarkerPoints_checkBox.isChecked())

    def _displayMarkerNamesClicked(self):
        self._model.setDisplayMarkerNames(self._ui.displayMarkerNames_checkBox.isChecked())

    def _displayDataPointsClicked(self):
        self._model.setDisplayDataPoints(self._ui.displayDataPoints_checkBox.isChecked())

    def _displayDataProjectionsClicked(self):
        self._model.setDisplayDataProjections(self._ui.displayDataProjections_checkBox.isChecked())

    def _displayDataProjectionPointsClicked(self):
        self._model.setDisplayDataProjectionPoints(self._ui.displayDataProjectionPoints_checkBox.isChecked())

    def _displayNodePointsClicked(self):
        self._model.setDisplayNodePoints(self._ui.displayNodePoints_checkBox.isChecked())

    def _displayNodeNumbersClicked(self):
        self._model.setDisplayNodeNumbers(self._ui.displayNodeNumbers_checkBox.isChecked())

    def _displayNodeDerivativesClicked(self):
        self._model.setDisplayNodeDerivatives(self._ui.displayNodeDerivatives_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD1Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D1", self._ui.displayNodeDerivativeLabelsD1_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD2Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D2", self._ui.displayNodeDerivativeLabelsD2_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD3Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D3", self._ui.displayNodeDerivativeLabelsD3_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD12Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D12", self._ui.displayNodeDerivativeLabelsD12_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD13Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D13", self._ui.displayNodeDerivativeLabelsD13_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD23Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D23", self._ui.displayNodeDerivativeLabelsD23_checkBox.isChecked())

    def _displayNodeDerivativeLabelsD123Clicked(self):
        self._model.setDisplayNodeDerivativeLabels("D123", self._ui.displayNodeDerivativeLabelsD123_checkBox.isChecked())

    def _displayElementAxesClicked(self):
        self._model.setDisplayElementAxes(self._ui.displayElementAxes_checkBox.isChecked())

    def _displayElementNumbersClicked(self):
        self._model.setDisplayElementNumbers(self._ui.displayElementNumbers_checkBox.isChecked())

    def _displayLinesClicked(self):
        self._model.setDisplayLines(self._ui.displayLines_checkBox.isChecked())
        self._autoPerturbLines()

    def _displayLinesExteriorClicked(self):
        self._model.setDisplayLinesExterior(self._ui.displayLinesExterior_checkBox.isChecked())

    def _displaySurfacesClicked(self):
        self._model.setDisplaySurfaces(self._ui.displaySurfaces_checkBox.isChecked())
        self._autoPerturbLines()

    def _displaySurfacesExteriorClicked(self):
        self._model.setDisplaySurfacesExterior(self._ui.displaySurfacesExterior_checkBox.isChecked())

    def _displaySurfacesTranslucentClicked(self):
        self._model.setDisplaySurfacesTranslucent(self._ui.displaySurfacesTranslucent_checkBox.isChecked())
        self._autoPerturbLines()

    def _displaySurfacesWireframeClicked(self):
        self._model.setDisplaySurfacesWireframe(self._ui.displaySurfacesWireframe_checkBox.isChecked())

    def _displayZeroJacobianContoursClicked(self):
        self._model.setDisplayZeroJacobianContours(self._ui.displayZeroJacobianContours_checkBox.isChecked())

    # === group setting widgets ===

    def _setupGroupSettingWidgets(self):
        """
        Set up group setting widgets and display values from fitter object.
        """
        self._ui.groupSettings_widget.groupSettings_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.groupSettings_widget.groupSettings_fieldChooser.setNullObjectName("- Default -")
        self._ui.groupSettings_widget.groupSettings_fieldChooser.setConditional(field_is_managed_group)
        self._ui.groupSettings_widget.groupSettings_fieldChooser.setField(Field())
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setNullObjectName("-")
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setConditional(field_is_managed_group)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setField(Field())

    def _makeConnectionsGroup(self):
        self._ui.groupSettings_widget.groupSettings_fieldChooser.currentIndexChanged.connect(self._groupSettingsGroupChanged)
        self._ui.groupSettings_widget.groupConfigCentralProjection_checkBox.clicked.connect(self._groupConfigCentralProjectionClicked)
        self._ui.groupSettings_widget.groupConfigCentralProjectionSet_checkBox.clicked.connect(self._groupConfigCentralProjectionSetClicked)
        self._ui.groupSettings_widget.groupConfigDataProportion_checkBox.clicked.connect(self._groupConfigDataProportionClicked)
        self._ui.groupSettings_widget.groupConfigDataProportion_lineEdit.editingFinished.connect(self._groupConfigDataProportionEntered)
        self._ui.groupSettings_widget.groupConfigOutlierLength_checkBox.clicked.connect(self._groupConfigOutlierLengthClicked)
        self._ui.groupSettings_widget.groupConfigOutlierLength_lineEdit.editingFinished.connect(self._groupConfigOutlierLengthEntered)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_checkBox.clicked.connect(self._groupConfigProjectionSubgroupClicked)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.currentIndexChanged.connect(self._groupConfigProjectionSubgroupFieldChanged)
        self._ui.groupSettings_widget.groupFitDataWeight_checkBox.clicked.connect(self._groupFitDataWeightClicked)
        self._ui.groupSettings_widget.groupFitDataWeight_lineEdit.editingFinished.connect(self._groupFitDataWeightEntered)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_checkBox.clicked.connect(self._groupFitDataSlidingFactorClicked)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_lineEdit.editingFinished.connect(self._groupFitDataSlidingFactorEntered)
        self._ui.groupSettings_widget.groupFitDataStretch_checkBox.clicked.connect(self._groupFitDataStretchClicked)
        self._ui.groupSettings_widget.groupFitDataStretchSet_checkBox.clicked.connect(self._groupFitDataStretchSetClicked)
        self._ui.groupSettings_widget.groupFitStrainPenalty_checkBox.clicked.connect(self._groupFitStrainPenaltyClicked)
        self._ui.groupSettings_widget.groupFitStrainPenalty_lineEdit.editingFinished.connect(self._groupFitStrainPenaltyEntered)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_checkBox.clicked.connect(self._groupFitCurvaturePenaltyClicked)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_lineEdit.editingFinished.connect(self._groupFitCurvaturePenaltyEntered)

    def _updateGroupSettingWidgets(self):
        """
        Update and display group setting widgets for currentFitterStep
        """
        # isAlign = isinstance(self._currentFitterStep, FitterStepAlign)
        isConfig = isinstance(self._currentFitterStep, FitterStepConfig)
        isFit = isinstance(self._currentFitterStep, FitterStepFit)
        if isConfig:
            self._updateGroupConfigCentralProjection()
            self._updateGroupConfigDataProportion()
            self._updateGroupConfigOutlierLength()
            self._updateGroupConfigProjectionSubgroup()
        elif isFit:
            self._updateGroupFitDataWeight()
            self._updateGroupFitDataSlidingFactor()
            self._updateGroupFitDataStretch()
            self._updateGroupFitStrainPenalty()
            self._updateGroupFitCurvaturePenalty()
        self._ui.groupSettings_widget.groupConfigCentralProjection_checkBox.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigCentralProjectionSet_checkBox.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigDataProportion_checkBox.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigDataProportion_lineEdit.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigOutlierLength_checkBox.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigOutlierLength_lineEdit.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_checkBox.setVisible(isConfig)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setVisible(isConfig)
        self._ui.groupSettings_widget.groupFitDataWeight_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitDataWeight_lineEdit.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_lineEdit.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitDataStretch_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitDataStretchSet_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitStrainPenalty_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitStrainPenalty_lineEdit.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_checkBox.setVisible(isFit)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_lineEdit.setVisible(isFit)

    def _groupSettingsGroupChanged(self, index):
        """
        Callback for change in group settings field chooser widget.
        """
        groupName = self._getGroupSettingsGroupName()
        self._model.setSelectHighlightGroupByName(groupName)
        self._updateGroupSettingWidgets()

    def _getGroupSettingsGroupName(self):
        group = self._ui.groupSettings_widget.groupSettings_fieldChooser.getField()
        groupName = None
        if group:
            groupName = group.getName()
        return groupName

    def _getGroupSettingDisplayState(self, func):
        groupName = self._getGroupSettingsGroupName()
        data, isLocallySet, inheritable = func(groupName)
        realFormat = "{:.4g}"
        editorDisable = True
        checkBoxTristate = False
        checkBoxState = QtCore.Qt.CheckState.Unchecked
        if isinstance(data, float):
            data = realFormat.format(data)
        elif isinstance(data, list):
            data = ", ".join(realFormat.format(e) for e in data)
        elif isinstance(data, bool):
            pass
        else:
            assert (data is None) or isinstance(data, FieldGroup)
        if inheritable:
            checkBoxTristate = True
            if not (isLocallySet or (isLocallySet is None)):
                checkBoxState = QtCore.Qt.CheckState.PartiallyChecked
        if isLocallySet and (data is not None):
            checkBoxState = QtCore.Qt.CheckState.Checked
            editorDisable = False
        return checkBoxTristate, checkBoxState, editorDisable, data

    def _updateGroupConfigCentralProjection(self):
        checkBoxTristate, checkBoxState, lineEditDisable, isConfigCentralProjectionSet = \
            self._getGroupSettingDisplayState(self._getConfig().getGroupCentralProjection)
        self._ui.groupSettings_widget.groupConfigCentralProjection_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupConfigCentralProjection_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupConfigCentralProjectionSet_checkBox.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupConfigCentralProjectionSet_checkBox.setCheckState(
            QtCore.Qt.CheckState.Checked if isConfigCentralProjectionSet else QtCore.Qt.CheckState.Unchecked)

    def _groupConfigCentralProjectionClicked(self):
        checkState = self._ui.groupSettings_widget.groupConfigCentralProjection_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getConfig().setGroupCentralProjection(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getConfig().clearGroupCentralProjection(groupName)
        else:
            self._groupConfigCentralProjectionSetClicked()
        self._updateGroupConfigCentralProjection()

    def _groupConfigCentralProjectionSetClicked(self):
        state = self._ui.groupSettings_widget.groupConfigCentralProjectionSet_checkBox.checkState()
        config = self._getConfig()
        groupName = self._getGroupSettingsGroupName()
        if config.setGroupCentralProjection(groupName, state == QtCore.Qt.CheckState.Checked):
            fitterSteps = self._fitter.getFitterSteps()
            index = fitterSteps.index(config)
            if config.hasRun() and (((index + 1) == len(fitterSteps)) or (not fitterSteps[index + 1].hasRun())):
                config.run()
                self._refreshStepItem(config)
                self._refreshGraphics()

    def _updateGroupConfigDataProportion(self):
        checkBoxTristate, checkBoxState, lineEditDisable, dataProportionStr = \
            self._getGroupSettingDisplayState(self._getConfig().getGroupDataProportion)
        self._ui.groupSettings_widget.groupConfigDataProportion_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupConfigDataProportion_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupConfigDataProportion_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupConfigDataProportion_lineEdit.setText(dataProportionStr)

    def _groupConfigDataProportionClicked(self):
        checkState = self._ui.groupSettings_widget.groupConfigDataProportion_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getConfig().setGroupDataProportion(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getConfig().clearGroupDataProportion(groupName)
        else:
            self._groupConfigDataProportionEntered()
        self._updateGroupConfigDataProportion()

    def _groupConfigDataProportionEntered(self):
        value = parse_real_non_negative(self._ui.groupSettings_widget.groupConfigDataProportion_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getConfig().setGroupDataProportion(groupName, value)
        self._updateGroupConfigDataProportion()

    def _updateGroupConfigOutlierLength(self):
        checkBoxTristate, checkBoxState, lineEditDisable, outlierLengthStr = \
            self._getGroupSettingDisplayState(self._getConfig().getGroupOutlierLength)
        self._ui.groupSettings_widget.groupConfigOutlierLength_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupConfigOutlierLength_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupConfigOutlierLength_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupConfigOutlierLength_lineEdit.setText(outlierLengthStr)

    def _groupConfigOutlierLengthClicked(self):
        checkState = self._ui.groupSettings_widget.groupConfigOutlierLength_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getConfig().setGroupOutlierLength(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getConfig().clearGroupOutlierLength(groupName)
        else:
            self._groupConfigOutlierLengthEntered()
        self._updateGroupConfigOutlierLength()

    def _groupConfigOutlierLengthEntered(self):
        value = parse_real(self._ui.groupSettings_widget.groupConfigOutlierLength_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getConfig().setGroupOutlierLength(groupName, value)
        self._updateGroupConfigOutlierLength()

    def _updateGroupConfigProjectionSubgroup(self):
        checkBoxTristate, checkBoxState, fieldchooserDisable, groupFieldOrNone = \
            self._getGroupSettingDisplayState(self._getConfig().getGroupProjectionSubgroup)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setDisabled(fieldchooserDisable)
        self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.setField(groupFieldOrNone)

    def _groupConfigProjectionSubgroupClicked(self):
        checkState = self._ui.groupSettings_widget.groupConfigProjectionSubgroup_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getConfig().setGroupProjectionSubgroup(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getConfig().clearGroupProjectionSubgroup(groupName)
        else:
            subgroup = self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.getField()
            if not subgroup:
                # get the first managed group field, if any
                fielditer = self._fitter.getFieldmodule().createFielditerator()
                field = fielditer.next()
                while field.isValid():
                    if field.isManaged() and field.castGroup().isValid():
                        subgroup = field
                        break
                    field = fielditer.next()
            self._getConfig().setGroupProjectionSubgroup(groupName, subgroup)
        self._updateGroupConfigProjectionSubgroup()

    def _groupConfigProjectionSubgroupFieldChanged(self, index):
        """
        Callback for change in group config projection subgroup field, to project onto intersected group.
        """
        field = self._ui.groupSettings_widget.groupConfigProjectionSubgroup_fieldChooser.getField()
        groupName = self._getGroupSettingsGroupName()
        self._getConfig().setGroupProjectionSubgroup(groupName, field)
        self._updateGroupConfigProjectionSubgroup()  # in case of None

    def _updateGroupFitDataWeight(self):
        checkBoxTristate, checkBoxState, lineEditDisable, dataWeightStr = \
            self._getGroupSettingDisplayState(self._getFit().getGroupDataWeight)
        self._ui.groupSettings_widget.groupFitDataWeight_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupFitDataWeight_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupFitDataWeight_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupFitDataWeight_lineEdit.setText(dataWeightStr)

    def _groupFitDataWeightClicked(self):
        checkState = self._ui.groupSettings_widget.groupFitDataWeight_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getFit().setGroupDataWeight(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getFit().clearGroupDataWeight(groupName)
        else:
            self._groupFitDataWeightEntered()
        self._updateGroupFitDataWeight()

    def _groupFitDataWeightEntered(self):
        value = parse_real_non_negative(self._ui.groupSettings_widget.groupFitDataWeight_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getFit().setGroupDataWeight(groupName, value)
        self._updateGroupFitDataWeight()

    def _updateGroupFitDataSlidingFactor(self):
        checkBoxTristate, checkBoxState, lineEditDisable, dataSlidingFactorStr = \
            self._getGroupSettingDisplayState(self._getFit().getGroupDataSlidingFactor)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupFitDataSlidingFactor_lineEdit.setText(dataSlidingFactorStr)

    def _groupFitDataSlidingFactorClicked(self):
        checkState = self._ui.groupSettings_widget.groupFitDataSlidingFactor_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getFit().setGroupDataSlidingFactor(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getFit().clearGroupDataSlidingFactor(groupName)
        else:
            self._groupFitDataSlidingFactorEntered()
        self._updateGroupFitDataSlidingFactor()

    def _groupFitDataSlidingFactorEntered(self):
        value = parse_real_non_negative(self._ui.groupSettings_widget.groupFitDataSlidingFactor_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getFit().setGroupDataSlidingFactor(groupName, value)
        self._updateGroupFitDataSlidingFactor()

    def _updateGroupFitDataStretch(self):
        checkBoxTristate, checkBoxState, lineEditDisable, isFitDataStretchSet = \
            self._getGroupSettingDisplayState(self._getFit().getGroupDataStretch)
        self._ui.groupSettings_widget.groupFitDataStretch_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupFitDataStretch_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupFitDataStretchSet_checkBox.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupFitDataStretchSet_checkBox.setCheckState(
            QtCore.Qt.CheckState.Checked if isFitDataStretchSet else QtCore.Qt.CheckState.Unchecked)

    def _groupFitDataStretchClicked(self):
        checkState = self._ui.groupSettings_widget.groupFitDataStretch_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getFit().setGroupDataStretch(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getFit().clearGroupDataStretch(groupName)
        else:
            self._groupFitDataStretchSetClicked()
        self._updateGroupFitDataStretch()

    def _groupFitDataStretchSetClicked(self):
        state = self._ui.groupSettings_widget.groupFitDataStretchSet_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        self._getFit().setGroupDataStretch(groupName, state == QtCore.Qt.CheckState.Checked)

    def _updateGroupFitStrainPenalty(self):
        checkBoxTristate, checkBoxState, lineEditDisable, dataStr = \
            self._getGroupSettingDisplayState(self._getFit().getGroupStrainPenalty)
        self._ui.groupSettings_widget.groupFitStrainPenalty_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupFitStrainPenalty_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupFitStrainPenalty_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupFitStrainPenalty_lineEdit.setText(dataStr)

    def _groupFitStrainPenaltyClicked(self):
        checkState = self._ui.groupSettings_widget.groupFitStrainPenalty_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getFit().setGroupStrainPenalty(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getFit().clearGroupStrainPenalty(groupName)
        else:
            self._groupFitStrainPenaltyEntered()
        self._updateGroupFitStrainPenalty()

    def _groupFitStrainPenaltyEntered(self):
        value = parse_vector(self._ui.groupSettings_widget.groupFitStrainPenalty_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getFit().setGroupStrainPenalty(groupName, value)
        self._updateGroupFitStrainPenalty()

    def _updateGroupFitCurvaturePenalty(self):
        checkBoxTristate, checkBoxState, lineEditDisable, dataStr = \
            self._getGroupSettingDisplayState(self._getFit().getGroupCurvaturePenalty)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_checkBox.setTristate(checkBoxTristate)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_checkBox.setCheckState(checkBoxState)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_lineEdit.setDisabled(lineEditDisable)
        self._ui.groupSettings_widget.groupFitCurvaturePenalty_lineEdit.setText(dataStr)

    def _groupFitCurvaturePenaltyClicked(self):
        checkState = self._ui.groupSettings_widget.groupFitCurvaturePenalty_checkBox.checkState()
        groupName = self._getGroupSettingsGroupName()
        if checkState == QtCore.Qt.CheckState.Unchecked:
            self._getFit().setGroupCurvaturePenalty(groupName, None)
        elif checkState == QtCore.Qt.CheckState.PartiallyChecked:
            self._getFit().clearGroupCurvaturePenalty(groupName)
        else:
            self._groupFitCurvaturePenaltyEntered()
        self._updateGroupFitCurvaturePenalty()

    def _groupFitCurvaturePenaltyEntered(self):
        value = parse_vector(self._ui.groupSettings_widget.groupFitCurvaturePenalty_lineEdit)
        groupName = self._getGroupSettingsGroupName()
        self._getFit().setGroupCurvaturePenalty(groupName, value)
        self._updateGroupFitCurvaturePenalty()

    # === config widgets ===

    def _setupConfigWidgets(self):
        """
        Set up config widgets and display values from fitter object.
        """
        self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.setConditional(field_is_managed_coordinates)
        self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.setField(self._fitter.getModelCoordinatesField())
        self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.setConditional(
            lambda field: field_is_managed_group_mesh(field, self._fitter.getHighestDimensionMesh()))
        self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.setField(self._fitter.getModelFitGroup())
        self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.setConditional(field_is_managed_real_1_to_3_components)
        self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.setField(self._fitter.getFibreField())
        self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.setConditional(field_is_managed_group)
        self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.setField(self._fitter.getFlattenGroup())
        self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.setConditional(field_is_managed_coordinates)
        self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.setField(self._fitter.getDataCoordinatesField())
        self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.setRegion(self._fitter.getRegion())
        self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.setNullObjectName("-")
        self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.setConditional(field_is_managed_group)
        self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.setField(self._fitter.getMarkerGroup())
        self._ui.initialConfig_widget.configDiagnosticLevel_spinBox.setValue(self._fitter.getDiagnosticLevel())

    def _makeConnectionsConfig(self):
        self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.currentIndexChanged.connect(self._configModelCoordinatesFieldChanged)
        self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.currentIndexChanged.connect(self._configModelFitGroupChanged)
        self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.currentIndexChanged.connect(self._configFibreOrientationFieldChanged)
        self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.currentIndexChanged.connect(self._configFlattenGroupChanged)
        self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.currentIndexChanged.connect(self._configDataCoordinatesFieldChanged)
        self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.currentIndexChanged.connect(self._configMarkerGroupChanged)
        self._ui.initialConfig_widget.configDiagnosticLevel_spinBox.valueChanged.connect(self._configDiagnosticLevelValueChanged)

    def _getConfig(self):
        config = self._currentFitterStep
        assert isinstance(config, FitterStepConfig)
        return config

    def _updateConfigWidgets(self):
        """
        Update config widgets to display settings for Fitter.
        """
        self._updateGroupSettingWidgets()

    def _configModelCoordinatesFieldChanged(self, index):
        """
        Callback for change in model coordinates field chooser widget.
        """
        field = self._ui.initialConfig_widget.configModelCoordinates_fieldChooser.getField()
        if field:
            self._fitter.setModelCoordinatesField(field)
            self._model.createGraphics()

    def _configModelFitGroupChanged(self, index):
        """
        Callback for change in model fit group field chooser widget.
        """
        self._fitter.setModelFitGroup(self._ui.initialConfig_widget.configModelFitGroup_fieldChooser.getField())

    def _configFibreOrientationFieldChanged(self, index):
        """
        Callback for change in model coordinates field chooser widget.
        """
        self._fitter.setFibreField(self._ui.initialConfig_widget.configFibreOrientation_fieldChooser.getField())

    def _configFlattenGroupChanged(self, index):
        """
        Callback for change in flatten group field chooser widget.
        """
        self._fitter.setFlattenGroup(self._ui.initialConfig_widget.configFlattenGroup_fieldChooser.getField())

    def _configDataCoordinatesFieldChanged(self, index):
        """
        Callback for change in data coordinates field chooser widget.
        """
        field = self._ui.initialConfig_widget.configDataCoordinates_fieldChooser.getField()
        if field:
            self._fitter.setDataCoordinatesField(field)
            self._model.createGraphics()

    def _configMarkerGroupChanged(self, index):
        """
        Callback for change in marker group field chooser widget.
        """
        group = self._ui.initialConfig_widget.configMarkerGroup_fieldChooser.getField()
        if group:
            self._fitter.setMarkerGroup(group)
            self._model.createGraphics()

    def _configDiagnosticLevelValueChanged(self, value):
        self._fitter.setDiagnosticLevel(value)

    # === align widgets ===

    def _makeConnectionsAlign(self):
        self._ui.align_widget.alignGroups_checkBox.clicked.connect(self._alignGroupsClicked)
        self._ui.align_widget.alignMarkers_checkBox.clicked.connect(self._alignMarkersClicked)
        self._ui.align_widget.alignRotationManual_lineEdit.editingFinished.connect(self._alignRotationEntered)
        self._ui.align_widget.alignScaleManual_lineEdit.editingFinished.connect(self._alignScaleEntered)
        self._ui.align_widget.alignScaleProportion_lineEdit.editingFinished.connect(self._alignScaleProportionEntered)
        self._ui.align_widget.alignTranslationManual_lineEdit.editingFinished.connect(self._alignTranslationEntered)
        self._ui.align_widget.modeChanged.connect(self._alignModeChanged)

    def _getAlign(self):
        align = self._currentFitterStep
        assert isinstance(align, FitterStepAlign)
        return align

    def _updateAutoWidgets(self, rotation_string, scale_string, translation_string):
        self._ui.align_widget.alignRotationAutoValue_label.setText(rotation_string)
        self._ui.align_widget.alignScaleAutoValue_label.setText(scale_string)
        self._ui.align_widget.alignTranslationAutoValue_label.setText(translation_string)

    def _updateManualWidgets(self, rotation_string, scale_string, translation_string):
        self._ui.align_widget.alignRotationManual_lineEdit.setText(rotation_string)
        self._ui.align_widget.alignScaleManual_lineEdit.setText(scale_string)
        self._ui.align_widget.alignTranslationManual_lineEdit.setText(translation_string)

    def _updateAlignWidgets(self, align=None):
        """
        Update align widgets to display parameters from current align step.
        """
        realFormat = "{:.4g}"
        default_auto_text = "[pending]"

        if align is None:
            align = self._getAlign()

        matched_markers = align.matchingMarkerCount()
        self._ui.align_widget.alignMarkers_checkBox.setText(f"({matched_markers} matched marker{'' if matched_markers == 1 else 's'}.)")
        matched_groups = align.matchingGroupCount()
        self._ui.align_widget.alignGroups_checkBox.setText(f"({matched_groups} matched group{'' if matched_groups == 1 else 's'}.)")

        self._ui.align_widget.alignGroups_checkBox.setCheckState(QtCore.Qt.CheckState.Checked if align.isAlignGroups() else QtCore.Qt.CheckState.Unchecked)
        self._ui.align_widget.alignMarkers_checkBox.setCheckState(QtCore.Qt.CheckState.Checked if align.isAlignMarkers() else QtCore.Qt.CheckState.Unchecked)

        rotation_string = ", ".join(realFormat.format(value) for value in align.getRotation())
        scale_string = realFormat.format(align.getScale())
        translation_string = ", ".join(realFormat.format(value) for value in align.getTranslation())
        self._updateAutoWidgets(
            rotation_string if align.hasRun() and not align.isAlignManually() else default_auto_text,
            scale_string if align.hasRun() and not align.isAlignManually() else default_auto_text,
            translation_string if align.hasRun() and not align.isAlignManually() else default_auto_text
        )
        self._updateManualWidgets(
            rotation_string if align.isAlignManually() else "0, 0, 0",
            scale_string if align.isAlignManually() else "1",
            translation_string if align.isAlignManually() else "0, 0, 0"
        )

        self._update_alignment_widgets(align)

    @set_wait_cursor
    def _run_fitter(self, fit_step, stem=None, reorder=False):
        return self._fitter.run(fit_step, modelFileNameStem=stem, reorder=reorder)

    def _alignCallback(self):
        self._updateAlignWidgets()
        self._applyAlignSettings(reorder=True)
        self._sceneChanged()

    def _alignGroupsClicked(self):
        state = self._ui.align_widget.alignGroups_checkBox.checkState()
        align = self._getAlign()
        align.setAlignGroups(state == QtCore.Qt.CheckState.Checked)
        self._update_alignment_widgets(align)

    def _alignMarkersClicked(self):
        state = self._ui.align_widget.alignMarkers_checkBox.checkState()
        align = self._getAlign()
        align.setAlignMarkers(state == QtCore.Qt.CheckState.Checked)
        self._update_alignment_widgets(align)

    def _update_alignment_widgets(self, align):
        self._align_model_handler.set_enabled(align.isAlignManually())

        is_align_groups = align.isAlignGroups()
        is_align_markers = align.isAlignMarkers()
        align_group_count = align.matchingGroupCount()
        align_marker_count = align.matchingMarkerCount()
        can_align_groups = align_group_count > 2
        can_align_markers = align_marker_count > 2
        can_auto_align = (align_group_count + align_marker_count) > 2

        self._ui.align_widget.alignGroups_checkBox.setEnabled(can_align_groups)
        self._ui.align_widget.alignMarkers_checkBox.setEnabled(can_align_markers)

        if can_align_groups and is_align_groups and align_marker_count > 0:
            self._ui.align_widget.alignMarkers_checkBox.setEnabled(True)
        elif can_align_groups and not is_align_groups and not can_align_markers:
            self._ui.align_widget.alignMarkers_checkBox.setChecked(False)
            align.setAlignMarkers(False)

        if can_align_markers and is_align_markers and align_group_count > 0:
            self._ui.align_widget.alignGroups_checkBox.setEnabled(True)
        elif can_align_markers and not is_align_markers and not can_align_groups:
            self._ui.align_widget.alignGroups_checkBox.setChecked(False)
            align.setAlignGroups(False)

        if can_auto_align and not can_align_markers and not can_align_groups:
            self._ui.align_widget.alignGroups_checkBox.setChecked(True)
            align.setAlignGroups(True)
            self._ui.align_widget.alignMarkers_checkBox.setChecked(True)
            align.setAlignMarkers(True)

        self._ui.align_widget.alignScaleProportion_lineEdit.setEnabled(is_align_markers or is_align_groups)

    def _alignRotationEntered(self):
        values = parse_vector_3(self._ui.align_widget.alignRotationManual_lineEdit)
        if values:
            self._getAlign().setRotation(values)
        else:
            print("Invalid model rotation Euler angles entered")
        # self._updateAlignWidgets()

    def _alignScaleEntered(self):
        value = parse_real_non_negative(self._ui.align_widget.alignScaleManual_lineEdit)
        if value > 0.0:
            self._getAlign().setScale(value)
        else:
            print("Invalid model scale entered")
        # self._updateAlignWidgets()

    def _alignScaleProportionEntered(self):
        value = parse_real_non_negative(self._ui.align_widget.alignScaleProportion_lineEdit)
        self._getAlign().setScaleProportion(value)
        # self._updateAlignWidgets()

    def _alignTranslationEntered(self):
        values = parse_vector_3(self._ui.align_widget.alignTranslationManual_lineEdit)
        if values:
            self._getAlign().setTranslation(values)
        else:
            print("Invalid model translation entered")
        # self._updateAlignWidgets()

    def _alignModeChanged(self, state):
        align = self._getAlign()
        if align.setAlignManually(state):
            self._align_model_handler.set_enabled(state)
            # No need to set scale proportion as that is only used in auto alignment mode.
            if state:
                self._alignRotationEntered()
                self._alignScaleEntered()
                self._alignTranslationEntered()
            else:
                values = parse_vector_3(self._ui.align_widget.alignRotationAutoValue_label)
                align.setRotation(values if values else [0, 0, 0])
                value = parse_real_non_negative(self._ui.align_widget.alignScaleAutoValue_label)
                align.setScale(value if value else 1)
                values = parse_vector_3(self._ui.align_widget.alignTranslationAutoValue_label)
                align.setTranslation(values if values else [0, 0, 0])

    def _applyAlignSettings(self, reorder=False):
        fitterSteps = self._fitter.getFitterSteps()
        index = fitterSteps.index(self._currentFitterStep)
        self._run_fitter(fitterSteps[index], reorder=reorder)
        for index in range(0, len(fitterSteps)):
            self._refreshStepItem(fitterSteps[index])

    # === fit widgets ===

    def _makeConnectionsFit(self):
        self._ui.fit_widget.fitIterations_spinBox.valueChanged.connect(self._fitIterationsValueChanged)
        self._ui.fit_widget.fitMaximumSubIterations_spinBox.valueChanged.connect(self._fitMaximumSubIterationsValueChanged)
        self._ui.fit_widget.fitUpdateReferenceState_checkBox.clicked.connect(self._fitUpdateReferenceStateClicked)

    def _getFit(self):
        assert isinstance(self._currentFitterStep, FitterStepFit)
        return self._currentFitterStep

    def _updateFitWidgets(self):
        """
        Update fit widgets to display parameters from fit step.
        """
        fit = self._getFit()
        self._ui.fit_widget.fitIterations_spinBox.setValue(fit.getNumberOfIterations())
        self._ui.fit_widget.fitMaximumSubIterations_spinBox.setValue(fit.getMaximumSubIterations())
        self._ui.fit_widget.fitUpdateReferenceState_checkBox.setCheckState(QtCore.Qt.CheckState.Checked if fit.isUpdateReferenceState() else QtCore.Qt.CheckState.Unchecked)
        self._updateGroupSettingWidgets()

    def _fitIterationsValueChanged(self, value):
        self._getFit().setNumberOfIterations(value)

    def _fitMaximumSubIterationsValueChanged(self, value):
        self._getFit().setMaximumSubIterations(value)

    def _fitUpdateReferenceStateClicked(self):
        state = self._ui.fit_widget.fitUpdateReferenceState_checkBox.checkState()
        self._getFit().setUpdateReferenceState(state == QtCore.Qt.CheckState.Checked)
