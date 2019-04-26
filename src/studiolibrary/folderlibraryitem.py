import os
from datetime import datetime

import studiolibrary
import studiolibrary.widgets

from studioqt import QtWidgets


class FolderLibraryItem(studiolibrary.LibraryItem):

    RegisterOrder = 90
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
            }
        ]

    @classmethod
    def showCreateWidget(cls, libraryWindow):
        """
        Show the dialog for creating a new folder.

        :rtype: None
        """
        path = libraryWindow.selectedFolderPath() or libraryWindow.path()

        name, button = studiolibrary.widgets.MessageBox.input(
            libraryWindow,
            "Create library",
            "Create a new library with the name:",
        )

        name = name.strip()

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
        return itemData

    def doubleClicked(self):
        """Overriding this method to show the items contained in the folder."""
        self.libraryWindow().selectFolderPath(self.path())

    def write(self, *args, **kwargs):
        """Adding this method to avoid NotImpementedError."""
        pass


studiolibrary.registerItem(FolderLibraryItem)
