"""
Faraday Penetration Test IDE
Copyright (C) 2016  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

"""
from faraday_plugins.plugins.plugin import PluginBase
import re

import xml.etree.ElementTree as ET

__author__ = 'Ezequiel Tavella'
__copyright__ = 'Copyright (c) 2016, Infobyte LLC'
__credits__ = ['Ezequiel Tavella']
__license__ = ''
__version__ = '1.0.0'
__email__ = "ezequieltbh@infobytesec.com"
__status__ = "Development"


class NdiffXmlParser:
    """
    The objective of this class is to parse an xml file generated by
    the ndiff tool.
    """

    def __init__(self, xmlOutput):
        self.tree = self.parse_xml(xmlOutput)

        if self.tree:
            self.hostDiff = self.getHostsDiffs(self.tree)
        else:
            self.hostDiff = []

    def parse_xml(self, xmlOutput):

        # Open and parse an xml output

        try:
            return ET.fromstring(xmlOutput)
        except SyntaxError as err:
            print(f"SyntaxError: {err}")
            return None

    def getHostsDiffs(self, tree):
        """
        @return hosts A list of HostDiff instances
        """
        for node in tree.findall('scandiff/hostdiff'):
            yield HostDiff(node)


class HostDiff():

    # Abstraction of a Hosts Diff
    # Search for a new host in the second scan and new ports opened or changed
    # of status...
    def __init__(self, hostDiff):

        self.isNewHost = False
        self.hostXml = self.getHostXml(hostDiff)

        self.ip = self.getIp()
        self.ports = self.getPorts()

    def getHostXml(self, hostDiff):

        host = hostDiff.find('host')
        if host is not None:
            return host
        else:
            self.isNewHost = True
            return hostDiff.find('b/host')

    def getIp(self):
        if self.hostXml is None:
            return None
        return self.hostXml.find('address').get('addr')

    def getPorts(self):

        ports = []
        if self.hostXml is None:
            return ports

        if self.isNewHost:

            for port in self.hostXml.find('ports').findall('port'):
                ports.append(
                    [port.get('portid'), port.find('state').get('state')])
            return ports

        else:

            for port in self.hostXml.find('ports').findall('portdiff'):
                if port.find('b/port'):
                    ports.append([port.find('b/port').get('portid'),
                                  port.find('b/port/state').get('state')])
            return ports


class CmdNdiffPlugin(PluginBase):
    """
    This plugin handles ndiff command.
    Add a new vuln INFO if detect a new host or a new port ..
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.id = "Ndiff"
        self.name = "ndiff"
        self.plugin_version = "0.0.1"
        self.version = "1.0.0"
        self._command_regex = re.compile(r'^(sudo ndiff|ndiff)\s+.*?')

    def parseOutputString(self, output):
        parser = NdiffXmlParser(output)
        for host in parser.hostDiff:
            if host.ip is None:
                continue
            if host.isNewHost:
                hostId = self.createAndAddHost(host.ip, '')
                description = f'{host.ip} is a NEW host active.\n'
                for port in host.ports:
                    description += f'Port: {port[0]}/{port[1]}\n'
                self.createAndAddVulnToHost(
                    hostId,
                    'New host active',
                    description,
                    ['Ndiff tool'],
                    'INFO'
                )
            else:
                if host.ports == []:
                    continue
                hostId = self.createAndAddHost(host.ip, '')
                description = 'New service/s found.\n'
                for port in host.ports:
                    description += f'Port: {port[0]}/{port[1]}\n'

                self.createAndAddVulnToHost(
                    hostId,
                    'New ports actives',
                    description,
                    ['Ndiff tool'],
                    'INFO'
                )

    def processCommandString(self, username, current_path, command_string):
        super().processCommandString(username, current_path, command_string)
        if command_string.find('--xml') < 0:
            return f"{command_string} --xml "


def createPlugin(*args, **kwargs):
    return CmdNdiffPlugin(*args, **kwargs)
