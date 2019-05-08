from xml.etree.ElementTree import ElementTree

class BaseReader(object):
    def __init__(self, path):
        self._path = path
        self._data = dict()

        tree = ElementTree()
        tree.parse(self._path)
        self._parse(tree)

    def _parse(self, tree):
        pass

    def data(self):
        return self._data


class PoseReader(BaseReader):
    """
    a pose reader for the old nwposelibrary format in xml
    """

    def _parse(self, tree):

        controls = tree.findall('control')
        for control in controls:

            name = control.find('name').text

            attributeDict = dict()
            self._data[name] = {'attrs':attributeDict}

            attributes = control.findall('attrValue')
            for attribute in attributes:

                attrname = attribute.find('attr').text
                attrvalue = float(attribute.find('value').text)
                attributeDict[attrname] = {'type':'doubleLinear','value':attrvalue}


class TabReader(BaseReader):
    """
    the tab reader from the old nwPoseLibrary
    """

    def _parse(self, tree):

        poses = tree.findall('pose')
        for pose in poses:

            name = pose.find('label').text
            file = pose.find('file').text
            image = pose.find('image').text

            self._data[name]={'file':file, 'image':image}


class LibReader(BaseReader):
    """
    the lib reader from the old nwPoseLibrary
    """

    def _parse(self, tree):

        tabs = tree.findall('tab')
        for tab in tabs:

            label = tab.find('label').text
            file = tab.find('file').text
            tag = tab.find('tag').text

            self._data[label] = {'file':file, 'tag':tag}