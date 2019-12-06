from xml.dom import minidom
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class Tool(ABC):
    """
    Base class for representing an Alteryx tool (or Node in the workflow XML).
    """

    def __init__(self, tool_id: str):
        self.tool_id: str = tool_id
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.plugin: str = ''
        self.engine_dll: str = ''
        self.engine_dll_entry_point: str = ''
        super().__init__()

    @abstractmethod
    def toxml(self) -> ET.Element:
        pass

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='    ')
