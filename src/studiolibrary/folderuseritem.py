import os
from datetime import datetime
from functools import partial

import studiolibrary
import studiolibrary.widgets

from studioqt import QtWidgets


class FolderUserItem(studiolibrary.LibraryItem):

    EnabledOnlyInLibrary = False

    RegisterOrder = 90
    EnableNestedItems = True

    MenuName = "User"
    MenuOrder = 1
    MenuIconPath = studiolibrary.resource().get("icons/user.png")
    PreviewWidgetClass = studiolibrary.widgets.PreviewWidget
    DefaultThumbnailPath = studiolibrary.resource().get("icons/user_item.png")

    @classmethod
    def match(cls, path):
        """
        Return True if the given path is supported by the item.

        :type path: str 
        :rtype: bool 
        """
        if path.endswith(".user"):
            return True
        return False

    def info(self):
        """
        Get the info to display to user.
        
        :rtype: list[dict]
        """

        return [
            {
                "name": "name",
                "value": self.name()[:-5]
            },
            {
                "name": "path",
                "value": self.path()
            }
        ]

    def user(self):
        """return the user name
        
        Returns:
            string -- user name
        """
        return self.name()[:-5]


    @classmethod
    def showCreateWidget(cls, libraryWindow):
        """
        Show the dialog for creating a new folder.

        :rtype: None
        """
        path = os.path.join( libraryWindow.library().path(), 'user' )

        name, button = studiolibrary.widgets.MessageBox.input(
            libraryWindow,
            "Create User",
            "Create a new user:",
            libraryWindow.library().currentUser()
        )

        name = name.strip() + ".user"

        if button == QtWidgets.QDialogButtonBox.Ok:
            path = os.path.join(path, name)

            if os.path.exists(path) == False:

                item = cls(path, libraryWindow=libraryWindow)
                item.save(path)

                if libraryWindow:
                    libraryWindow.refresh()
                    libraryWindow.selectFolderPath(path)

    def createItemData(self):
        """Overriding this method to force the item type to library"""
        itemData = super(FolderUserItem, self).createItemData()
        itemData['type'] = "User"
        return itemData

    def doubleClicked(self):
        """Overriding this method to show the items contained in the folder."""
        self.libraryWindow().selectFolderPath(self.path())

    def write(self, *args, **kwargs):
        """Adding this method to avoid NotImpementedError."""
        pass

    def contextMenu(self, menu, items=None):
        """
        Called when the user right clicks on the item.

        :type menu: QtWidgets.QMenu
        :type items: list[LibraryItem]
        :rtype: None
        """
        callback = partial(self._filterUsers, [item for item in items if isinstance(item, FolderUserItem)])

        action = QtWidgets.QAction("Display only selected users", menu)
        action.triggered.connect(callback)
        menu.addAction(action)

        super(FolderUserItem, self).contextMenu(menu, items)

    def _filterUsers(self, items):
        """callback when filtering with the menu
        
        Arguments:
            items {list of items} -- list of FolderLibraryItems
        """
        self.libraryWindow().setFolderFilterUserText(" ".join([item.name()[:-5] for item in items]))
    



studiolibrary.registerItem(FolderUserItem)
