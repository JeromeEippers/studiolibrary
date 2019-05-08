import converter

"""
usage :

import poselibraryconverter as conv
conv.Convert(r"/nwave/projects/BF2/LIB/nwPoseLibrary/", r"/home/jeromee/development/local_dev/studioLibraryPoseFolder/")

"""


def Convert(sourceLibrary, destinationLibrary):

    conv = converter.Converter()
    conv.convertPoseLibrary( sourceLibrary, destinationLibrary, "converted from nwPoseLibrary")


