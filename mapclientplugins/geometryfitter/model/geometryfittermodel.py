"""
Geometric fit model adding visualisations to github.com/ABI-Software/scaffoldfitter
"""
import os
import json

from cmlibs.maths.vectorops import add, axis_angle_to_rotation_matrix, euler_to_rotation_matrix, matrix_minor, \
    matrix_mult, rotation_matrix_to_euler, matrix_inv, identity_matrix
from cmlibs.utils.zinc.field import create_jacobian_determinant_field, determine_node_field_derivatives
from cmlibs.utils.zinc.finiteelement import evaluateFieldNodesetRange
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.utils.zinc.group import group_add_group_elements, group_add_group_nodes
from cmlibs.utils.zinc.scene import (
    scene_create_node_derivative_graphics, scene_get_selection_group, scene_create_selection_group)
from cmlibs.zinc.field import Field, FieldGroup
from cmlibs.zinc.glyph import Glyph
from cmlibs.zinc.graphics import Graphics
from cmlibs.zinc.material import Material
from cmlibs.zinc.node import Node
from cmlibs.zinc.scenefilter import Scenefilter
from cmlibs.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_WORLD
from scaffoldfitter.fitter import Fitter
from scaffoldfitter.fitterjson import decodeJSONFitterSteps


class GeometryFitterModel(object):
    """
    Geometric fit model adding visualisations to github.com/ABI-Software/scaffoldfitter
    """

    def __init__(self, input_zinc_model_file, input_zinc_data_file, location, identifier, reset_settings):
        """
        :param location: Path to folder for mapclient step name.
        """
        self._manualAlignTempInvisible = None
        self._initial_matrix = []
        self._fitter = Fitter(input_zinc_model_file, input_zinc_data_file)
        # self._fitter.setDiagnosticLevel(1)
        self._location = os.path.join(location, identifier)
        self._identifier = identifier
        self._initGraphicsModules()
        self._nodeDerivativeLabels = ['D1', 'D2', 'D3', 'D12', 'D13', 'D23', 'D123']
        self._displaySettings = {
            "displayAxes": True,
            "displayMarkerDataPoints": True,
            "displayMarkerDataNames": False,
            "displayMarkerDataProjections": True,
            "displayMarkerPoints": True,
            "displayMarkerNames": False,
            "displayDataPoints": True,
            "displayDataProjections": True,
            "displayDataProjectionPoints": False,
            "displayDataProjectionTangents": False,
            "displayNodePoints": False,
            "displayNodeNumbers": False,
            'displayNodeDerivatives': 0,  # tri-state: 0=show none, 1=show selected, 2=show all
            "displayNodeDerivativeLabels": self._nodeDerivativeLabels[0:3],
            "displayElementNumbers": False,
            "displayElementAxes": False,
            "displayLines": True,
            "displayLinesExterior": False,
            "displaySurfaces": True,
            "displaySurfacesExterior": True,
            "displaySurfacesTranslucent": True,
            "displaySurfacesWireframe": False,
            "displayZeroJacobianContours": False,
            "displaySubgroupFieldName":  None
        }
        self._loadSettings(reset_settings)
        self._isStateAlign = False
        self._alignStep = None
        self._modelTransformedCoordinateField = None
        self._alignSettingsUIUpdateCallback = None
        self._alignSettingsChangeCallback = None

    def _initGraphicsModules(self):
        context = self._fitter.getContext()
        self._materialmodule = context.getMaterialmodule()
        with ChangeManager(self._materialmodule):
            self._materialmodule.defineStandardMaterials()
            solid_blue = self._materialmodule.createMaterial()
            solid_blue.setName("solid_blue")
            solid_blue.setManaged(True)
            solid_blue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
            solid_blue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
            solid_blue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
            solid_blue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
            solid_blue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)
            trans_blue = self._materialmodule.createMaterial()
            trans_blue.setName("trans_blue")
            trans_blue.setManaged(True)
            trans_blue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [0.0, 0.2, 0.6])
            trans_blue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [0.0, 0.7, 1.0])
            trans_blue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [0.0, 0.0, 0.0])
            trans_blue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
            trans_blue.setAttributeReal(Material.ATTRIBUTE_ALPHA, 0.3)
            trans_blue.setAttributeReal(Material.ATTRIBUTE_SHININESS, 0.2)
        glyphmodule = context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()
        tessellationmodule = context.getTessellationmodule()
        defaultTessellation = tessellationmodule.getDefaultTessellation()
        defaultTessellation.setRefinementFactors([12])

    def getJsonSettingsFilename(self):
        return self._location + "-settings.json"

    def getJsonDisplaySettingsFilename(self):
        return self._location + "-display-settings.json"

    GEOMETRY_FITTER_DISPLAY_SETTINGS_ID = 'geometry fitter display settings'

    def _getOutputDisplaySettings(self):
        """
        :return: Display settings augmented with id and version information.
        """
        displaySettingsDct = {
            'id': self.GEOMETRY_FITTER_DISPLAY_SETTINGS_ID,
            'version': '1.0.0'
        }
        displaySettingsDct.update(self._displaySettings)
        return displaySettingsDct

    def _loadSettings(self, reset_settings):
        # try:
        fitSettingsFileName = self.getJsonSettingsFilename()
        if os.path.isfile(fitSettingsFileName):
            if reset_settings:
                if os.path.isfile(fitSettingsFileName):
                    os.remove(fitSettingsFileName)
            else:
                with open(fitSettingsFileName, "r") as f:
                    self._fitter.decodeSettingsJSON(f.read(), decodeJSONFitterSteps)
        # except:
        #    print('_loadSettings FitSettings EXCEPTION')
        #    raise()
        # try:
        displaySettingsFileName = self.getJsonDisplaySettingsFilename()
        if os.path.isfile(displaySettingsFileName):
            if reset_settings:
                if os.path.isfile(displaySettingsFileName):
                    os.remove(displaySettingsFileName)
            else:
                with open(displaySettingsFileName, "r") as f:
                    savedSettings = json.loads(f.read())
                    settings_id = savedSettings.get('id')
                    if settings_id is not None:
                        assert settings_id == self.GEOMETRY_FITTER_DISPLAY_SETTINGS_ID
                        assert savedSettings['version'] == '1.0.0'  # future: migrate if version changes
                        # these are not stored:
                        del savedSettings['id']
                        del savedSettings['version']
                    # migrate to tristate:
                    displayNodeDerivatives = savedSettings.get('displayNodeDerivatives')
                    if isinstance(displayNodeDerivatives, bool):
                        savedSettings['displayNodeDerivatives'] = 2 if displayNodeDerivatives else 0
                    self._displaySettings.update(savedSettings)
        # except:
        #    print('_loadSettings DisplaySettings EXCEPTION')
        #    pass

    def _saveSettings(self):
        with open(self.getJsonSettingsFilename(), "w") as f:
            f.write(self._fitter.encodeSettingsJSON())
        with open(self.getJsonDisplaySettingsFilename(), "w") as f:
            f.write(json.dumps(self._getOutputDisplaySettings(), sort_keys=False, indent=4))

    def getOutputModelFileNameStem(self):
        return self._location

    def getOutputModelFileName(self):
        return self._location + ".exf"

    def load(self):
        self._fitter.load()

    def done(self):
        self._saveSettings()
        self._fitter.run(endStep=None, modelFileNameStem=self.getOutputModelFileNameStem())
        self._fitter.writeModel(self.getOutputModelFileName())

    def getIdentifier(self):
        return self._identifier

    def getContext(self):
        return self._fitter.getContext()

    def getFitter(self):
        return self._fitter

    def getRegion(self):
        return self._fitter.getRegion()

    def getFieldmodule(self):
        return self._fitter.getFieldmodule()

    def getScene(self):
        return self._fitter.getRegion().getScene()

    def _getVisibility(self, graphicsName):
        return self._displaySettings[graphicsName]

    def _setVisibility(self, graphicsName, show):
        self._displaySettings[graphicsName] = show
        graphics = self.getScene().findGraphicsByName(graphicsName)
        if graphics.isValid():
            graphics.setVisibilityFlag(show)

    def _setMultipleGraphicsVisibility(self, graphicsPartName, show, selectMode=None):
        """
        Ensure visibility of all graphics containing graphicsPartName is set to boolean show.
        :param graphicsPartName: Part of the graphics name to match.
        :param show: Boolean to set visibility.
        :param selectMode: Optional selectMode to set at the same time.
        """
        scene = self.getScene()
        graphics = scene.getFirstGraphics()
        while graphics.isValid():
            graphicsName = graphics.getName()
            if graphicsPartName in graphicsName:
                graphics.setVisibilityFlag(show)
                if selectMode:
                    graphics.setSelectMode(selectMode)
            graphics = scene.getNextGraphics(graphics)

    def isDisplayAxes(self):
        return self._getVisibility("displayAxes")

    def setDisplayAxes(self, show):
        self._setVisibility("displayAxes", show)

    def isDisplayElementNumbers(self):
        return self._getVisibility("displayElementNumbers")

    def setDisplayElementNumbers(self, show):
        self._setVisibility("displayElementNumbers", show)

    def isDisplayLines(self):
        return self._getVisibility("displayLines")

    def setDisplayLines(self, show):
        self._setVisibility("displayLines", show)

    def isDisplayLinesExterior(self):
        return self._displaySettings["displayLinesExterior"]

    def setDisplayLinesExterior(self, isExterior):
        self._displaySettings["displayLinesExterior"] = isExterior
        lines = self.getScene().findGraphicsByName("displayLines")
        lines.setExterior(self.isDisplayLinesExterior())

    def getDisplayNodeDerivatives(self):
        """
        :return: tri-state: 0=show none, 1=show selected, 2=show all
        """
        return self._displaySettings['displayNodeDerivatives']

    def setDisplayNodeDerivatives(self, triState):
        """
        :param triState: From Qt::CheckState: 0=show none, 1=show selected, 2=show all
        """
        self._displaySettings['displayNodeDerivatives'] = triState
        with ChangeManager(self.getScene()):
            for nodeDerivativeLabel in self._nodeDerivativeLabels:
                graphicsPartName = 'displayNodeDerivatives_' + nodeDerivativeLabel
                self._setMultipleGraphicsVisibility(
                    graphicsPartName,
                    bool(triState) and self.isDisplayNodeDerivativeLabels(nodeDerivativeLabel),
                    selectMode=Graphics.SELECT_MODE_DRAW_SELECTED if (triState == 1) else Graphics.SELECT_MODE_ON)


    def isDisplayNodeDerivativeLabels(self, nodeDerivativeLabel):
        """
        :param nodeDerivativeLabel: Label from self._nodeDerivativeLabels ("D1", "D2" ...)
        """
        return nodeDerivativeLabel in self._displaySettings["displayNodeDerivativeLabels"]

    def setDisplayNodeDerivativeLabels(self, nodeDerivativeLabel, show):
        """
        :param nodeDerivativeLabel: Label from self._nodeDerivativeLabels ("D1", "D2" ...)
        """
        shown = nodeDerivativeLabel in self._displaySettings["displayNodeDerivativeLabels"]
        if show:
            if not shown:
                # keep in same order as self._nodeDerivativeLabels
                nodeDerivativeLabels = []
                for label in self._nodeDerivativeLabels:
                    if (label == nodeDerivativeLabel) or self.isDisplayNodeDerivativeLabels(label):
                        nodeDerivativeLabels.append(label)
                self._displaySettings["displayNodeDerivativeLabels"] = nodeDerivativeLabels
        else:
            if shown:
                self._displaySettings["displayNodeDerivativeLabels"].remove(nodeDerivativeLabel)
        # workaround for setting multiple visibility of d1/d2 applied to any derivatives starting with same text!
        with ChangeManager(self.getScene()):
            for tmpNodeDerivativeLabel in self._nodeDerivativeLabels:
                if nodeDerivativeLabel in tmpNodeDerivativeLabel:
                    graphicsPartName = 'displayNodeDerivatives_' + tmpNodeDerivativeLabel
                    show = tmpNodeDerivativeLabel in self._displaySettings['displayNodeDerivativeLabels']
                    self._setMultipleGraphicsVisibility(graphicsPartName, show and bool(self.getDisplayNodeDerivatives()))

    def isDisplayMarkerDataPoints(self):
        return self._getVisibility("displayMarkerDataPoints")

    def setDisplayMarkerDataPoints(self, show):
        self._setVisibility("displayMarkerDataPoints", show)

    def isDisplayMarkerDataNames(self):
        return self._getVisibility("displayMarkerDataNames")

    def setDisplayMarkerDataNames(self, show):
        self._setVisibility("displayMarkerDataNames", show)

    def isDisplayMarkerDataProjections(self):
        return self._getVisibility("displayMarkerDataProjections")

    def setDisplayMarkerDataProjections(self, show):
        self._setVisibility("displayMarkerDataProjections", show)

    def isDisplayMarkerPoints(self):
        return self._getVisibility("displayMarkerPoints")

    def setDisplayMarkerPoints(self, show):
        self._setVisibility("displayMarkerPoints", show)

    def isDisplayMarkerNames(self):
        return self._getVisibility("displayMarkerNames")

    def setDisplayMarkerNames(self, show):
        self._setVisibility("displayMarkerNames", show)

    def isDisplayDataPoints(self):
        return self._getVisibility("displayDataPoints")

    def setDisplayDataPoints(self, show):
        self._setVisibility("displayDataPoints", show)

    def isDisplayDataProjections(self):
        return self._getVisibility("displayDataProjections")

    def setDisplayDataProjections(self, show):
        self._setMultipleGraphicsVisibility("displayDataProjections", show)

    def isDisplayDataProjectionPoints(self):
        return self._getVisibility("displayDataProjectionPoints")

    def setDisplayDataProjectionPoints(self, show):
        self._setMultipleGraphicsVisibility("displayDataProjectionPoints", show)

    def isDisplayDataProjectionTangents(self):
        return self._getVisibility("displayDataProjectionTangents")

    def setDisplayDataProjectionTangents(self, show):
        self._setMultipleGraphicsVisibility("displayDataProjectionTangents", show)

    def isDisplayNodeNumbers(self):
        return self._getVisibility("displayNodeNumbers")

    def setDisplayNodeNumbers(self, show):
        self._setVisibility("displayNodeNumbers", show)

    def isDisplayNodePoints(self):
        return self._getVisibility("displayNodePoints")

    def setDisplayNodePoints(self, show):
        self._setVisibility("displayNodePoints", show)

    def isDisplaySurfaces(self):
        return self._getVisibility("displaySurfaces")

    def setDisplaySurfaces(self, show):
        self._setVisibility("displaySurfaces", show)

    def isDisplaySurfacesExterior(self):
        return self._displaySettings["displaySurfacesExterior"]

    def setDisplaySurfacesExterior(self, isExterior):
        self._displaySettings["displaySurfacesExterior"] = isExterior
        surfaces = self.getScene().findGraphicsByName("displaySurfaces")
        surfaces.setExterior(self.isDisplaySurfacesExterior() if (self._fitter.getHighestDimensionMesh().getDimension() == 3) else False)

    def isDisplaySurfacesTranslucent(self):
        return self._displaySettings["displaySurfacesTranslucent"]

    def setDisplaySurfacesTranslucent(self, isTranslucent):
        self._displaySettings["displaySurfacesTranslucent"] = isTranslucent
        surfaces = self.getScene().findGraphicsByName("displaySurfaces")
        surfacesMaterial = self._materialmodule.findMaterialByName("trans_blue" if isTranslucent else "solid_blue")
        surfaces.setMaterial(surfacesMaterial)

    def isDisplaySurfacesWireframe(self):
        return self._displaySettings["displaySurfacesWireframe"]

    def setDisplaySurfacesWireframe(self, isWireframe):
        self._displaySettings["displaySurfacesWireframe"] = isWireframe
        surfaces = self.getScene().findGraphicsByName("displaySurfaces")
        surfaces.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_WIREFRAME if isWireframe else Graphics.RENDER_POLYGON_MODE_SHADED)

    def isDisplayElementAxes(self):
        return self._getVisibility("displayElementAxes")

    def setDisplayElementAxes(self, show):
        self._setVisibility("displayElementAxes", show)

    def isDisplayZeroJacobianContours(self):
        return self._getVisibility("displayZeroJacobianContours")

    def setDisplayZeroJacobianContours(self, show):
        self._setVisibility("displayZeroJacobianContours", show)

    def needPerturbLines(self):
        """
        Return if solid surfaces are drawn with lines, requiring perturb lines to be activated.
        """
        region = self.getRegion()
        if region is None:
            return False
        mesh2d = region.getFieldmodule().findMeshByDimension(2)
        if mesh2d.getSize() == 0:
            return False
        return self.isDisplayLines() and self.isDisplaySurfaces() and not self.isDisplaySurfacesTranslucent()

    def setSelectHighlightGroup(self, group: FieldGroup):
        """
        Select and highlight objects in the group.
        :param group: FieldGroup to select, or None to clear selection.
        """
        fieldmodule = self.getFieldmodule()
        with ChangeManager(fieldmodule):
            scene = self.getScene()
            # can't use SUBELEMENT_HANDLING_MODE_FULL as some groups have been tweaked to omit some faces
            selectionGroup = scene_get_selection_group(scene)
            if group:
                if selectionGroup:
                    selectionGroup.clear()
                else:
                    selectionGroup = scene_create_selection_group(scene)
                oldSubelementHandlingMode = selectionGroup.getSubelementHandlingMode()
                selectionGroup.setSubelementHandlingMode(FieldGroup.SUBELEMENT_HANDLING_MODE_NONE)
                group_add_group_elements(selectionGroup, group, highest_dimension_only=False)
                group_add_group_nodes(selectionGroup, group, Field.DOMAIN_TYPE_DATAPOINTS)
                selectionGroup.setSubelementHandlingMode(oldSubelementHandlingMode)
            else:
                if selectionGroup:
                    selectionGroup.clear()
                    scene.setSelectionField(Field())

    def setSelectHighlightGroupByName(self, groupName):
        """
        Select and highlight objects in the group by name.
        :param groupName: Name of group to select, or None to clear selection.
        """
        fieldmodule = self.getFieldmodule()
        group = None
        if groupName:
            group = fieldmodule.findFieldByName(groupName).castGroup()
            if not group.isValid():
                group = None
        self.setSelectHighlightGroup(group)

    def createGraphics(self):
        fieldmodule = self.getFieldmodule()
        mesh = self._fitter.getHighestDimensionMesh()
        meshDimension = mesh.getDimension()
        modelCoordinates = self._fitter.getModelCoordinatesField()
        componentsCount = modelCoordinates.getNumberOfComponents()

        # prepare fields and calculate axis and glyph scaling
        with ChangeManager(fieldmodule):
            elementDerivativesField = fieldmodule.createFieldConcatenate(
                [fieldmodule.createFieldDerivative(modelCoordinates, d + 1) for d in range(meshDimension)])
            cmiss_number = fieldmodule.findFieldByName("cmiss_number")

            # get sizing for axes
            axesScale = 1.0
            nodes = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            minX, maxX = evaluateFieldNodesetRange(modelCoordinates, nodes)
            if componentsCount == 1:
                maxRange = maxX - minX
            else:
                maxRange = maxX[0] - minX[0]
                for c in range(1, componentsCount):
                    maxRange = max(maxRange, maxX[c] - minX[c])
            if maxRange > 0.0:
                while axesScale * 10.0 < maxRange:
                    axesScale *= 10.0
                while axesScale * 0.1 > maxRange:
                    axesScale *= 0.1

            # fixed width glyph size is based on average element size in all dimensions
            mesh1d = fieldmodule.findMeshByDimension(1)
            meanLineLength = 0.0
            lineCount = mesh1d.getSize()
            if lineCount > 0:
                one = fieldmodule.createFieldConstant(1.0)
                sumLineLength = fieldmodule.createFieldMeshIntegral(one, modelCoordinates, mesh1d)
                cache = fieldmodule.createFieldcache()
                result, totalLineLength = sumLineLength.evaluateReal(cache, 1)
                glyphWidth = 0.1 * totalLineLength / lineCount
                del cache
                del sumLineLength
                del one
            if (lineCount == 0) or (glyphWidth == 0.0):
                # use function of coordinate range if no elements
                if componentsCount == 1:
                    maxScale = maxX - minX
                else:
                    first = True
                    for c in range(componentsCount):
                        scale = maxX[c] - minX[c]
                        if first or (scale > maxScale):
                            maxScale = scale
                            first = False
                if maxScale == 0.0:
                    maxScale = 1.0
                glyphWidth = 0.01 * maxScale
            glyphWidthSmall = 0.25 * glyphWidth

            jacobian = None
            if meshDimension == 3:
                jacobian = create_jacobian_determinant_field(
                    modelCoordinates, self._fitter.getModelReferenceCoordinatesField())

        # make graphics
        scene = self._fitter.getRegion().getScene()
        with ChangeManager(scene):
            scene.removeAllGraphics()

            axes = scene.createGraphicsPoints()
            pointattr = axes.getGraphicspointattributes()
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_AXES_XYZ)
            pointattr.setBaseSize([axesScale, axesScale, axesScale])
            pointattr.setLabelText(1, "  " + str(axesScale))
            axes.setMaterial(self._materialmodule.findMaterialByName("grey50"))
            axes.setName("displayAxes")
            axes.setVisibilityFlag(self.isDisplayAxes())

            # marker points, projections

            markerGroup = self._fitter.getMarkerGroup()
            markerDataGroup, markerDataCoordinates, markerDataName = self._fitter.getMarkerDataFields()
            markerDataLocation, markerDataLocationCoordinates, markerDataDelta = self._fitter.getMarkerDataLocationFields()
            markerNodeGroup, markerLocation, markerCoordinates, markerName = self._fitter.getMarkerModelFields()
            markerDataLocationGroupField = self._fitter.getMarkerDataLocationGroupField()

            markerDataPoints = scene.createGraphicsPoints()
            markerDataPoints.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            if markerDataLocationGroupField:
                markerDataPoints.setSubgroupField(markerDataLocationGroupField)
            elif markerGroup:
                markerDataPoints.setSubgroupField(markerGroup)
            if markerDataCoordinates:
                markerDataPoints.setCoordinateField(markerDataCoordinates)
            pointattr = markerDataPoints.getGraphicspointattributes()
            pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_CROSS)
            markerDataPoints.setMaterial(self._materialmodule.findMaterialByName("yellow"))
            markerDataPoints.setName("displayMarkerDataPoints")
            markerDataPoints.setVisibilityFlag(self.isDisplayMarkerDataPoints())

            markerDataNames = scene.createGraphicsPoints()
            markerDataNames.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            if markerDataLocationGroupField:
                markerDataNames.setSubgroupField(markerDataLocationGroupField)
            elif markerGroup:
                markerDataNames.setSubgroupField(markerGroup)
            if markerDataCoordinates:
                markerDataNames.setCoordinateField(markerDataCoordinates)
            pointattr = markerDataNames.getGraphicspointattributes()
            pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
            if markerDataName:
                pointattr.setLabelField(markerDataName)
            markerDataNames.setMaterial(self._materialmodule.findMaterialByName("yellow"))
            markerDataNames.setName("displayMarkerDataNames")
            markerDataNames.setVisibilityFlag(self.isDisplayMarkerDataNames())

            markerDataProjections = scene.createGraphicsPoints()
            markerDataProjections.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            if markerDataLocationGroupField:
                markerDataProjections.setSubgroupField(markerDataLocationGroupField)
            elif markerGroup:
                markerDataProjections.setSubgroupField(markerGroup)
            if markerDataCoordinates:
                markerDataProjections.setCoordinateField(markerDataCoordinates)
            pointAttr = markerDataProjections.getGraphicspointattributes()
            pointAttr.setGlyphShapeType(Glyph.SHAPE_TYPE_LINE)
            pointAttr.setBaseSize([0.0, 1.0, 1.0])
            pointAttr.setScaleFactors([1.0, 0.0, 0.0])
            if markerDataDelta:
                pointAttr.setOrientationScaleField(markerDataDelta)
            markerDataProjections.setMaterial(self._materialmodule.findMaterialByName("magenta"))
            markerDataProjections.setName("displayMarkerDataProjections")
            markerDataProjections.setVisibilityFlag(self.isDisplayMarkerDataProjections())

            markerPoints = scene.createGraphicsPoints()
            markerPoints.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            if markerGroup:
                markerPoints.setSubgroupField(markerGroup)
            if markerCoordinates:
                markerPoints.setCoordinateField(markerCoordinates)
            pointattr = markerPoints.getGraphicspointattributes()
            pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_CROSS)
            markerPoints.setMaterial(self._materialmodule.findMaterialByName("white"))
            markerPoints.setName("displayMarkerPoints")
            markerPoints.setVisibilityFlag(self.isDisplayMarkerPoints())

            markerNames = scene.createGraphicsPoints()
            markerNames.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            if markerGroup:
                markerNames.setSubgroupField(markerGroup)
            if markerCoordinates:
                markerNames.setCoordinateField(markerCoordinates)
            pointattr = markerNames.getGraphicspointattributes()
            pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
            if markerName:
                pointattr.setLabelField(markerName)
            markerNames.setMaterial(self._materialmodule.findMaterialByName("white"))
            markerNames.setName("displayMarkerNames")
            markerNames.setVisibilityFlag(self.isDisplayMarkerNames())

            # data points, projections and projection points

            dataCoordinates = self._fitter.getDataCoordinatesField()
            dataPoints = scene.createGraphicsPoints()
            dataPoints.setScenecoordinatesystem(SCENECOORDINATESYSTEM_WORLD)
            dataPoints.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            if dataCoordinates:
                dataPoints.setCoordinateField(dataCoordinates)
            pointattr = dataPoints.getGraphicspointattributes()
            # pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_DIAMOND)
            # pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_POINT)
            dataPoints.setRenderPointSize(3.0)
            dataPoints.setMaterial(self._materialmodule.findMaterialByName("grey50"))
            dataPoints.setName("displayDataPoints")
            dataPoints.setVisibilityFlag(self.isDisplayDataPoints())

            for projectionMeshDimension in range(1, 3):
                dataProjectionNodeGroup = self._fitter.getDataProjectionNodeGroupField(projectionMeshDimension)
                if dataProjectionNodeGroup.isEmpty():
                    continue
                dataProjectionCoordinates = self._fitter.getDataHostCoordinatesField()
                dataProjectionDelta = self._fitter.getDataDeltaField()
                dataProjectionError = self._fitter.getDataErrorField()

                dataProjections = scene.createGraphicsPoints()
                dataProjections.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
                dataProjections.setSubgroupField(dataProjectionNodeGroup)
                if dataCoordinates:
                    dataProjections.setCoordinateField(dataCoordinates)
                pointAttr = dataProjections.getGraphicspointattributes()
                pointAttr.setGlyphShapeType(Glyph.SHAPE_TYPE_LINE)
                pointAttr.setBaseSize([0.0, 1.0, 1.0])
                pointAttr.setScaleFactors([1.0, 0.0, 0.0])
                dataProjections.setRenderLineWidth(2.0 if (projectionMeshDimension == 1) else 1.0)
                if dataProjectionDelta:
                    pointAttr.setOrientationScaleField(dataProjectionDelta)
                if dataProjectionError:
                    dataProjections.setDataField(dataProjectionError)
                spectrummodule = scene.getSpectrummodule()
                spectrum = spectrummodule.getDefaultSpectrum()
                dataProjections.setSpectrum(spectrum)
                dataProjections.setName("displayDataProjections")
                dataProjections.setVisibilityFlag(self.isDisplayDataProjections())

                dataProjectionPoints = scene.createGraphicsPoints()
                dataProjectionPoints.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
                dataProjectionPoints.setSubgroupField(dataProjectionNodeGroup)
                if dataProjectionCoordinates:
                    dataProjectionPoints.setCoordinateField(dataProjectionCoordinates)
                pointattr = dataProjectionPoints.getGraphicspointattributes()
                pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_POINT)
                dataProjectionPoints.setRenderPointSize(3.0)
                dataProjectionPoints.setMaterial(self._materialmodule.findMaterialByName("grey50"))
                dataProjectionPoints.setName("displayDataProjectionPoints")
                dataProjectionPoints.setVisibilityFlag(self.isDisplayDataProjectionPoints())

                dataProjectionTangents = scene.createGraphicsPoints()
                dataProjectionTangents.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
                dataProjectionTangents.setSubgroupField(dataProjectionNodeGroup)
                if dataProjectionCoordinates:
                    dataProjectionTangents.setCoordinateField(dataProjectionCoordinates)
                pointattr = dataProjectionTangents.getGraphicspointattributes()
                # visualize local projection tangent 1
                pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_LINE)
                pointattr.setOrientationScaleField(self._fitter.getDataProjectionOrientationField())
                pointattr.setBaseSize([glyphWidthSmall, glyphWidthSmall, glyphWidthSmall])
                pointattr.setScaleFactors([0.0, 0.0, 0.0])
                dataProjectionTangents.setMaterial(self._materialmodule.findMaterialByName("grey50"))
                dataProjectionTangents.setName("displayDataProjectionTangents")
                dataProjectionTangents.setVisibilityFlag(self.isDisplayDataProjectionTangents())

            nodePoints = scene.createGraphicsPoints()
            nodePoints.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            nodePoints.setCoordinateField(modelCoordinates)
            pointattr = nodePoints.getGraphicspointattributes()
            pointattr.setBaseSize([glyphWidth, glyphWidth, glyphWidth])
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
            nodePoints.setMaterial(self._materialmodule.findMaterialByName("white"))
            nodePoints.setName("displayNodePoints")
            nodePoints.setVisibilityFlag(self.isDisplayNodePoints())

            nodeNumbers = scene.createGraphicsPoints()
            nodeNumbers.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            nodeNumbers.setCoordinateField(modelCoordinates)
            pointattr = nodeNumbers.getGraphicspointattributes()
            pointattr.setLabelField(cmiss_number)
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
            nodeNumbers.setMaterial(self._materialmodule.findMaterialByName("green"))
            nodeNumbers.setName("displayNodeNumbers")
            nodeNumbers.setVisibilityFlag(self.isDisplayNodeNumbers())

            nodeDerivativeFields = determine_node_field_derivatives(self.getRegion(), modelCoordinates)
            scene_create_node_derivative_graphics(
                scene, modelCoordinates, nodeDerivativeFields, glyphWidth, self._nodeDerivativeLabels,
                self.getDisplayNodeDerivatives(), self._displaySettings['displayNodeDerivativeLabels'])

            elementNumbers = scene.createGraphicsPoints()
            elementNumbers.setFieldDomainType(Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION)
            elementNumbers.setCoordinateField(modelCoordinates)
            pointattr = elementNumbers.getGraphicspointattributes()
            pointattr.setLabelField(cmiss_number)
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
            elementNumbers.setMaterial(self._materialmodule.findMaterialByName("cyan"))
            elementNumbers.setName("displayElementNumbers")
            elementNumbers.setVisibilityFlag(self.isDisplayElementNumbers())

            elementAxes = scene.createGraphicsPoints()
            elementAxes.setFieldDomainType(Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION)
            elementAxes.setCoordinateField(modelCoordinates)
            pointattr = elementAxes.getGraphicspointattributes()
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_AXES_123)
            pointattr.setOrientationScaleField(elementDerivativesField)
            if meshDimension == 1:
                pointattr.setBaseSize([0.0, 2 * glyphWidth, 2 * glyphWidth])
                pointattr.setScaleFactors([0.25, 0.0, 0.0])
            elif meshDimension == 2:
                pointattr.setBaseSize([0.0, 0.0, 2 * glyphWidth])
                pointattr.setScaleFactors([0.25, 0.25, 0.0])
            else:
                pointattr.setBaseSize([0.0, 0.0, 0.0])
                pointattr.setScaleFactors([0.25, 0.25, 0.25])
            elementAxes.setMaterial(self._materialmodule.findMaterialByName("yellow"))
            elementAxes.setName("displayElementAxes")
            elementAxes.setVisibilityFlag(self.isDisplayElementAxes())

            lines = scene.createGraphicsLines()
            lines.setCoordinateField(modelCoordinates)
            lines.setExterior(self.isDisplayLinesExterior())
            lines.setName("displayLines")
            lines.setVisibilityFlag(self.isDisplayLines())

            surfaces = scene.createGraphicsSurfaces()
            surfaces.setCoordinateField(modelCoordinates)
            surfaces.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_WIREFRAME if self.isDisplaySurfacesWireframe() else Graphics.RENDER_POLYGON_MODE_SHADED)
            surfaces.setExterior(self.isDisplaySurfacesExterior() if (meshDimension == 3) else False)
            surfacesMaterial = self._materialmodule.findMaterialByName("trans_blue" if self.isDisplaySurfacesTranslucent() else "solid_blue")
            surfaces.setMaterial(surfacesMaterial)
            surfaces.setName("displaySurfaces")
            surfaces.setVisibilityFlag(self.isDisplaySurfaces())

            # zero Jacobian contours
            if jacobian:
                contours = scene.createGraphicsContours()
                contours.setCoordinateField(modelCoordinates)
                contours.setIsoscalarField(jacobian)
                contours.setListIsovalues([0.0])
                contours.setMaterial(self._materialmodule.findMaterialByName("magenta"))
                contours.setName("displayZeroJacobianContours")
                contours.setVisibilityFlag(self.isDisplayZeroJacobianContours())

            # above graphics are created without subgroup field set, and modified here:
            displaySubgroupField = self.getGraphicsDisplaySubgroupField()
            if displaySubgroupField:
                self._updateGraphicsDisplaySubgroupField(displaySubgroupField)

    def getGraphicsDisplaySubgroupField(self):
        """
        :return: Field or None.
        """
        displayGroupFieldName = self._displaySettings["displaySubgroupFieldName"]
        displayGroupField = None
        if displayGroupFieldName:
            displayGroupField = self._fitter.getFieldmodule().findFieldByName(displayGroupFieldName)
            if not displayGroupField.isValid():
                displayGroupField = None
                self._displaySettings["displaySubgroupFieldName"] = None
        return displayGroupField

    def setGraphicsDisplaySubgroupField(self, subgroupField: Field):
        """
        Set graphics to only show a particular group, or all.
        :param subgroupField: Subgroup field to set or None for none.
        """
        self._displaySettings["displaySubgroupFieldName"] = subgroupField.getName() if subgroupField else None
        self._updateGraphicsDisplaySubgroupField(subgroupField)

    def _updateGraphicsDisplaySubgroupField(self, subgroupField: Field):
        """
        Modify graphics to use the supplied subgroupField, or clear it if None.
        Currently only affects model graphics.
        :param subgroupField: The group to show, or None for whole model.
        :return:
        """
        scene = self._fitter.getRegion().getScene()
        useSubgroupField = subgroupField if subgroupField else Field()
        with ChangeManager(scene):
            graphicsNames = [
                # we need a separate flag to use subgroup for data as not always wanted
                # "displayDataPoints",
                # "displayDataProjectionPoints",
                # "displayDataProjections",
                "displayElementAxes",
                "displayElementNumbers",
                "displayLines",
                "displayNodeNumbers",
                "displayNodePoints",
                "displaySurfaces",
                "displayZeroJacobianContours"
            ]
            for graphicsName in graphicsNames:
                graphics = scene.findGraphicsByName(graphicsName)
                if graphics.isValid():
                    graphics.setSubgroupField(useSubgroupField)

    def autorangeSpectrum(self):
        scene = self._fitter.getRegion().getScene()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        spectrum.autorange(scene, Scenefilter())

    # === Align Utilities ===

    def isStateAlign(self):
        return self._isStateAlign

    def setStateAlign(self, isStateAlign):
        self._isStateAlign = isStateAlign

    def setAlignStep(self, alignStep):
        self._alignStep = alignStep

    def setAlignSettingsUIUpdateCallback(self, alignSettingsUIUpdateCallback):
        self._alignSettingsUIUpdateCallback = alignSettingsUIUpdateCallback

    def setAlignSettingsChangeCallback(self, alignSettingsChangeCallback):
        self._alignSettingsChangeCallback = alignSettingsChangeCallback

    def rotateModel(self, axis, angle):
        mat1 = axis_angle_to_rotation_matrix(axis, angle)
        mat2 = euler_to_rotation_matrix(self._alignStep.getRotation())
        newmat = matrix_mult(mat1, mat2)
        rotation = rotation_matrix_to_euler(newmat)

        self._alignStep.setRotation(rotation)
        self._setGraphicsTransformation()
        self._alignSettingsUIUpdateCallback()

    def scaleModel(self, factor):
        newScale = self._alignStep.getScale() * factor
        self._alignStep.setScale(newScale)
        self._setGraphicsTransformation()
        self._alignSettingsUIUpdateCallback()

    def offsetModel(self, relativeOffset):
        newTranslation = add(self._alignStep.getTranslation(), relativeOffset)
        self._alignStep.setTranslation(newTranslation)
        self._setGraphicsTransformation()
        self._alignSettingsUIUpdateCallback()

    def interactionStart(self):
        self._initial_matrix = self._alignStep.getTransformationMatrix() if self._alignStep.hasRun() else identity_matrix(4)
        manualAlignGraphicsNames = [
            # we need a separate flag to use manual align for data as not always wanted
            "displayMarkerDataPoints",
            "displayMarkerDataNames",
            "displayMarkerDataProjections",
            "displayDataProjectionPoints",
            "displayDataProjectionTangents",
            "displayDataProjections",
            "displayAxes",
        ]
        self._manualAlignTempInvisible = []
        for graphicsName in manualAlignGraphicsNames:
            if self._getVisibility(graphicsName):
                self._manualAlignTempInvisible.append(graphicsName)
                self._setVisibility(graphicsName, False)

    def interactionEnd(self):
        self._applyAlignSettings()
        for graphicsName in self._manualAlignTempInvisible:
            self._setVisibility(graphicsName, True)

    def _autorangeSpectrum(self):
        scene = self.getScene()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        scenefiltermodule = scene.getScenefiltermodule()
        scenefilter = scenefiltermodule.getDefaultScenefilter()
        spectrum.autorange(scene, scenefilter)

    def _applyAlignSettings(self):
        if not self._fitter.getModelCoordinatesField().isValid():
            print("Can't create transformed model coordinate field. Is problem 2-D?")
        self._alignSettingsChangeCallback()

    def _setGraphicsTransformation(self):
        """
        Establish 4x4 graphics transformation for current scaffold package.
        transformationMatrix 4x4 transformation matrix in row major format
        i.e. 4 rows of 4 values, or None to clear.
        """
        transformationMatrix = self._alignStep.getTransformationMatrix()
        scene = self.getScene()
        if transformationMatrix:
            initial_matrix_inv = matrix_inv(self._initial_matrix)
            transMat = matrix_mult(transformationMatrix, initial_matrix_inv)
            # flatten to list of 16 components for passing to Zinc
            scene.setTransformationMatrix(transMat[0] + transMat[1] + transMat[2] + transMat[3])
        else:
            scene.clearTransformation()
