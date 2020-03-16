import os

from xml.etree.ElementTree  import Element, SubElement, Comment, tostring, XML, parse as ETParse, register_namespace
from xml.dom                import minidom

def _prettify(elem, indent = "  ", newl = ''):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent = indent, newl = newl)

class XMLElement:
    def __init__(self, name = 'child', element = None):
        if element:
            self.element = element
        else:
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
    @staticmethod
    def Parse(xmlFile, namespace = ''):
        register_namespace('', namespace)
        return XMLBuilder(ETParse(xmlFile).getroot())

    def __init__(self, root = None):
        self.root = XMLElement(element = root)

    def GetRoot(self):
        return self.root

    def GetElement(self, name, sroot = None):
        if not sroot:
            return None

        for child in sroot.GetElement():
            if name in child.tag:
                return XMLElement(element = child)

        return None

    def Root(self, name):
        self.root = XMLElement(name)
        return self.root

    def ParseRawXML(self, xml):
        return XML(xml)

    def ToString(self):
        prettified = _prettify(self.root.GetElement(), newl='\n')
        return '\r'.join([ s for s in prettified.splitlines() if s.strip() ])