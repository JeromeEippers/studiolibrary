from functools import partial

from studioqt import QtCore, QtWidgets

import studiolibrary


class LibrarySelectMenu(QtCore.QObject):

    def __init__(self, libraries, name="Library", callback=None, parent=None):
        """create a select menu
        
        Arguments:
            libraries {list or dict} -- the list or dict of libraries path. If this is a dict the key is the libpath and the value is the full path of the item
        
        Keyword Arguments:
            name {str} -- the name of the menu (default: {"Library"})
            callback {function} -- the callback when we do the selection (default: {None})
            parent {QMenu/QtWidget} -- the parent menu (default: {None})
        """
        super(LibrarySelectMenu, self).__init__()

        self._callback = callback

        self._menu = QtWidgets.QMenu(name, parent)
        if parent != None and isinstance(parent, QtWidgets.QMenu):
            parent.addMenu(self._menu)

        builddict = {'menu' : self._menu, 'children':{} }

        libkeys = libraries
        if isinstance(libraries, dict): 
            libkeys = sorted(libraries.keys())

        for lib in libkeys:
            d = builddict

            paths = lib.split('/')
            pathsCount = len(paths)
            for i, path in enumerate(paths):

                #if we are the last element we add an action
                if i >= pathsCount-1:
                    childaction = d['menu'].addAction(path)
                    thisdict = d['children'].get(path, {})
                    thisdict['action'] = childaction
                    d['children'][path] = thisdict

                    if isinstance(libraries, dict):
                        callback = partial(self._onselected, lib, libraries[lib])
                    else:
                        callback = partial(self._onselected, lib, lib)
                    childaction.triggered.connect(callback)

                #check if we already have the path in the children of our dict
                elif path not in d['children'] or 'menu' not in d['children'][path]:

                    childmenu = d['menu'].addMenu(path)
                    thisdict = d['children'].get(path, {})
                    thisdict['menu'] = childmenu
                    d['children'][path] = thisdict

                #prepare for the next path
                d = d['children'][path]
                if 'children' not in d:
                    d['children'] = {}

        self._selected = ""
        self._path = ""

    def menu(self):
        return self._menu

    def show(self, point=None):
        self._selected = ""
        self._menu.exec_(point)

    def _onselected(self, name, path):
        self._selected = name
        self._path = path
        if self._callback:
            self._callback(name, path)

    def selected(self, full=True):
        if full:
            return self._selected
        return self._selected.split('/')[-1]

    def selectedPath(self):
        return self._path
