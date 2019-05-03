from functools import partial

from studioqt import QtCore, QtWidgets

import studiolibrary


class LibrarySelectMenu(QtCore.QObject):

    def __init__(self, libraries, name="Library", parent=None):
        super(LibrarySelectMenu, self).__init__()

        self._menu = QtWidgets.QMenu(name, parent)
        builddict = {'menu' : self._menu, 'children':{} }

        for lib in libraries:
            d = builddict

            paths = lib.split('/')
            pathsCount = len(paths)
            for i, path in enumerate(paths):

                #check if we already have the path in the children of our dict
                if path not in d['children']:

                    #if we are the last element we add an action
                    if i >= pathsCount-1 :
                        childaction = d['menu'].addAction(path)
                        d['children'][path] = {'action' : childaction, 'children':{} }

                        callback = partial(self._onselected, lib)
                        childaction.triggered.connect(callback)

                    #otherwise we add a sub menu
                    else:
                        childmenu = d['menu'].addMenu(path)
                        d['children'][path] = {'menu' : childmenu, 'children':{} }

                #prepare for the next path
                d = d['children'][path]

        self._selected = ""

    def menu(self):
        return self._menu

    def show(self, point=None):
        self._selected = ""
        self._menu.exec_(point)

    def _onselected(self, name):
        self._selected = name

    def selected(self, full=True):
        if full:
            return self._selected
        return self._selected.split('/')[-1]
