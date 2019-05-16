import maya.cmds as cmds

import mutils
from nwmaya.animation.geppetto.library import mirror


class MirrorGeppetto(object):

    def __init__(self, namespace):
        self._namespace = namespace
    
    def path(self):
        return "geppetto"

    def mirrorObject(self, srcName):
        """Get the mirror object from the srcName
        
        Arguments:
            srcName {str} -- the src name of the node in the pose
        
        Returns:
            str -- the mirrored node with the same namespace as the srcname
        """
        srcNode = mutils.Node(srcName)
        #look for the object in the scene and not in the pose data
        mirrorName = mirror.mirrorNode('{0}:{1}'.format(self._namespace, srcNode.nameOnly()))
        
        if mirrorName != '':
            #return the object name with the same namespace as the srcname
            mirrorNode = mutils.Node(mirrorName)
            return '{0}:{1}'.format(srcNode.namespace(), mirrorNode.nameOnly())
        return None


    def mirrorAxis(self, srcName):
        """get the mirror axis from the node in the scene
        
        Arguments:
            srcName {str} -- node name in the pose
        
        Returns:
            list of float -- the mirrors axis
        """
        srcNode = mutils.Node(srcName)
        factors = mirror.mirrorFactors('{0}:{1}'.format(self._namespace, srcNode.nameOnly()))

        #as we have more often rotations than translations we will look at the rotations factors to set the mirror plane
        #and we will flip the values ( and force it to be 1 or -1)
        axis = []
        for factor in factors[3:]:
            if factor < 0:
                axis.append(1)
            else :
                axis.append(-1)
        return axis


    def matchObjects(self, objects):

        for obj in objects:
            yield obj, obj, self.mirrorAxis(obj)


    @staticmethod
    def formatValue(attr, value, mirrorAxis):
        """
        :type attr: str
        :type value: float
        :type mirrorAxis: list[int]
        :rtype: float
        """
        if mutils.MirrorTable.isAttrMirrored(attr, mirrorAxis):
            return value * -1
        return value