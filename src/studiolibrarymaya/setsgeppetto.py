import maya.cmds as cmds

from nwmaya.animation.geppetto.library import tags

class SetsGeppetto(object):
    """Geppetto sets. this wraps the call to the geppetto library to find nodes per geppetto tags
    """


    def __init__(self, name, tag):

        self._name = name
        self._tag = tag


    def dirname(self):
        """get the dirname, empty in our case
        
        Returns:
            str -- ""
        """
        return ''

    def extension(self):
        """get the extension, empty in our case
        
        Returns:
            str -- ""
        """
        return ''

    def name(self):
        """The name of the selection
        
        Returns:
            str -- the name
        """
        return self._name

    def menuItemIcon(self):
        """the name of the icon to display in the menu
        
        Returns:
            str -- 'geppetto' in our case
        """
        return 'geppetto'


    def load(self, namespaces):
        """load the seleciton set.  Technically use the tag to find the objects and select them
        
        Arguments:
            namespaces {list str} -- list of namespaces to look into
        """
        nodes = []
        for namespace in namespaces:
            nodes += tags.listTagNodes(namespace, self._tag)
        cmds.select(nodes)