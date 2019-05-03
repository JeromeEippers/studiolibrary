import os
from datetime import datetime
from functools import partial

import studiolibrary
import studiolibrary.widgets
from studioqt import QtWidgets, QtCore


class FolderLibraryCreateCustomWidget(QtWidgets.QWidget):

    def __init__(self, libraries, parent=None):
        super(FolderLibraryCreateCustomWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)

        self._label = QtWidgets.QLabel(libraries[0], self)
        layout.addWidget(self._label, 100)

        self._menu = studiolibrary.widgets.LibrarySelectMenu(libraries, 'to create', self)
        self._pushButton = QtWidgets.QPushButton("...", self)
        self._pushButton.clicked.connect(self._onclicked)
        layout.addWidget(self._pushButton,1)

    def _onclicked(self):
        point = self._pushButton.mapToGlobal(QtCore.QPoint(0, 0))
        self._menu.show(point)
        if self._menu.selected() != "":
            self._label.setText(self._menu.selected())

    def text(self):
        return str(self._label.text())
        

class FolderLibraryItem(studiolibrary.LibraryItem):

    EnabledOnlyInLibrary = False

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
            
            loaded_rigs = libraryWindow.library().findRigsInScene()

            if len(loaded_rigs) <= 0:
                studiolibrary.widgets.MessageBox.warning(
                    libraryWindow,
                    "Missing rigs",
                    "No entity found in the scene",
                    buttons = QtWidgets.QDialogButtonBox.Ok
                )

            else :

                custom = FolderLibraryCreateCustomWidget(loaded_rigs)

                button = studiolibrary.widgets.MessageBox.customInput(
                    libraryWindow,
                    "Create library",
                    "Create a library for:",
                    custom
                )

                name = custom.text()

                if name and button == QtWidgets.QDialogButtonBox.Ok:
                    path = path.split('.user')[0] + '.user'
                    for p in name.split('/'):
                        path = os.path.join(path, p)
                    path += '.lib'

                    os.makedirs(path)

                    if libraryWindow:
                        libraryWindow.sync()

    def createItemData(self):
        """Overriding this method to force the item type to library"""
        itemData = super(FolderLibraryItem, self).createItemData()
        itemData['type'] = "Library"
        itemData['lib_id'] = itemData['path'].split('.user/')[-1].split('.lib')[0]
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
