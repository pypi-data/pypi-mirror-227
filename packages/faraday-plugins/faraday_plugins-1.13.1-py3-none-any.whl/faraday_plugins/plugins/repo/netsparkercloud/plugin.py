"""
Faraday Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

"""
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from faraday_plugins.plugins.plugin import PluginXMLFormat

__author__ = "Francisco Amato"
__copyright__ = "Copyright (c) 2013, Infobyte LLC"
__credits__ = ["Francisco Amato"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Francisco Amato"
__email__ = "famato@infobytesec.com"
__status__ = "Development"


def get_urls(string):
    if isinstance(string, bytes):
        string_decode = string.decode("utf-8")
        urls = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', string_decode)
    else:
        urls = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', string)
    return urls


class NetsparkerCloudXmlParser:
    """
    The objective of this class is to parse an xml file generated by the netsparkercloud tool.

    TODO: Handle errors.
    TODO: Test netsparkercloud output version. Handle what happens if the parser doesn't support it.
    TODO: Test cases.

    @param netsparkercloud_xml_filepath A proper xml generated by netsparkercloud
    """

    def __init__(self, xml_output):
        self.filepath = xml_output
        tree = self.parse_xml(xml_output)
        if tree:
            self.items = self.get_items(tree)
        else:
            self.items = []

    def parse_xml(self, xml_output):
        """
        Open and parse an xml file.

        TODO: Write custom parser to just read the nodes that we need instead of
        reading the whole file.

        @return xml_tree An xml tree instance. None if error.
        """
        try:
            tree = ET.fromstring(xml_output)
        except SyntaxError as err:
            self.logger.error(f"SyntaxError: {err}. {xml_output}")
            return None
        return tree

    def get_items(self, tree):
        """
        @return items A list of Host instances
        """
        for node in tree.findall("vulnerabilities/vulnerability"):
            yield Item(node)


class Item:
    """
    An abstract representation of a Item


    @param item_node A item_node taken from an netsparkercloud xml tree
    """

    def re_map_severity(self, severity):
        if severity == "Important":
            return "high"
        return severity

    def __init__(self, item_node, encoding="ascii"):
        self.node = item_node
        self.url = urlparse(self.get_text_from_subnode("url"))
        self.protocol = self.url.scheme
        self.hostname = self.url.netloc
        self.port = self.url.port
        if self.port is None:
            self.port = '80'
        self.type = self.get_text_from_subnode("type")
        self.name = self.get_text_from_subnode("name")
        self.severity = self.re_map_severity(self.get_text_from_subnode("severity"))
        self.certainty = self.get_text_from_subnode("certainty")
        self.node = item_node.find("http-request")
        self.method = self.get_text_from_subnode("method")
        self.request = self.get_text_from_subnode("content")
        self.param = ""
        self.paramval = ""
        for p in self.node.findall("parameters/parameter"):
            self.param = p.get('name')
            self.paramval = p.get('value')

        self.node = item_node.find("http-response")
        self.response = self.get_text_from_subnode("content")
        self.extra = []
        for v in item_node.findall("extra-information/info"):
            self.extra.append(v.get('name') + ":" + v.get('value'))

        self.node = item_node.find("classification")
        self.owasp = self.get_text_from_subnode("owasp")
        self.wasc = self.get_text_from_subnode("wasc")
        self.cwe = self.get_text_from_subnode("cwe")
        self.capec = self.get_text_from_subnode("capec")
        self.pci = self.get_text_from_subnode("pci31")
        self.pci2 = self.get_text_from_subnode("pci32")
        self.hipaa = self.get_text_from_subnode("hipaa")

        self.ref = []
        if self.cwe:
            self.cwe = [f"CWE-{self.cwe}"]
        if self.owasp:
            self.ref.append(f"OWASP-{self.owasp}")

        self.node = item_node
        self.remedyreferences = self.get_text_from_subnode("remedy-references")
        self.externalreferences = self.get_text_from_subnode("external-references")
        if self.remedyreferences:
            for u in get_urls(self.remedyreferences):
                self.ref.append(u)
        if self.externalreferences:
            for u in get_urls(self.externalreferences):
                self.ref.append(u)

        self.impact = self.get_text_from_subnode("impact")
        self.remedialprocedure = self.get_text_from_subnode("remedial-procedure")
        self.remedialactions = self.get_text_from_subnode("remedial-actions")
        self.exploitationskills = self.get_text_from_subnode("exploitation-skills")
        self.proofofconcept = self.get_text_from_subnode("proof-of-concept")

        self.resolution = "Remerdial Procedure: {} \nRemedial Actions: {}".format(self.remedialprocedure,
                                                                                  self.remedialactions)

        self.desc = self.get_text_from_subnode("description")
        self.desc = "\nImpact: {} \nExploitation Skills: {} \nProof of concept: {} \nWASC: {}  \nPCI31: {} \nPCI32: {}" \
                    " \nCAPEC: {} \nHIPA: {} \nExtra: {}".format(self.impact, self.exploitationskills,
                                                                 self.proofofconcept, self.wasc, self.pci, self.pci2,
                                                                 self.capec, self.hipaa, self.extra)

    def get_text_from_subnode(self, subnode_xpath_expr):
        """
        Finds a subnode in the host node and the retrieves a value from it.

        @return An attribute value
        """
        if self.node:
            sub_node = self.node.find(subnode_xpath_expr)
            if sub_node is not None:
                return sub_node.text
        return None


class NetsparkerCloudPlugin(PluginXMLFormat):
    """
    Example plugin to parse netsparkercloud output.
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.identifier_tag = "netsparker-cloud"
        self.id = "NetsparkerCloud"
        self.name = "NetsparkerCloud XML Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "NetsparkerCloud"
        self.framework_version = "1.0.0"
        self.options = None

    def parseOutputString(self, output):
        parser = NetsparkerCloudXmlParser(output)
        first = True
        for i in parser.items:
            if first:
                ip = self.resolve_hostname(i.hostname)
                h_id = self.createAndAddHost(ip, hostnames=[i.hostname])
                s_id = self.createAndAddServiceToHost(h_id, i.protocol, ports=[i.port], status="open")
                first = False
            v_id = self.createAndAddVulnWebToService(h_id, s_id, i.name, ref=i.ref, website=i.hostname,
                                                     severity=i.severity, desc=i.desc, path=i.url.path, method=i.method,
                                                     request=i.request, response=i.response, resolution=i.resolution,
                                                     pname=i.param, cwe=i.cwe)
        del parser


def createPlugin(*args, **kwargs):
    return NetsparkerCloudPlugin(*args, **kwargs)
