import maya.cmds

from studiolibrary import Library


class MayaLibrary (Library):

    def findRigsInScene(self):
        """return the list of rigs (.lib) loaded in the scene
        
        Returns:
            list string -- the list of rigs
        """
        return sorted( list(set(
            [
                str(maya.cmds.getAttr(attr)) 
                for attr in ( maya.cmds.ls('*.nwgpt_id', recursive=True, objectsOnly=False) )
            ] )))


    def findRigsNamespacesInScene(self):
        """return the list of namespace in the scene who have a rig
        
        Returns:
            list string -- the list of namespaces
        """
        return sorted(
            [
                ":".join(attr.split(':')[:-1]) 
                for attr in ( maya.cmds.ls('*.nwgpt_id', recursive=True, objectsOnly=False) ) 
                if ':' in attr
            ])


    def findRigInSceneFromNamespace(self, namespace):
        """Find the rig from a namespace
        
        Arguments:
            namespace {string} -- the namespace
        
        Returns:
            string -- the rig id
        """

        attributes = maya.cmds.ls('{0}:*.nwgpt_id'.format(namespace), recursive=True, objectsOnly=False)
        if attributes:
            return str(maya.cmds.getAttr(attributes[0])) 

        return ""