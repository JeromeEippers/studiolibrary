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

from studioqt import QtCore
from studioqt import QtWidgets


__all__ = ["LineEditAction"]


class LineEditWidgetAction(QtWidgets.QFrame):
    pass


class LineEditAction(QtWidgets.QWidgetAction):

    valueChanged = QtCore.Signal(str)

    def __init__(self, label="", parent=None):
        """
        :type parent: QtWidgets.QMenu
        """
        QtWidgets.QWidgetAction.__init__(self, parent)

        self._widget = LineEditWidgetAction(parent)
        self._lineEdit = QtWidgets.QLineEdit(self._widget)
        self._lineEdit.setPlaceholderText(label)
        self._lineEdit.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self._lineEdit.editingFinished.connect(self._editFinished)

    def widget(self):
        """
        Return the widget for this action.

        :rtype: QtWidgets.QWidget
        """
        return self._widget

    def label(self):
        """
        Return the QLabel object.

        :rtype: QtWidgets.QLabel
        """
        return self._label

    def line(self):
        """
        Return the QLabel object.

        :rtype: QtWidgets.QSlider
        """
        return self._lineEdit

    def createWidget(self, menu):
        """
        This method is called by the QWidgetAction base class.

        :type menu: QtWidgets.QMenu
        """
        actionWidget = self.widget()

        actionLayout = QtWidgets.QHBoxLayout(actionWidget)
        actionLayout.setContentsMargins(0, 0, 0, 0)
        actionLayout.addWidget(self.line())
        actionWidget.setLayout(actionLayout)

        return actionWidget

    def _editFinished(self):
        self.valueChanged.emit(str(self._lineEdit.text()))