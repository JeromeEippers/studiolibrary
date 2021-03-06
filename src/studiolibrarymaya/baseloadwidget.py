# Copyright 2019 by Kurt Rathjen. All Rights Reserved.
#
# This library is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Lesser General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. This library is distributed in the 
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

import os
import logging

from studioqt import QtGui
from studioqt import QtCore
from studioqt import QtWidgets

import studioqt
import studiolibrary
import studiolibrarymaya
import studiolibrary.widgets

try:
    import mutils
    import mutils.gui
    import maya.cmds
except ImportError as error:
    print(error)

__all__ = [
    "BaseLoadWidget",
]

logger = logging.getLogger(__name__)



class BaseLoadWidget(QtWidgets.QWidget):
    """Base widget for creating and previewing transfer items."""

    stateChanged = QtCore.Signal(object)

    def __init__(self, item, parent=None):
        """
        :type parent: QtWidgets.QWidget
        """
        QtWidgets.QWidget.__init__(self, parent)
        self.setObjectName("studioLibraryMayaPreviewWidget")
        self.setWindowTitle("Preview Item")

        studioqt.loadUi(self)

        self._item = None
        self._iconPath = ""
        self._scriptJob = None
        self._optionsWidget = None

        self.setItem(item)
        self.loadSettings()

        try:
            self.selectionChanged()
            self.setScriptJobEnabled(True)
        except NameError as error:
            logger.exception(error)

        self.createSequenceWidget()
        self.updateThumbnailSize()
        self.setupConnections()

    def setupConnections(self):
        """Setup the connections for all the widgets."""
        self.ui.acceptButton.clicked.connect(self.accept)
        self.ui.selectionSetButton.clicked.connect(self.showSelectionSetsMenu)

        self.ui.iconToggleBoxButton.clicked.connect(self.saveSettings)
        self.ui.infoToggleBoxButton.clicked.connect(self.saveSettings)
        self.ui.optionsToggleBoxButton.clicked.connect(self.saveSettings)

        self.ui.iconToggleBoxButton.toggled[bool].connect(self.ui.iconToggleBoxFrame.setVisible)
        self.ui.infoToggleBoxButton.toggled[bool].connect(self.ui.infoToggleBoxFrame.setVisible)
        self.ui.optionsToggleBoxButton.toggled[bool].connect(self.ui.optionsToggleBoxFrame.setVisible)

    def createSequenceWidget(self):
        """
        Create a sequence widget to replace the static thumbnail widget.

        :rtype: None
        """
        self.ui.sequenceWidget = studiolibrary.widgets.ImageSequenceWidget(self)
        self.ui.sequenceWidget.setStyleSheet(self.ui.thumbnailButton.styleSheet())
        self.ui.sequenceWidget.setToolTip(self.ui.thumbnailButton.toolTip())

        self.ui.thumbnailFrame.layout().insertWidget(0, self.ui.sequenceWidget)
        self.ui.thumbnailButton.hide()
        self.ui.thumbnailButton = self.ui.sequenceWidget

        path = self.item().thumbnailPath()
        if os.path.exists(path):
            self.setIconPath(path)

        if self.item().imageSequencePath():
            self.ui.sequenceWidget.setDirname(self.item().imageSequencePath())

    def isEditable(self):
        """
        Return True if the user can edit the item.

        :rtype: bool 
        """
        item = self.item()
        editable = True

        if item and item.libraryWindow():
            editable = not item.libraryWindow().isLocked()

        return editable

    def setCaptureMenuEnabled(self, enable):
        """
        Enable the capture menu for editing the thumbnail.

        :rtype: None 
        """
        if enable:
            parent = self.item().libraryWindow()

            iconPath = self.iconPath()
            if iconPath == "":
                iconPath = self.item().thumbnailPath()

            menu = mutils.gui.ThumbnailCaptureMenu(iconPath, parent=parent)
            menu.captured.connect(self.setIconPath)
            self.ui.thumbnailButton.setMenu(menu)
        else:
            self.ui.thumbnailButton.setMenu(QtWidgets.QMenu(self))

    def item(self):
        """
        Return the library item to be created.

        :rtype: studiolibrarymaya.BaseItem
        """
        return self._item

    def _itemValueChanged(self, field, value):
        """
        :type field: str
        :type value: object
        """
        self._optionsWidget.setValue(field, value)

    def setItem(self, item):
        """
        Set the item for the preview widget.

        :type item: BaseItem
        """
        self._item = item

        if hasattr(self.ui, "titleLabel"):
            self.ui.titleLabel.setText(item.MenuName)

        if hasattr(self.ui, "iconLabel"):
            self.ui.iconLabel.setPixmap(QtGui.QPixmap(item.TypeIconPath))

        if hasattr(self.ui, "infoFrame"):
            infoWidget = studiolibrary.widgets.FormWidget(self)
            infoWidget.setSchema(item.info())
            self.ui.infoFrame.layout().addWidget(infoWidget)

        if hasattr(self.ui, "optionsFrame"):

            options = item.loadSchema()
            if options:
                item.loadValueChanged.connect(self._itemValueChanged)

                optionsWidget = studiolibrary.widgets.FormWidget(self)
                optionsWidget.setSchema(item.loadSchema())
                optionsWidget.setValidator(item.loadValidator)
                optionsWidget.setStateFromOptions(self.item().optionsFromSettings())
                self.ui.optionsFrame.layout().addWidget(optionsWidget)
                self._optionsWidget = optionsWidget
                optionsWidget.validate()
            else:
                self.ui.optionsToggleBox.setVisible(False)

    def iconPath(self):
        """
        Return the icon path to be used for the thumbnail.

        :rtype str
        """
        return self._iconPath

    def setIconPath(self, path):
        """
        Set the icon path to be used for the thumbnail.

        :type path: str
        :rtype: None
        """
        self._iconPath = path
        icon = QtGui.QIcon(QtGui.QPixmap(path))
        self.setIcon(icon)
        self.updateThumbnailSize()
        self.item().update()

    def setIcon(self, icon):
        """
        Set the icon to be shown for the preview.

        :type icon: QtGui.QIcon
        """
        self.ui.thumbnailButton.setIcon(icon)
        self.ui.thumbnailButton.setIconSize(QtCore.QSize(200, 200))
        self.ui.thumbnailButton.setText("")

    def showSelectionSetsMenu(self):
        """Show the selection sets menu."""
        item = self.item()
        item.showSelectionSetsMenu()

    def resizeEvent(self, event):
        """
        Overriding to adjust the image size when the widget changes size.

        :type event: QtCore.QSizeEvent
        """
        self.updateThumbnailSize()

    def updateThumbnailSize(self):
        """
        Update the thumbnail button to the size of the widget.

        :rtype: None
        """
        if hasattr(self.ui, "thumbnailButton"):
            width = self.width() - 10
            if width > 250:
                width = 250

            size = QtCore.QSize(width, width)
            self.ui.thumbnailButton.setIconSize(size)
            self.ui.thumbnailButton.setMaximumSize(size)
            self.ui.thumbnailFrame.setMaximumSize(size)

    def close(self):
        """
        Overriding the close method so that we can disable the script job.

        :rtype: None
        """
        self.setScriptJobEnabled(False)
        if self._optionsWidget:
            self.item().saveOptions(**self._optionsWidget.optionsToDict())
        QtWidgets.QWidget.close(self)

    def scriptJob(self):
        """
        Get the script job object used when the users selection changes.

        :rtype: mutils.ScriptJob
        """
        return self._scriptJob

    def setScriptJobEnabled(self, enable):
        """
        Enable the script job used when the users selection changes.

        :rtype: None
        """
        if enable:
            if not self._scriptJob:
                event = ['SelectionChanged', self.selectionChanged]
                self._scriptJob = mutils.ScriptJob(event=event)
        else:
            sj = self.scriptJob()
            if sj:
                sj.kill()
            self._scriptJob = None

    def objectCount(self):
        """
        Return the number of controls contained in the item.

        :rtype: int
        """
        return self.item().objectCount()


    def setSettings(self, settings):
        """
        Set the state of the widget.

        :type settings: dict
        """

        toggleBoxChecked = settings.get("iconToggleBoxChecked", True)
        self.ui.iconToggleBoxFrame.setVisible(toggleBoxChecked)
        self.ui.iconToggleBoxButton.setChecked(toggleBoxChecked)

        toggleBoxChecked = settings.get("infoToggleBoxChecked", True)
        self.ui.infoToggleBoxFrame.setVisible(toggleBoxChecked)
        self.ui.infoToggleBoxButton.setChecked(toggleBoxChecked)

        toggleBoxChecked = settings.get("optionsToggleBoxChecked", True)
        self.ui.optionsToggleBoxFrame.setVisible(toggleBoxChecked)
        self.ui.optionsToggleBoxButton.setChecked(toggleBoxChecked)


    def settings(self):
        """
        Get the current state of the widget.

        :rtype: dict
        """
        settings = {}
        settings["iconToggleBoxChecked"] = self.ui.iconToggleBoxButton.isChecked()
        settings["infoToggleBoxChecked"] = self.ui.infoToggleBoxButton.isChecked()
        settings["optionsToggleBoxChecked"] = self.ui.optionsToggleBoxButton.isChecked()
        return settings

    def loadSettings(self):
        """
        Load the user settings from disc.

        :rtype: None
        """
        data = studiolibrarymaya.settings()
        self.setSettings(data)

    def saveSettings(self):
        """
        Save the user settings to disc.

        :rtype: None
        """
        data = self.settings()
        studiolibrarymaya.saveSettings(data)

    def selectionChanged(self):
        """
        Triggered when the users Maya selection has changed.

        :rtype: None
        """
        pass

    def accept(self):
        """
        Called when the user clicks the apply button.

        :rtype: None
        """
        self.item().loadFromCurrentOptions()
