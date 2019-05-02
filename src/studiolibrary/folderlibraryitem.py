import os
from datetime import datetime
from functools import partial

import studiolibrary
import studiolibrary.widgets
from studioqt import QtWidgets


class FolderLibraryItem(studiolibrary.LibraryItem):

    RegisterOrder = 95
    EnableNestedItems = True

    MenuName = "Library"
    MenuOrder = 1
    MenuIconPath = studiolibrary.resource().get("icons/library.png")
    PreviewWidgetClass = studiolibrary.widgets.PreviewWidget
    DefaultThumbnailPath = studiolibrary.resource().get("icons/library_item.png")

    @classmethod
    def match(cls, path):
        """
        Return True if the given path is supported by the item.

        :type path: str 
        :rtype: bool 
        """
        if path.endswith(".lib"):
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
                "value": self.name()[:-4]
            },
            {
                "name": "path",
                "value": self.path()
            },
            {
                "name": "library id",
                "value": self.itemData()['lib_id']
            }
        ]

    @classmethod
    def showCreateWidget(cls, libraryWindow):
        """
        Show the dialog for creating a new folder.

        :rtype: None
        """
        path = libraryWindow.selectedFolderPath() or libraryWindow.path()

        #we can only create a library inside a user,
        #so let's make sure we are inside one
        if '.user' not in path:
            studiolibrary.widgets.MessageBox.warning(
                libraryWindow,
                "Missing User",
                "You need to be inside a user to create a library",
                buttons = QtWidgets.QDialogButtonBox.Ok
            )

        else:

            name, button = studiolibrary.widgets.MessageBox.input(
                libraryWindow,
                "Create library",
                "Create a new library with the name:",
            )

            name = name.strip() + ".lib"

            if name and button == QtWidgets.QDialogButtonBox.Ok:
                path = os.path.join(path, name)

                item = cls(path, libraryWindow=libraryWindow)
                item.save(path)

                if libraryWindow:
                    libraryWindow.refresh()
                    libraryWindow.selectFolderPath(path)

    def createItemData(self):
        """Overriding this method to force the item type to library"""
        itemData = super(FolderLibraryItem, self).createItemData()
        itemData['type'] = "Library"
        itemData['lib_id'] = itemData['path'].split('.user')[-1].split('.lib')[0]
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
        callback = partial(self._filterLibraries, [item for item in items if isinstance(item, FolderLibraryItem)])

        action = QtWidgets.QAction("Display only selected libraries", menu)
        action.triggered.connect(callback)
        menu.addAction(action)

        super(FolderLibraryItem, self).contextMenu(menu, items)

    def _filterLibraries(self, items):
        """callback when filtering with the menu
        
        Arguments:
            items {list of items} -- list of FolderLibraryItems
        """
        self.libraryWindow().setFolderFilterLibraryText(" ".join([item.name()[:-4] for item in items]))


studiolibrary.registerItem(FolderLibraryItem)
