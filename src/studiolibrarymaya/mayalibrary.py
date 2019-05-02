import maya.cmds

from studiolibrary import Library


class MayaLibrary (Library):

    def findRigsInScene(self):
        """return the list of rigs (.lib) loaded in the scene
        
        Returns:
            list string -- the list of rigs
        """
        return sorted( list(set([str(maya.cmds.getAttr(attr)) for attr in ( maya.cmds.ls('*.nwgpt_id', recursive=True, objectsOnly=False) )] )))
