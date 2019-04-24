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

import studioqt
import studiolibrary
import zefir
import platform


def zefir_library():
    """Return the project path on the NAS
    
    Returns:
        string -- the path to the library
    """
    context = zefir.get_context()
    if context != None:
        projectname = context.find_project().name

        rootPath = "/nwave/projects/{0}/LIB/StudioLibrary/".format(projectname)
        if 'windows' in platform.system().lower():
            rootPath = "\\\\nwave\\projects\\{0}\\LIB\\StudioLibrary\\".format(projectname)

        return rootPath

    
def zefir_supervisors():
    """Returns the list of animation supervisors
    
    Returns:
        list string -- the supervisors id
    """
    return ['dirkd'] 


def main(*args, **kwargs):
    """
    Convenience method for creating/showing a library widget instance.

    return studiolibrary.LibraryWindow.instance(
        name="",
        path="",
        show=True,
        lock=False,
        superusers=None,
        lockRegExp=None,
        unlockRegExp=None
    )

    :rtype: studiolibrary.LibraryWindow
    """
    # Reload all Studio Library modules when Shift is pressed.
    # This is for developers to test their changes in a DCC application.
    if studioqt.isShiftModifier():
        import studiolibrary
        studiolibrary.reload()

    import studiolibrary

    #merge the default value in the kwargs parameters:
    if "path" not in kwargs:
        kwargs["path"] = zefir_library()

    if "superusers" not in kwargs:
        kwargs["superusers"] = zefir_supervisors()

    if studiolibrary.isMaya():
        import studiolibrarymaya
        libraryWindow = studiolibrarymaya.main(*args, **kwargs)
    else:
        libraryWindow = studiolibrary.LibraryWindow.instance(*args, **kwargs)

    return libraryWindow


if __name__ == "__main__":

    # Run the Studio Library in a QApplication instance
    with studiolibrary.app():
        studiolibrary.main()
