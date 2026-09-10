# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\flash\distance_marker_flash.py
# Compiled at: 2025-06-19 12:34:48
import BigWorld, GUI, Keys, SCALEFORM, Math, logging
from gui import DEPTH_OF_VehicleMarker, InputHandler
from gui.Scaleform.daapi.view.external_components import ExternalFlashComponent, ExternalFlashSettings
from gui.Scaleform.flash_wrapper import InputKeyMode
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule
from distancemarker.flash import serializeConfigParams
from distancemarker.hooks import aih_hooks
from distancemarker.settings import clamp
from distancemarker.settings.config import g_config
from distancemarker.settings.config_param import g_configParams, DisplayMode, AnchorPosition, MarkerTarget
logger = logging.getLogger(__name__)

class _SimpleDictPool(object):

    def __init__(self):
        self.pool = []

    def __getitem__(self, item):
        return self.pool[item]

    def ensureLength(self, length):
        lackingCount = length - len(self.pool)
        if lackingCount <= 0:
            return
        for i in range(lackingCount):
            self.pool.append({})


class _ConfigState(object):

    def __init__(self, distanceMarker):
        self._distanceMarker = distanceMarker
        self.currentHorizontalAnchorOffset = g_configParams.anchorHorizontalOffset()
        self.currentVerticalAnchorOffset = -1 * g_configParams.anchorVerticalOffset()
        self.isDisplayingMarkers = g_configParams.displayMode() == DisplayMode.ALWAYS
        self._wereOffsetsEdited = False
        self._isMarkerDragging = False
        InputHandler.g_instance.onKeyDown += self._onKeyDown
        InputHandler.g_instance.onKeyUp += self._onKeyUp

    def _onKeyDown(self, event):
        if g_configParams.displayMode() == DisplayMode.ON_ALT_PRESSED:
            self.isDisplayingMarkers = event.isAltDown()
        cursor = GUI.mcursor()
        isOffsetChangeAllowed = not g_configParams.lockPositionOffsets()
        if self.isDisplayingMarkers and isOffsetChangeAllowed and event.isCtrlDown() and self._isLeftMouseButton(event) and cursor.inWindow and cursor.inFocus:
            mouseX, mouseY = cursor.position
            screenX, screenY = self._distanceMarker.toScreenPixelPosition(mouseX, mouseY)
            if self._distanceMarker.as_isPointInMarker(screenX, screenY):
                aih_hooks.onMouseEvent += self._onMarkerDragging
                self._isMarkerDragging = True

    def _onKeyUp(self, event):
        if g_configParams.displayMode() == DisplayMode.ON_ALT_PRESSED:
            self.isDisplayingMarkers = event.isAltDown()
        if self._isMarkerDragging and self._isLeftMouseButton(event):
            aih_hooks.onMouseEvent -= self._onMarkerDragging
            self._isMarkerDragging = False

    def _onMarkerDragging(self, dx, dy):
        self.currentHorizontalAnchorOffset = clamp(g_configParams.anchorHorizontalOffset.minValue, self.currentHorizontalAnchorOffset + dx, g_configParams.anchorHorizontalOffset.maxValue)
        self.currentVerticalAnchorOffset = clamp(g_configParams.anchorVerticalOffset.minValue, self.currentVerticalAnchorOffset + dy, g_configParams.anchorVerticalOffset.maxValue)
        self._wereOffsetsEdited = True

    @staticmethod
    def _isLeftMouseButton(event):
        return event.isMouseButton() and event.key == Keys.KEY_LEFTMOUSE

    def persistParamsIfChanged(self):
        if self._wereOffsetsEdited:
            g_configParams.anchorHorizontalOffset.value = self.currentHorizontalAnchorOffset
            g_configParams.anchorVerticalOffset.value = -1 * self.currentVerticalAnchorOffset
            g_config.persistParamsSafely()

    def close(self):
        if self._isMarkerDragging:
            aih_hooks.onMouseEvent -= self._onMarkerDragging
            self._isMarkerDragging = False
        InputHandler.g_instance.onKeyDown -= self._onKeyDown
        InputHandler.g_instance.onKeyUp -= self._onKeyUp


class DistanceMarkerFlashMeta(BaseDAAPIModule):

    def as_applyConfig(self, serializedConfig):
        if self._isDAAPIInited():
            return self.flashObject.as_applyConfig(serializedConfig)

    def as_isPointInMarker(self, mouseX, mouseY):
        if self._isDAAPIInited():
            return self.flashObject.as_isPointInMarker(mouseX, mouseY)


class DistanceMarkerFlash(ExternalFlashComponent, DistanceMarkerFlashMeta):

    def __init__(self, vehicleMarkerClass):
        super(DistanceMarkerFlash, self).__init__(ExternalFlashSettings('DistanceMarkerFlash', 'DistanceMarkerFlash.swf', 'root', None))
        self._vehicleMarkerClass = vehicleMarkerClass
        self.createExternalComponent()
        self._configureApp()
        self._configState = _ConfigState(self)
        if g_configParams.anchorPosition() == AnchorPosition.TANK_MARKER:
            self._markerPositionProvider = self._vehicleMarkerPositionProvider
        elif g_configParams.anchorPosition() == AnchorPosition.TANK_CENTER:
            self._markerPositionProvider = self._vehicleCenterPositionProvider
        else:
            self._markerPositionProvider = self._vehicleBottomPositionProvider
        self._currentViewProjectionMatrix = Math.Matrix()
        self._tempMatrix = Math.Matrix()
        self._emptyList = []
        self._dictPool = _SimpleDictPool()
        screenResolution = GUI.screenResolution()
        self._currentScreenWidth = screenResolution[0]
        self._currentScreenHeight = screenResolution[1]
        self._currentFrameData = {'screenWidth': (self._currentScreenWidth), 
           'screenHeight': (self._currentScreenHeight), 
           'observedVehicles': (self._emptyList)}
        serializedConfig = serializeConfigParams()
        self.as_applyConfig(serializedConfig)
        return

    def close(self):
        self._configState.close()
        super(DistanceMarkerFlash, self).close()
        self._configState.persistParamsIfChanged()

    def _configureApp(self):
        self.movie.backgroundAlpha = 0.0
        self.movie.scaleMode = SCALEFORM.eMovieScaleMode.NO_SCALE
        self.component.wg_inputKeyMode = InputKeyMode.NO_HANDLE
        self.component.position.z = DEPTH_OF_VehicleMarker - 0.02
        self.component.focus = False
        self.component.moveFocus = False

    def py_requestFrameData(self):
        try:
            screenResolution = GUI.screenResolution()
            self._currentFrameData['screenWidth'] = self._currentScreenWidth = screenResolution[0]
            self._currentFrameData['screenHeight'] = self._currentScreenHeight = screenResolution[1]
            self._currentFrameData['observedVehicles'] = self._emptyList
            return self._requestFrameData()
        except:
            logger.warn('Error occurred on requesting frame data by DistanceMarkerFlash, safely skipping frame rendering', exc_info=True)
            self._currentFrameData['observedVehicles'] = self._emptyList
            return self._currentFrameData

    def _requestFrameData(self):
        if not self._configState.isDisplayingMarkers:
            return self._currentFrameData
        else:
            player = BigWorld.player()
            if player is None:
                return self._currentFrameData
            avatarInputHandler = player.inputHandler
            if avatarInputHandler is not None and not avatarInputHandler.isGuiVisible:
                return self._currentFrameData
            currentVehicleID = -1
            currentVehicle = player.getVehicleAttached()
            if self._isVehicleSafeToUse(currentVehicle):
                currentVehicleID = currentVehicle.id
                playerPositionProvider = currentVehicle.matrix
            elif BigWorld.camera() is not None:
                playerPositionProvider = BigWorld.camera().matrix
            else:
                return self._currentFrameData
            self._tempMatrix.set(playerPositionProvider)
            currentPlayerPosition = self._tempMatrix.translation
            self._updateViewProjectionMatrix()
            vehicles = BigWorld.player().vehicles
            self._dictPool.ensureLength(len(vehicles))
            self._currentFrameData['observedVehicles'] = [self._serializeObservedVehicle(currentPlayerPosition, vehicle, self._dictPool[poolIndex]) for poolIndex, vehicle in enumerate(vehicles) if self._shouldDisplayForVehicle(vehicle, currentVehicleID)]
            return self._currentFrameData

    def _shouldDisplayForVehicle(self, vehicle, currentVehicleID):
        if not self._isVehicleSafeToUse(vehicle) or vehicle.id == currentVehicleID:
            return False
        if not vehicle.isAlive():
            return False
        if g_configParams.markerTarget() == MarkerTarget.ALLY_AND_ENEMY:
            return True
        return BigWorld.player().team != vehicle.publicInfo['team']

    @staticmethod
    def _isVehicleSafeToUse(vehicle):
        return vehicle is not None and getattr(vehicle, 'isStarted', False)

    def _updateViewProjectionMatrix(self):
        proj = BigWorld.projection()
        aspect = BigWorld.getAspectRatio()
        self._currentViewProjectionMatrix.perspectiveProjection(proj.fov, aspect, proj.nearPlane, proj.farPlane)
        self._currentViewProjectionMatrix.preMultiply(BigWorld.camera().matrix)

    def _serializeObservedVehicle(self, currentPlayerPosition, vehicle, pooledVehicleDict):
        self._tempMatrix.set(vehicle.matrix)
        vehiclePosition = self._tempMatrix.translation
        currentDistance = (vehiclePosition - currentPlayerPosition).length
        markerPosition3d = self._markerPositionProvider(vehicle)
        projectedMarkerPosition2d, isPointOnScreen = self._projectPointWithVisibilityResult(markerPosition3d)
        x, y = self.toScreenPixelPosition(projectedMarkerPosition2d.x, projectedMarkerPosition2d.y)
        pooledVehicleDict['id'] = (
         str(vehicle.id),)
        pooledVehicleDict['currentDistance'] = (currentDistance,)
        pooledVehicleDict['x'] = (x + self._configState.currentHorizontalAnchorOffset,)
        pooledVehicleDict['y'] = (y + self._configState.currentVerticalAnchorOffset,)
        pooledVehicleDict['isVisible'] = isPointOnScreen
        return pooledVehicleDict

    def _vehicleMarkerPositionProvider(self, vehicle):
        vehicleMarkerMatrixProvider = self._vehicleMarkerClass.fetchMatrixProvider(vehicle)
        self._tempMatrix.set(vehicleMarkerMatrixProvider)
        return self._tempMatrix.translation

    def _vehicleCenterPositionProvider(self, vehicle):
        self._tempMatrix.set(vehicle.matrix)
        vehicleCenterPosition = self._tempMatrix.translation
        vehicleCenterPosition.y += 2.0
        return vehicleCenterPosition

    def _vehicleBottomPositionProvider(self, vehicle):
        self._tempMatrix.set(vehicle.matrix)
        vehicleCenterPosition = self._tempMatrix.translation
        vehicleCenterPosition.y -= 1.0
        return vehicleCenterPosition

    def _projectPointWithVisibilityResult(self, point):
        posInClip = Math.Vector4(point.x, point.y, point.z, 1)
        posInClip = self._currentViewProjectionMatrix.applyV4Point(posInClip)
        if point.lengthSquared != 0.0:
            visible = posInClip.w > 0 and -1 <= posInClip.x / posInClip.w <= 1 and -1 <= posInClip.y / posInClip.w <= 1
        else:
            visible = False
        if posInClip.w != 0:
            posInClip = posInClip.scale(1 / posInClip.w)
        return (posInClip, visible)

    def toScreenPixelPosition(self, x, y):
        normalizedX = 0.5 + 0.5 * x
        normalizedY = 0.5 - 0.5 * y
        return (
         normalizedX * self._currentScreenWidth,
         normalizedY * self._currentScreenHeight)
