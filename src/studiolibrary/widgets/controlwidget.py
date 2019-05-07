import logging
from functools import partial

from studioqt import QtGui
from studioqt import QtCore
from studioqt import QtWidgets

import studioqt
import studiolibrary

logger = logging.getLogger(__name__)


class ControlWidget(QtWidgets.QWidget):

    controlChanged = QtCore.Signal(str)

    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)

        layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(layout)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self._dataset = None
        self._iconPadding = 6
        self._iconButton = QtWidgets.QPushButton(self)
        self._iconButton.clicked.connect(self._onClicked)
        layout.addWidget(self._iconButton)

        icon = studiolibrary.resource().icon("pokeball")
        self._iconButton.setIcon(icon)

        self._comboBox = QtWidgets.QComboBox(self)
        layout.addWidget(self._comboBox, 1)

        self._comboBox.addItem("Select a character", "")
        self._comboBox.installEventFilter(self)
        self._comboBox.activated.connect(self._onActivated)

        self._comboBox.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.update()

    def update(self):
        self.updateIconColor()


    def setDataset(self, dataset):
        """
        Set the data set for the search widget:
        
        :type dataset: studiolibrary.Dataset
        """
        self._dataset = dataset


    def dataset(self):
        """
        Get the data set for the search widget.
        
        :rtype: studiolibrary.Dataset 
        """
        return self._dataset


    def updateIconColor(self):
        """
        Update the icon colors to the current foregroundRole.

        :rtype: None
        """
        
        color = self.palette().color(self._iconButton.foregroundRole())
        color = studioqt.Color.fromColor(color)

        icon = self._iconButton.icon()
        icon = studioqt.Icon(icon)
        icon.setColor(color)
        self._iconButton.setIcon(icon)



    def resizeEvent(self, event):
        """
        Reimplemented so the icon maintains the same height as the widget.

        :type event:  QtWidgets.QResizeEvent
        :rtype: None
        """
        QtWidgets.QWidget.resizeEvent(self, event)
        size = QtCore.QSize(self.height(), self.height())
        self._iconButton.setIconSize(size)
        self._iconButton.setFixedSize(size)


    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and
            source is self._comboBox):

            #populate the list
            self._comboBox.clear()
            self._comboBox.addItem("Select a character", "")
            for rig in self.dataset().findRigsNamespacesInScene():
                self._comboBox.addItem(rig, rig)

        return super(ControlWidget, self).eventFilter(source, event)


    def _onClicked(self):
        self._comboBox.setFocus()

    def _onActivated(self, id=None):

        userdata = str( self._comboBox.itemData(id) ) 
        self.dataset().setActiveCharacter(userdata)
        self.controlChanged.emit(userdata)