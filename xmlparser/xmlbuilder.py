from xml.etree.ElementTree  import Element, SubElement, Comment, tostring, XML
from xml.dom                import minidom

def _prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

class XMLElement:
    def __init__(self, name):
        self.element = Element(name)

    def SetProperty(self, pName, pVal):
        self.element.set(pName, pVal)

    def SetText(self, text):
        self.element.text = text

    def SetTail(self, tail):
        self.element.tail = tail

    def Extend(self, child):
        self.element.extend(child)

    def Comment(self, comm):
        self.element.append(Comment(comm))

    def Child(self, name, text = '', tail = ''):
        child = XMLSubElement(self.element, name)
        child.SetText(text)
        child.SetTail(tail)

        return child

    def Childs(self, dictionary, parent = None):
        if not parent:
            parent = self

        for k, v in dictionary.items():
            if isinstance(v, dict):
                parent = self.Child(k)
                self.Childs(v, parent)
            parent.Child(k, v)

    def GetElement(self):
        return self.element

class XMLSubElement(XMLElement):
    def __init__(self, parent, name):
        self.element = SubElement(parent, name)

class XMLBuilder:
    def __init__(self):
        self.root = None

    def Root(self, name):
        self.root = XMLElement(name)
        return self.root

    def ParseRawXML(self, xml):
        return XML(xml)

    def ToString(self):
        return _prettify(self.root.GetElement())