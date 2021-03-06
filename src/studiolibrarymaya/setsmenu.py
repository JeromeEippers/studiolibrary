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
from functools import partial

from studioqt import QtGui
from studioqt import QtWidgets

import studiolibrary
import studiolibrarymaya

from studiolibrarymaya import setsitem
from studiolibrarymaya import setsgeppetto


__all__ = ["SetsMenu"]

logger = logging.getLogger(__name__)


def selectContentAction(item, parent=None):
    """
    :param item: mayabaseitem.MayaBaseItem
    :param parent: QtWidgets.QMenu
    """
    icon = studiolibrarymaya.resource().icon("arrow")
    action = QtWidgets.QAction(icon, "Select content", parent)
    action.triggered.connect(item.selectContent)
    return action


def showSetsMenu(path, **kwargs):
    """
    Show the frame range menu at the current cursor position.

    :type path: str
    :rtype: QtWidgets.QAction
    """
    menu = SetsMenu.fromPath(path, **kwargs)
    position = QtGui.QCursor().pos()
    action = menu.exec_(position)
    return action


class SetsMenu(QtWidgets.QMenu):

    @classmethod
    def fromPath(cls, path, parent=None, libraryWindow=None, **kwargs):
        """
        Return a new SetMenu instance from the given path.
        
        :type path: str
        :type parent: QtWidgets.QMenu or None
        :type libraryWindow: studiolibrary.LibraryWindow or None
        :type kwargs: dict
        :rtype: QtWidgets.QAction
        """
        item = setsitem.SetsItem(path, libraryWindow=libraryWindow)
        return cls(item, parent, enableSelectContent=False, **kwargs)

    def __init__(
            self,
            item,
            parent=None,
            namespaces=None,
            enableSelectContent=True,
    ):
        """
        :type item: studiolibrarymaya.BaseItem
        :type parent: QtWidgets.QMenu or None
        :type namespaces: list[str] or None
        :type enableSelectContent: bool
        """
        parent = parent or item.libraryWindow()
        QtWidgets.QMenu.__init__(self, "Selection Sets", parent)

        icon = studiolibrarymaya.resource().icon("selectionSet")
        self.setIcon(icon)

        self._item = item
        self._namespaces = namespaces
        self._enableSelectContent = enableSelectContent
        self.reload()

    def item(self):
        """
        :rtype: mayabaseitem.MayaBaseItem
        """
        return self._item

    def namespaces(self):
        """
        :rtype: list[str]
        """
        return self._namespaces

    def selectContent(self):
        """
        :rtype: None
        """
        self.item().selectContent(namespaces=self.namespaces())

    def selectionSets(self):
        """
        :rtype: list[setsitem.SetsItem]
        """

        items = []
        paths = []

        #add the geppetto selection sets
        items += [        
            setsgeppetto.SetsGeppetto('Body', 'ctl body'),
            setsgeppetto.SetsGeppetto('Face', 'ctl face'),
            setsgeppetto.SetsGeppetto('All', 'ctl'),
        ]

        #first get all the one from the global library if it exists:
        myuser = self.item().FolderUserItem()
        if myuser and myuser.user() != 'global':

            #get the library name and compute the global path
            mylib = self.item().FolderLibraryItem()
            if mylib:
                libids = mylib.libraryId().split('/')
                globalpath = os.path.join(
                    self.item().library().globalUserFolderPath(),
                    os.path.sep.join(libids)
                ) + '.lib'

                #add a dummy folder to the path for the 'walkup' to start by the lib
                globalpath = os.path.join(globalpath, 'dummy')

                setIterator = studiolibrary.walkup(
                    globalpath,
                    match=lambda path: path.endswith(".set"),
                    depth=10,
                )

                paths += list(setIterator)

        #now add the set from the current folder

        setIterator = studiolibrary.walkup(
            self.item().path(),
            match=lambda path: path.endswith(".set"),
            depth=10,
        )
        paths += list(setIterator)

        #convert to items
        libraryWindow = self.item().libraryWindow()

        for path in paths:
            item = setsitem.SetsItem(path)
            item.setLibraryWindow(libraryWindow)
            items.append(item)

        return items

    def reload(self):
        """
        :rtype: None
        """
        self.clear()

        if self._enableSelectContent:
            action = selectContentAction(item=self.item(), parent=self)
            self.addAction(action)
            self.addSeparator()

        selectionSets = self.selectionSets()

        if selectionSets:
            for selectionSet in selectionSets:
                dirname = os.path.basename(selectionSet.dirname())
                basename = selectionSet.name().replace(selectionSet.extension(), "")
                nicename = '{0}{1}{2}'.format (dirname, ": " if dirname != '' else '', basename)

                if selectionSet.menuItemIcon() != '': 
                    icon = studiolibrarymaya.resource().icon(selectionSet.menuItemIcon())
                    action = QtWidgets.QAction(icon, nicename, self)
                else:
                    action = QtWidgets.QAction(nicename, self)
                callback = partial(selectionSet.load, namespaces=self.namespaces())
                action.triggered.connect(callback)
                self.addAction(action)
        else:
            action = QtWidgets.QAction("No selection sets found!", self)
            action.setEnabled(False)
            self.addAction(action)
