from ayxproperty import AyxProperty
from tool import Tool
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
from typing import Dict, List

class Workflow:
    """
    Contains operations to create, modify, read, and write Alteryx workflows.
    """
    
    def __init__(self, name: str, yxmd_version: str):
        """Initializes the Workflow instance with a name, yxmd file version, and default properties.

        The name can be an arbitrary string. If no file name is specified when the
        workflow is written, the name will be used as the root of the file name,
        with invalid characters converted to underscores.

        The value of yxmd_version should be the full Alteryx version with which
        the workflow will be compatible. For example '2019.2' or '2018.3'.

        All other properties are set to their default values.

        :param name: name of the workflow
        :type name: str
        :param yxmd_version: version string for the workflow
        :type yxmd_version: str
        :return: no value
        :rtype: none
        """
        self.name = name
        self.yxmd_version: str = yxmd_version
        self.tools: Dict[str, Tool] = dict({})
        self.connections = []
        
        self.properties: Dict[str, AyxProperty] = dict({
            'Memory': AyxProperty('Memory').set_attribute('default', 'True'),
            'GlobalRecordLimit': AyxProperty('GlobalRecordLimit').set_attribute('value', '0'),
            'TempFiles': AyxProperty('TempFiles').set_attribute('default', 'True'),
            'Annotation': AyxProperty('Annotation').set_attribute('on', 'True').set_attribute('includeToolName', 'False'),
            'ConvErrorLimit': AyxProperty('ConvErrorLimit').set_attribute('value', 'False'),
            'ConvErrorLimit_Stop': AyxProperty('ConvErrorLimit_Stop').set_attribute('value', 'False'),
            'CancelOnError': AyxProperty('CancelOnError').set_attribute('value', 'False'),
            'DisableBrowse': AyxProperty('DisableBrowse').set_attribute('value', 'False'),
            'EnablePerformanceProfiling': AyxProperty('EnablePerformanceProfiling').set_attribute('value', 'False'),
            'DisableAllOutput': AyxProperty('DisableAllOutput').set_attribute('value', 'False'),
            'ShowAllMacroMessages': AyxProperty('ShowAllMacroMessages').set_attribute('value', 'False'),
            'ShowConnectionStatusIsOn': AyxProperty('ShowConnectionStatusIsOn').set_attribute('value', 'True'),
            'ShowConnectionStatusOnlyWhenRunning': AyxProperty('ShowConnectionStatusOnlyWhenRunning').set_attribute('value', 'True'),
            'ZoomLevel': AyxProperty('ZoomLevel').set_attribute('value', '0'),
            'LayoutType': AyxProperty('LayoutType', 'Horizontal')
        })

        self.metainfo: Dict[str, AyxProperty] = dict({
            'NameIsFileName': AyxProperty('NameIsFileName').set_attribute('value', 'True'),
            'Name': AyxProperty('Name', self.name),
            'Description': AyxProperty('Description'),
            'RootToolName': AyxProperty('RootToolName'),
            'ToolVersion': AyxProperty('ToolVersion'),
            'ToolInDb': AyxProperty('ToolInDb').set_attribute('value', 'False'),
            'CategoryName': AyxProperty('CategoryName'),
            'SearchTags': AyxProperty('SearchTags'),
            'Author': AyxProperty('Author'),
            'Company': AyxProperty('Company'),
            'Copyright': AyxProperty('Copyright'),
            'DescriptionLink': AyxProperty('DescriptionLink').set_attribute('actual', '').set_attribute('displayed', '')
        })

    def write(self, filename: str = "", overwrite: bool = True) -> None:
        """Writes the workflow to the specified file.

        If no filename is provided, the workflow name is used. If overwrite
        is True, then any existing file with the same name will be overwritten.
        If overwrite is False and a file exists with the same name, this
        method will raise an exception.
        """
        if not overwrite and os.path.isfile(filename):
            raise FileExistsError('File "{}" already exists and overwrite is false'.format(filename))

        def property_to_attributes(parent: ET.Element, prop: AyxProperty) -> None:
            child = ET.SubElement(parent, prop.name)
            for key, val in prop.get_attributes().items():
                child.set(key, val)
            if prop.value != '':
                child.text = prop.value

        ayx_doc = ET.Element('AlteryxDocument')
        ayx_doc.set('yxmdVer', self.yxmd_version)

        tools = ET.SubElement(ayx_doc, 'Nodes')
        for _, tool_val in self.tools.items():
            tools.extend(tool_val.toxml())
        
        connections = ET.SubElement(ayx_doc, 'Connections')
        if len(self.connections) > 0:
            print("Not implemented")

        properties = ET.SubElement(ayx_doc, 'Properties')
        for _, prop_val in self.properties.items():
            property_to_attributes(properties, prop_val)

        metainfo = ET.SubElement(properties, 'MetaInfo')
        for _, mi_val in self.metainfo.items():
            property_to_attributes(metainfo, mi_val)

        workflow_text = ET.tostring(ayx_doc, 'utf-8')
        reparsed = minidom.parseString(workflow_text)

        with open(filename, 'w') as f:
            f.write(reparsed.toprettyxml(indent='    '))

    def add_tool(self, tool: Tool) -> None:
        """Adds the provided Tool instance to the workflow
        """
        self.tools[tool.tool_id] = tool
