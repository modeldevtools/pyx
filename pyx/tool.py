from ayxproperty import AyxProperty
from decorators import newobj
import xml.etree.ElementTree as ET

class Tool:
    """
    Represents an Alteryx tool (or Node in the workflow XML).
    """

    def __init__(self, tool_id: str, configuration: str = ''):
        self.tool_id: str = tool_id
        self.configuration: str = configuration
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.plugin: str = ''
        self.engine_dll: str = ''
        self.engine_dll_entry_point: str = ''

    def toxml(self) -> ET.Element:
        # Dummy element that ElementTree extend() will strip
        root = ET.Element('root')

        node = ET.SubElement(root, 'Node')
        node.set('ToolID', self.tool_id)

        guisettings = ET.SubElement(node, 'GuiSettings')
        guisettings.set('Plugin', self.plugin)
        position = ET.SubElement(guisettings, 'Position')
        position.set('x', str(self.pos_x))
        position.set('y', str(self.pos_y))

        return root
