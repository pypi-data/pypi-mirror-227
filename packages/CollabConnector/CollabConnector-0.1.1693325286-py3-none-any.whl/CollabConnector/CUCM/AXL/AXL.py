import requests
from requests import Session
from requests.auth import HTTPBasicAuth
import sys
import os
import lxml
from zeep.transports import Transport
from zeep import Client, Settings
from zeep.helpers import serialize_object


requests.packages.urllib3.disable_warnings()


class Connect:
    def __init__(self, ipaddr, username, passwd, version="14.0", wsdl=None):
        # if type= cucm then set username/password for AXL connection
        if ipaddr is None or passwd is None or username is None:
            raise Exception(
                f'Usage: CollabConnector.AXL("ipaddr", "admin", "password", version="12.0", wsdl="./AXL/AXLAPI.wsdl")')
        else:
            self.username = username

            if wsdl:
                wsdl = wsdl
            elif version and int(version.split(".")[0]) < 10:
                wsdl = os.path.join(os.path.dirname(__file__), 'schema', '10.0', 'AXLAPI.wsdl')
            elif version:
                wsdl = os.path.join(os.path.dirname(__file__), 'schema', version, 'AXLAPI.wsdl')

            # create a SOAP client session
            session = Session()

            # avoid certificate verification by default and setup session
            session.verify = False
            session.auth = HTTPBasicAuth(username, passwd)
            transport = Transport(session=session, timeout=10)
            settings = Settings(strict=False, xml_huge_tree=True)

            # If WSDL file specified then create AXL SOAP connector
            if wsdl is not None:
                # Create the Zeep client with the specified settings
                client_axl = Client(wsdl, settings=settings, transport=transport)  # ,plugins = plugin )
                # Create the Zeep service binding to AXL at the specified CUCM
                try:
                    self.client = client_axl.create_service(
                        '{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',
                        f'https://{ipaddr}:8443/axl/')

                except Exception as err:
                    print(f"SOAP/AXL Error could not create service: {err}", file=sys.stderr)
                    self.client = False

    def elements_to_dict(self, input):
        if input is None or isinstance(input, (str, int, float, complex, bool, tuple)):
            return input

        if isinstance(input, dict):
            for key, value in input.items():
                input[key] = self.elements_to_dict(value)
            return input

        elif isinstance(input, list):
            return_list = []
            for position in input:
                return_list.append(self.elements_to_dict(position))
            return return_list

        elif isinstance(input, lxml.etree._Element):
            element = {}  # {t.tag : map(etree_to_dict, t.iterchildren())}
            element.update(('@' + k, v) for k, v in input.attrib.iteritems())
            element[input.tag] = input.text
            return element

        else:
            return str(input)

    def getSipProfile(self, **args):
        """
        axl.getSipProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipProfile`: ", str(err), file=sys.stderr)
            return []

    def listSipProfile(self, **args):
        """
        axl.listSipProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipProfile`: ", str(err), file=sys.stderr)
            return []

    def getSipProfileOptions(self, **args):
        """
        axl.getSipProfileOptions parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipProfileOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipProfileOptions`: ", str(err), file=sys.stderr)
            return []

    def getSipTrunkSecurityProfile(self, **args):
        """
        axl.getSipTrunkSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipTrunkSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipTrunkSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listSipTrunkSecurityProfile(self, **args):
        """
        axl.listSipTrunkSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipTrunkSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipTrunkSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getTimePeriod(self, **args):
        """
        axl.getTimePeriod parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTimePeriod(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTimePeriod`: ", str(err), file=sys.stderr)
            return []

    def listTimePeriod(self, **args):
        """
        axl.listTimePeriod parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTimePeriod(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTimePeriod`: ", str(err), file=sys.stderr)
            return []

    def getTimeSchedule(self, **args):
        """
        axl.getTimeSchedule parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTimeSchedule(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTimeSchedule`: ", str(err), file=sys.stderr)
            return []

    def listTimeSchedule(self, **args):
        """
        axl.listTimeSchedule parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTimeSchedule(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTimeSchedule`: ", str(err), file=sys.stderr)
            return []

    def updateTodAccessReq(self, **args):
        """
        axl.updateTodAccessReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateTodAccessReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateTodAccessReq`: ", str(err), file=sys.stderr)
            return []

    def getTodAccess(self, **args):
        """
        axl.getTodAccess parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTodAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTodAccess`: ", str(err), file=sys.stderr)
            return []

    def listTodAccess(self, **args):
        """
        axl.listTodAccess parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTodAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTodAccess`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailPilot(self, **args):
        """
        axl.getVoiceMailPilot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVoiceMailPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailPilot`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailPilot(self, **args):
        """
        axl.listVoiceMailPilot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVoiceMailPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailPilot`: ", str(err), file=sys.stderr)
            return []

    def getProcessNode(self, **args):
        """
        axl.getProcessNode parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getProcessNode(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getProcessNode`: ", str(err), file=sys.stderr)
            return []

    def listProcessNode(self, **args):
        """
        axl.listProcessNode parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listProcessNode(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listProcessNode`: ", str(err), file=sys.stderr)
            return []

    def getCallerFilterList(self, **args):
        """
        axl.getCallerFilterList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallerFilterList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallerFilterList`: ", str(err), file=sys.stderr)
            return []

    def listCallerFilterList(self, **args):
        """
        axl.listCallerFilterList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallerFilterList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallerFilterList`: ", str(err), file=sys.stderr)
            return []

    def getRoutePartition(self, **args):
        """
        axl.getRoutePartition parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRoutePartition(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRoutePartition`: ", str(err), file=sys.stderr)
            return []

    def listRoutePartition(self, **args):
        """
        axl.listRoutePartition parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRoutePartition(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePartition`: ", str(err), file=sys.stderr)
            return []

    def getCss(self, **args):
        """
        axl.getCss parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCss(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCss`: ", str(err), file=sys.stderr)
            return []

    def listCss(self, **args):
        """
        axl.listCss parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCss(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCss`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallManagerReq(self, **args):
        """
        axl.updateCallManagerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallManagerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallManagerReq`: ", str(err), file=sys.stderr)
            return []

    def getCallManager(self, **args):
        """
        axl.getCallManager parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallManager(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallManager`: ", str(err), file=sys.stderr)
            return []

    def listCallManager(self, **args):
        """
        axl.listCallManager parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallManager(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallManager`: ", str(err), file=sys.stderr)
            return []

    def getExpresswayCConfiguration(self, **args):
        """
        axl.getExpresswayCConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getExpresswayCConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getExpresswayCConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listExpresswayCConfiguration(self, **args):
        """
        axl.listExpresswayCConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listExpresswayCConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listExpresswayCConfiguration`: ", str(err), file=sys.stderr)
            return []

    def getMedia(self, **args):
        """
        axl.getMedia parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMedia(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMedia`: ", str(err), file=sys.stderr)
            return []

    def listMedia(self, **args):
        """
        axl.listMedia parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMedia(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMedia`: ", str(err), file=sys.stderr)
            return []

    def getMedia(self, **args):
        """
        axl.getMedia parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMedia(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMedia`: ", str(err), file=sys.stderr)
            return []

    def listMedia(self, **args):
        """
        axl.listMedia parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMedia(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMedia`: ", str(err), file=sys.stderr)
            return []

    def updateRegionReq(self, **args):
        """
        axl.updateRegionReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRegionReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRegionReq`: ", str(err), file=sys.stderr)
            return []

    def getRegion(self, **args):
        """
        axl.getRegion parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRegion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRegion`: ", str(err), file=sys.stderr)
            return []

    def listRegion(self, **args):
        """
        axl.listRegion parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRegion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRegion`: ", str(err), file=sys.stderr)
            return []

    def getAarGroup(self, **args):
        """
        axl.getAarGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAarGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAarGroup`: ", str(err), file=sys.stderr)
            return []

    def listAarGroup(self, **args):
        """
        axl.listAarGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAarGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAarGroup`: ", str(err), file=sys.stderr)
            return []

    def getPhysicalLocation(self, **args):
        """
        axl.getPhysicalLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhysicalLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhysicalLocation`: ", str(err), file=sys.stderr)
            return []

    def listPhysicalLocation(self, **args):
        """
        axl.listPhysicalLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhysicalLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhysicalLocation`: ", str(err), file=sys.stderr)
            return []

    def getCustomer(self, **args):
        """
        axl.getCustomer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCustomer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCustomer`: ", str(err), file=sys.stderr)
            return []

    def listCustomer(self, **args):
        """
        axl.listCustomer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCustomer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCustomer`: ", str(err), file=sys.stderr)
            return []

    def getRouteGroup(self, **args):
        """
        axl.getRouteGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def listRouteGroup(self, **args):
        """
        axl.listRouteGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def updateDevicePoolReq(self, **args):
        """
        axl.updateDevicePoolReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDevicePoolReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDevicePoolReq`: ", str(err), file=sys.stderr)
            return []

    def updateDevicePoolReq(self, **args):
        """
        axl.updateDevicePoolReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDevicePoolReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDevicePoolReq`: ", str(err), file=sys.stderr)
            return []

    def getDevicePool(self, **args):
        """
        axl.getDevicePool parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDevicePool(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDevicePool`: ", str(err), file=sys.stderr)
            return []

    def listDevicePool(self, **args):
        """
        axl.listDevicePool parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDevicePool(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDevicePool`: ", str(err), file=sys.stderr)
            return []

    def getDeviceMobilityGroup(self, **args):
        """
        axl.getDeviceMobilityGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDeviceMobilityGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceMobilityGroup`: ", str(err), file=sys.stderr)
            return []

    def listDeviceMobilityGroup(self, **args):
        """
        axl.listDeviceMobilityGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDeviceMobilityGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceMobilityGroup`: ", str(err), file=sys.stderr)
            return []

    def updateLocationReq(self, **args):
        """
        axl.updateLocationReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocationReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocationReq`: ", str(err), file=sys.stderr)
            return []

    def updateLocationReq(self, **args):
        """
        axl.updateLocationReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocationReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocationReq`: ", str(err), file=sys.stderr)
            return []

    def getLocation(self, **args):
        """
        axl.getLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLocation`: ", str(err), file=sys.stderr)
            return []

    def listLocation(self, **args):
        """
        axl.listLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLocation`: ", str(err), file=sys.stderr)
            return []

    def getSoftKeyTemplate(self, **args):
        """
        axl.getSoftKeyTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSoftKeyTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSoftKeyTemplate`: ", str(err), file=sys.stderr)
            return []

    def listSoftKeyTemplate(self, **args):
        """
        axl.listSoftKeyTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSoftKeyTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSoftKeyTemplate`: ", str(err), file=sys.stderr)
            return []

    def getTranscoder(self, **args):
        """
        axl.getTranscoder parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTranscoder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTranscoder`: ", str(err), file=sys.stderr)
            return []

    def listTranscoder(self, **args):
        """
        axl.listTranscoder parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTranscoder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTranscoder`: ", str(err), file=sys.stderr)
            return []

    def updateCommonDeviceConfigReq(self, **args):
        """
        axl.updateCommonDeviceConfigReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCommonDeviceConfigReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCommonDeviceConfigReq`: ", str(err), file=sys.stderr)
            return []

    def updateCommonDeviceConfigReq(self, **args):
        """
        axl.updateCommonDeviceConfigReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCommonDeviceConfigReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCommonDeviceConfigReq`: ", str(err), file=sys.stderr)
            return []

    def getCommonDeviceConfig(self, **args):
        """
        axl.getCommonDeviceConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCommonDeviceConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCommonDeviceConfig`: ", str(err), file=sys.stderr)
            return []

    def listCommonDeviceConfig(self, **args):
        """
        axl.listCommonDeviceConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCommonDeviceConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCommonDeviceConfig`: ", str(err), file=sys.stderr)
            return []

    def get(self, **args):
        """
        axl.get parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.get(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `get`: ", str(err), file=sys.stderr)
            return []

    def list(self, **args):
        """
        axl.list parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.list(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `list`: ", str(err), file=sys.stderr)
            return []

    def get(self, **args):
        """
        axl.get parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.get(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `get`: ", str(err), file=sys.stderr)
            return []

    def list(self, **args):
        """
        axl.list parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.list(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `list`: ", str(err), file=sys.stderr)
            return []

    def getDeviceMobility(self, **args):
        """
        axl.getDeviceMobility parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDeviceMobility(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceMobility`: ", str(err), file=sys.stderr)
            return []

    def listDeviceMobility(self, **args):
        """
        axl.listDeviceMobility parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDeviceMobility(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceMobility`: ", str(err), file=sys.stderr)
            return []

    def getCmcInfo(self, **args):
        """
        axl.getCmcInfo parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCmcInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCmcInfo`: ", str(err), file=sys.stderr)
            return []

    def listCmcInfo(self, **args):
        """
        axl.listCmcInfo parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCmcInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCmcInfo`: ", str(err), file=sys.stderr)
            return []

    def getCredentialPolicy(self, **args):
        """
        axl.getCredentialPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCredentialPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCredentialPolicy`: ", str(err), file=sys.stderr)
            return []

    def listCredentialPolicy(self, **args):
        """
        axl.listCredentialPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCredentialPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCredentialPolicy`: ", str(err), file=sys.stderr)
            return []

    def getFacInfo(self, **args):
        """
        axl.getFacInfo parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFacInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFacInfo`: ", str(err), file=sys.stderr)
            return []

    def listFacInfo(self, **args):
        """
        axl.listFacInfo parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listFacInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFacInfo`: ", str(err), file=sys.stderr)
            return []

    def getHuntList(self, **args):
        """
        axl.getHuntList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getHuntList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHuntList`: ", str(err), file=sys.stderr)
            return []

    def listHuntList(self, **args):
        """
        axl.listHuntList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listHuntList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listHuntList`: ", str(err), file=sys.stderr)
            return []

    def getIvrUserLocale(self, **args):
        """
        axl.getIvrUserLocale parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getIvrUserLocale(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIvrUserLocale`: ", str(err), file=sys.stderr)
            return []

    def listIvrUserLocale(self, **args):
        """
        axl.listIvrUserLocale parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listIvrUserLocale(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listIvrUserLocale`: ", str(err), file=sys.stderr)
            return []

    def getLineGroup(self, **args):
        """
        axl.getLineGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLineGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLineGroup`: ", str(err), file=sys.stderr)
            return []

    def listLineGroup(self, **args):
        """
        axl.listLineGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLineGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLineGroup`: ", str(err), file=sys.stderr)
            return []

    def getRecordingProfile(self, **args):
        """
        axl.getRecordingProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRecordingProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRecordingProfile`: ", str(err), file=sys.stderr)
            return []

    def listRecordingProfile(self, **args):
        """
        axl.listRecordingProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRecordingProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRecordingProfile`: ", str(err), file=sys.stderr)
            return []

    def getRouteFilter(self, **args):
        """
        axl.getRouteFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRouteFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteFilter`: ", str(err), file=sys.stderr)
            return []

    def listRouteFilter(self, **args):
        """
        axl.listRouteFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRouteFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteFilter`: ", str(err), file=sys.stderr)
            return []

    def getCallManagerGroup(self, **args):
        """
        axl.getCallManagerGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallManagerGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallManagerGroup`: ", str(err), file=sys.stderr)
            return []

    def listCallManagerGroup(self, **args):
        """
        axl.listCallManagerGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallManagerGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallManagerGroup`: ", str(err), file=sys.stderr)
            return []

    def getUserGroup(self, **args):
        """
        axl.getUserGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUserGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUserGroup`: ", str(err), file=sys.stderr)
            return []

    def listUserGroup(self, **args):
        """
        axl.listUserGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUserGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUserGroup`: ", str(err), file=sys.stderr)
            return []

    def getDialPlan(self, **args):
        """
        axl.getDialPlan parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDialPlan(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDialPlan`: ", str(err), file=sys.stderr)
            return []

    def listDialPlan(self, **args):
        """
        axl.listDialPlan parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDialPlan(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDialPlan`: ", str(err), file=sys.stderr)
            return []

    def getDialPlanTag(self, **args):
        """
        axl.getDialPlanTag parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDialPlanTag(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDialPlanTag`: ", str(err), file=sys.stderr)
            return []

    def listDialPlanTag(self, **args):
        """
        axl.listDialPlanTag parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDialPlanTag(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDialPlanTag`: ", str(err), file=sys.stderr)
            return []

    def getDdi(self, **args):
        """
        axl.getDdi parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDdi(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDdi`: ", str(err), file=sys.stderr)
            return []

    def listDdi(self, **args):
        """
        axl.listDdi parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDdi(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDdi`: ", str(err), file=sys.stderr)
            return []

    def getMobileSmartClientProfile(self, **args):
        """
        axl.getMobileSmartClientProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMobileSmartClientProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobileSmartClientProfile`: ", str(err), file=sys.stderr)
            return []

    def listMobileSmartClientProfile(self, **args):
        """
        axl.listMobileSmartClientProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMobileSmartClientProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMobileSmartClientProfile`: ", str(err), file=sys.stderr)
            return []

    def getProcessNodeService(self, **args):
        """
        axl.getProcessNodeService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getProcessNodeService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getProcessNodeService`: ", str(err), file=sys.stderr)
            return []

    def listProcessNodeService(self, **args):
        """
        axl.listProcessNodeService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listProcessNodeService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listProcessNodeService`: ", str(err), file=sys.stderr)
            return []

    def getMohAudioSource(self, **args):
        """
        axl.getMohAudioSource parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMohAudioSource(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def listMohAudioSource(self, **args):
        """
        axl.listMohAudioSource parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMohAudioSource(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def getDhcpServer(self, **args):
        """
        axl.getDhcpServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDhcpServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDhcpServer`: ", str(err), file=sys.stderr)
            return []

    def listDhcpServer(self, **args):
        """
        axl.listDhcpServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDhcpServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDhcpServer`: ", str(err), file=sys.stderr)
            return []

    def getDhcpSubnet(self, **args):
        """
        axl.getDhcpSubnet parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDhcpSubnet(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDhcpSubnet`: ", str(err), file=sys.stderr)
            return []

    def listDhcpSubnet(self, **args):
        """
        axl.listDhcpSubnet parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDhcpSubnet(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDhcpSubnet`: ", str(err), file=sys.stderr)
            return []

    def getCallPark(self, **args):
        """
        axl.getCallPark parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallPark`: ", str(err), file=sys.stderr)
            return []

    def listCallPark(self, **args):
        """
        axl.listCallPark parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallPark`: ", str(err), file=sys.stderr)
            return []

    def getDirectedCallPark(self, **args):
        """
        axl.getDirectedCallPark parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDirectedCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirectedCallPark`: ", str(err), file=sys.stderr)
            return []

    def listDirectedCallPark(self, **args):
        """
        axl.listDirectedCallPark parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDirectedCallPark(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirectedCallPark`: ", str(err), file=sys.stderr)
            return []

    def getMeetMe(self, **args):
        """
        axl.getMeetMe parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMeetMe(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMeetMe`: ", str(err), file=sys.stderr)
            return []

    def listMeetMe(self, **args):
        """
        axl.listMeetMe parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMeetMe(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMeetMe`: ", str(err), file=sys.stderr)
            return []

    def getConferenceNow(self, **args):
        """
        axl.getConferenceNow parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getConferenceNow(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getConferenceNow`: ", str(err), file=sys.stderr)
            return []

    def listConferenceNow(self, **args):
        """
        axl.listConferenceNow parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listConferenceNow(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listConferenceNow`: ", str(err), file=sys.stderr)
            return []

    def getMobileVoiceAccess(self, **args):
        """
        axl.getMobileVoiceAccess parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMobileVoiceAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobileVoiceAccess`: ", str(err), file=sys.stderr)
            return []

    def getRouteList(self, **args):
        """
        axl.getRouteList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRouteList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRouteList`: ", str(err), file=sys.stderr)
            return []

    def listRouteList(self, **args):
        """
        axl.listRouteList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRouteList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRouteList`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateUserReq(self, **args):
        """
        axl.updateUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUserReq`: ", str(err), file=sys.stderr)
            return []

    def getUser(self, **args):
        """
        axl.getUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUser`: ", str(err), file=sys.stderr)
            return []

    def listUser(self, **args):
        """
        axl.listUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUser`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def updateAppUserReq(self, **args):
        """
        axl.updateAppUserReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAppUserReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAppUserReq`: ", str(err), file=sys.stderr)
            return []

    def getAppUser(self, **args):
        """
        axl.getAppUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAppUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAppUser`: ", str(err), file=sys.stderr)
            return []

    def listAppUser(self, **args):
        """
        axl.listAppUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAppUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAppUser`: ", str(err), file=sys.stderr)
            return []

    def getSipRealm(self, **args):
        """
        axl.getSipRealm parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipRealm(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipRealm`: ", str(err), file=sys.stderr)
            return []

    def listSipRealm(self, **args):
        """
        axl.listSipRealm parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipRealm(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipRealm`: ", str(err), file=sys.stderr)
            return []

    def getPhoneNtp(self, **args):
        """
        axl.getPhoneNtp parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhoneNtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneNtp`: ", str(err), file=sys.stderr)
            return []

    def listPhoneNtp(self, **args):
        """
        axl.listPhoneNtp parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhoneNtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneNtp`: ", str(err), file=sys.stderr)
            return []

    def getDateTimeGroup(self, **args):
        """
        axl.getDateTimeGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDateTimeGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDateTimeGroup`: ", str(err), file=sys.stderr)
            return []

    def listDateTimeGroup(self, **args):
        """
        axl.listDateTimeGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDateTimeGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDateTimeGroup`: ", str(err), file=sys.stderr)
            return []

    def updatePresenceGroupReq(self, **args):
        """
        axl.updatePresenceGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePresenceGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePresenceGroupReq`: ", str(err), file=sys.stderr)
            return []

    def getPresenceGroup(self, **args):
        """
        axl.getPresenceGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPresenceGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPresenceGroup`: ", str(err), file=sys.stderr)
            return []

    def listPresenceGroup(self, **args):
        """
        axl.listPresenceGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPresenceGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPresenceGroup`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocation(self, **args):
        """
        axl.getGeoLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGeoLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocation`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocation(self, **args):
        """
        axl.listGeoLocation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listGeoLocation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocation`: ", str(err), file=sys.stderr)
            return []

    def getSrst(self, **args):
        """
        axl.getSrst parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSrst(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSrst`: ", str(err), file=sys.stderr)
            return []

    def listSrst(self, **args):
        """
        axl.listSrst parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSrst(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSrst`: ", str(err), file=sys.stderr)
            return []

    def getMlppDomain(self, **args):
        """
        axl.getMlppDomain parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMlppDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMlppDomain`: ", str(err), file=sys.stderr)
            return []

    def listMlppDomain(self, **args):
        """
        axl.listMlppDomain parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMlppDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMlppDomain`: ", str(err), file=sys.stderr)
            return []

    def getCumaServerSecurityProfile(self, **args):
        """
        axl.getCumaServerSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCumaServerSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCumaServerSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listCumaServerSecurityProfile(self, **args):
        """
        axl.listCumaServerSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCumaServerSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCumaServerSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getApplicationServer(self, **args):
        """
        axl.getApplicationServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getApplicationServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationServer`: ", str(err), file=sys.stderr)
            return []

    def listApplicationServer(self, **args):
        """
        axl.listApplicationServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listApplicationServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationServer`: ", str(err), file=sys.stderr)
            return []

    def getApplicationUserCapfProfile(self, **args):
        """
        axl.getApplicationUserCapfProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getApplicationUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def listApplicationUserCapfProfile(self, **args):
        """
        axl.listApplicationUserCapfProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listApplicationUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def getEndUserCapfProfile(self, **args):
        """
        axl.getEndUserCapfProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getEndUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEndUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def listEndUserCapfProfile(self, **args):
        """
        axl.listEndUserCapfProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listEndUserCapfProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listEndUserCapfProfile`: ", str(err), file=sys.stderr)
            return []

    def getServiceParameter(self, **args):
        """
        axl.getServiceParameter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getServiceParameter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getServiceParameter`: ", str(err), file=sys.stderr)
            return []

    def listServiceParameter(self, **args):
        """
        axl.listServiceParameter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listServiceParameter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listServiceParameter`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocationFilter(self, **args):
        """
        axl.getGeoLocationFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGeoLocationFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocationFilter`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocationFilter(self, **args):
        """
        axl.listGeoLocationFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listGeoLocationFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocationFilter`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailProfile(self, **args):
        """
        axl.getVoiceMailProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVoiceMailProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailProfile`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailProfile(self, **args):
        """
        axl.listVoiceMailProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVoiceMailProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailProfile`: ", str(err), file=sys.stderr)
            return []

    def getVoiceMailPort(self, **args):
        """
        axl.getVoiceMailPort parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVoiceMailPort(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVoiceMailPort`: ", str(err), file=sys.stderr)
            return []

    def listVoiceMailPort(self, **args):
        """
        axl.listVoiceMailPort parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVoiceMailPort(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVoiceMailPort`: ", str(err), file=sys.stderr)
            return []

    def getGatekeeper(self, **args):
        """
        axl.getGatekeeper parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatekeeper(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatekeeper`: ", str(err), file=sys.stderr)
            return []

    def listGatekeeper(self, **args):
        """
        axl.listGatekeeper parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listGatekeeper(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGatekeeper`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneButtonTemplateReq(self, **args):
        """
        axl.updatePhoneButtonTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneButtonTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneButtonTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def getPhoneButtonTemplate(self, **args):
        """
        axl.getPhoneButtonTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhoneButtonTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneButtonTemplate`: ", str(err), file=sys.stderr)
            return []

    def listPhoneButtonTemplate(self, **args):
        """
        axl.listPhoneButtonTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhoneButtonTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneButtonTemplate`: ", str(err), file=sys.stderr)
            return []

    def getCommonPhoneConfig(self, **args):
        """
        axl.getCommonPhoneConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCommonPhoneConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCommonPhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def listCommonPhoneConfig(self, **args):
        """
        axl.listCommonPhoneConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCommonPhoneConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCommonPhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def getMessageWaiting(self, **args):
        """
        axl.getMessageWaiting parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMessageWaiting(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMessageWaiting`: ", str(err), file=sys.stderr)
            return []

    def listMessageWaiting(self, **args):
        """
        axl.listMessageWaiting parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMessageWaiting(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMessageWaiting`: ", str(err), file=sys.stderr)
            return []

    def getIpPhoneServices(self, **args):
        """
        axl.getIpPhoneServices parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getIpPhoneServices(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIpPhoneServices`: ", str(err), file=sys.stderr)
            return []

    def listIpPhoneServices(self, **args):
        """
        axl.listIpPhoneServices parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listIpPhoneServices(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listIpPhoneServices`: ", str(err), file=sys.stderr)
            return []

    def getCtiRoutePoint(self, **args):
        """
        axl.getCtiRoutePoint parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCtiRoutePoint(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCtiRoutePoint`: ", str(err), file=sys.stderr)
            return []

    def listCtiRoutePoint(self, **args):
        """
        axl.listCtiRoutePoint parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCtiRoutePoint(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCtiRoutePoint`: ", str(err), file=sys.stderr)
            return []

    def getTransPattern(self, **args):
        """
        axl.getTransPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTransPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransPattern`: ", str(err), file=sys.stderr)
            return []

    def listTransPattern(self, **args):
        """
        axl.listTransPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTransPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTransPattern`: ", str(err), file=sys.stderr)
            return []

    def getTransPatternOptions(self, **args):
        """
        axl.getTransPatternOptions parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTransPatternOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransPatternOptions`: ", str(err), file=sys.stderr)
            return []

    def getCallingPartyTransformationPattern(self, **args):
        """
        axl.getCallingPartyTransformationPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallingPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallingPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def listCallingPartyTransformationPattern(self, **args):
        """
        axl.listCallingPartyTransformationPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallingPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallingPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def getSipRoutePattern(self, **args):
        """
        axl.getSipRoutePattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def listSipRoutePattern(self, **args):
        """
        axl.listSipRoutePattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def updateHuntPilotReq(self, **args):
        """
        axl.updateHuntPilotReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateHuntPilotReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateHuntPilotReq`: ", str(err), file=sys.stderr)
            return []

    def getHuntPilot(self, **args):
        """
        axl.getHuntPilot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getHuntPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHuntPilot`: ", str(err), file=sys.stderr)
            return []

    def listHuntPilot(self, **args):
        """
        axl.listHuntPilot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listHuntPilot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listHuntPilot`: ", str(err), file=sys.stderr)
            return []

    def updateRoutePatternReq(self, **args):
        """
        axl.updateRoutePatternReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRoutePatternReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRoutePatternReq`: ", str(err), file=sys.stderr)
            return []

    def updateRoutePatternReq(self, **args):
        """
        axl.updateRoutePatternReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRoutePatternReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRoutePatternReq`: ", str(err), file=sys.stderr)
            return []

    def updateRoutePatternReq(self, **args):
        """
        axl.updateRoutePatternReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRoutePatternReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRoutePatternReq`: ", str(err), file=sys.stderr)
            return []

    def updateRoutePatternReq(self, **args):
        """
        axl.updateRoutePatternReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRoutePatternReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRoutePatternReq`: ", str(err), file=sys.stderr)
            return []

    def getRoutePattern(self, **args):
        """
        axl.getRoutePattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def listRoutePattern(self, **args):
        """
        axl.listRoutePattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRoutePattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePattern`: ", str(err), file=sys.stderr)
            return []

    def getApplicationDialRules(self, **args):
        """
        axl.getApplicationDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getApplicationDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getApplicationDialRules`: ", str(err), file=sys.stderr)
            return []

    def listApplicationDialRules(self, **args):
        """
        axl.listApplicationDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listApplicationDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listApplicationDialRules`: ", str(err), file=sys.stderr)
            return []

    def getDirectoryLookupDialRules(self, **args):
        """
        axl.getDirectoryLookupDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDirectoryLookupDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirectoryLookupDialRules`: ", str(err), file=sys.stderr)
            return []

    def listDirectoryLookupDialRules(self, **args):
        """
        axl.listDirectoryLookupDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDirectoryLookupDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirectoryLookupDialRules`: ", str(err), file=sys.stderr)
            return []

    def getPhoneSecurityProfile(self, **args):
        """
        axl.getPhoneSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhoneSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listPhoneSecurityProfile(self, **args):
        """
        axl.listPhoneSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhoneSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getSipDialRules(self, **args):
        """
        axl.getSipDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipDialRules`: ", str(err), file=sys.stderr)
            return []

    def listSipDialRules(self, **args):
        """
        axl.listSipDialRules parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipDialRules(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipDialRules`: ", str(err), file=sys.stderr)
            return []

    def updateConferenceBridgeReq(self, **args):
        """
        axl.updateConferenceBridgeReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateConferenceBridgeReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateConferenceBridgeReq`: ", str(err), file=sys.stderr)
            return []

    def updateConferenceBridgeReq(self, **args):
        """
        axl.updateConferenceBridgeReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateConferenceBridgeReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateConferenceBridgeReq`: ", str(err), file=sys.stderr)
            return []

    def getConferenceBridge(self, **args):
        """
        axl.getConferenceBridge parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getConferenceBridge(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getConferenceBridge`: ", str(err), file=sys.stderr)
            return []

    def listConferenceBridge(self, **args):
        """
        axl.listConferenceBridge parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listConferenceBridge(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listConferenceBridge`: ", str(err), file=sys.stderr)
            return []

    def getAnnunciator(self, **args):
        """
        axl.getAnnunciator parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAnnunciator(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAnnunciator`: ", str(err), file=sys.stderr)
            return []

    def listAnnunciator(self, **args):
        """
        axl.listAnnunciator parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAnnunciator(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAnnunciator`: ", str(err), file=sys.stderr)
            return []

    def getInteractiveVoice(self, **args):
        """
        axl.getInteractiveVoice parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getInteractiveVoice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInteractiveVoice`: ", str(err), file=sys.stderr)
            return []

    def listInteractiveVoice(self, **args):
        """
        axl.listInteractiveVoice parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listInteractiveVoice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listInteractiveVoice`: ", str(err), file=sys.stderr)
            return []

    def getMtp(self, **args):
        """
        axl.getMtp parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMtp`: ", str(err), file=sys.stderr)
            return []

    def listMtp(self, **args):
        """
        axl.listMtp parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMtp(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMtp`: ", str(err), file=sys.stderr)
            return []

    def getFixedMohAudioSource(self, **args):
        """
        axl.getFixedMohAudioSource parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFixedMohAudioSource(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFixedMohAudioSource`: ", str(err), file=sys.stderr)
            return []

    def getRemoteDestinationProfile(self, **args):
        """
        axl.getRemoteDestinationProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRemoteDestinationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteDestinationProfile`: ", str(err), file=sys.stderr)
            return []

    def listRemoteDestinationProfile(self, **args):
        """
        axl.listRemoteDestinationProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRemoteDestinationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteDestinationProfile`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def updateLineReq(self, **args):
        """
        axl.updateLineReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLineReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLineReq`: ", str(err), file=sys.stderr)
            return []

    def getLine(self, **args):
        """
        axl.getLine parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLine(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLine`: ", str(err), file=sys.stderr)
            return []

    def listLine(self, **args):
        """
        axl.listLine parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLine(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLine`: ", str(err), file=sys.stderr)
            return []

    def getLineOptions(self, **args):
        """
        axl.getLineOptions parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLineOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLineOptions`: ", str(err), file=sys.stderr)
            return []

    def getDefaultDeviceProfile(self, **args):
        """
        axl.getDefaultDeviceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDefaultDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDefaultDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def listDefaultDeviceProfile(self, **args):
        """
        axl.listDefaultDeviceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDefaultDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDefaultDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def updateH323PhoneReq(self, **args):
        """
        axl.updateH323PhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323PhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323PhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updateH323PhoneReq(self, **args):
        """
        axl.updateH323PhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323PhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323PhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updateH323PhoneReq(self, **args):
        """
        axl.updateH323PhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323PhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323PhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updateH323PhoneReq(self, **args):
        """
        axl.updateH323PhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323PhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323PhoneReq`: ", str(err), file=sys.stderr)
            return []

    def getH323Phone(self, **args):
        """
        axl.getH323Phone parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getH323Phone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Phone`: ", str(err), file=sys.stderr)
            return []

    def listH323Phone(self, **args):
        """
        axl.listH323Phone parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listH323Phone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Phone`: ", str(err), file=sys.stderr)
            return []

    def updateMohServerReq(self, **args):
        """
        axl.updateMohServerReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateMohServerReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateMohServerReq`: ", str(err), file=sys.stderr)
            return []

    def getMohServer(self, **args):
        """
        axl.getMohServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMohServer`: ", str(err), file=sys.stderr)
            return []

    def listMohServer(self, **args):
        """
        axl.listMohServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMohServer`: ", str(err), file=sys.stderr)
            return []

    def updateH323TrunkReq(self, **args):
        """
        axl.updateH323TrunkReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323TrunkReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323TrunkReq`: ", str(err), file=sys.stderr)
            return []

    def updateH323TrunkReq(self, **args):
        """
        axl.updateH323TrunkReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323TrunkReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323TrunkReq`: ", str(err), file=sys.stderr)
            return []

    def getH323Trunk(self, **args):
        """
        axl.getH323Trunk parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getH323Trunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Trunk`: ", str(err), file=sys.stderr)
            return []

    def listH323Trunk(self, **args):
        """
        axl.listH323Trunk parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listH323Trunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Trunk`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def updatePhoneReq(self, **args):
        """
        axl.updatePhoneReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePhoneReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePhoneReq`: ", str(err), file=sys.stderr)
            return []

    def getPhone(self, **args):
        """
        axl.getPhone parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhone`: ", str(err), file=sys.stderr)
            return []

    def listPhone(self, **args):
        """
        axl.listPhone parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhone(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhone`: ", str(err), file=sys.stderr)
            return []

    def getPhoneOptions(self, **args):
        """
        axl.getPhoneOptions parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPhoneOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPhoneOptions`: ", str(err), file=sys.stderr)
            return []

    def updateH323GatewayReq(self, **args):
        """
        axl.updateH323GatewayReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323GatewayReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323GatewayReq`: ", str(err), file=sys.stderr)
            return []

    def updateH323GatewayReq(self, **args):
        """
        axl.updateH323GatewayReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateH323GatewayReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateH323GatewayReq`: ", str(err), file=sys.stderr)
            return []

    def getH323Gateway(self, **args):
        """
        axl.getH323Gateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getH323Gateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getH323Gateway`: ", str(err), file=sys.stderr)
            return []

    def listH323Gateway(self, **args):
        """
        axl.listH323Gateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listH323Gateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listH323Gateway`: ", str(err), file=sys.stderr)
            return []

    def updateDeviceProfileReq(self, **args):
        """
        axl.updateDeviceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDeviceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDeviceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def updateDeviceProfileReq(self, **args):
        """
        axl.updateDeviceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDeviceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDeviceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def updateDeviceProfileReq(self, **args):
        """
        axl.updateDeviceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDeviceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDeviceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def updateDeviceProfileReq(self, **args):
        """
        axl.updateDeviceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDeviceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDeviceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def updateDeviceProfileReq(self, **args):
        """
        axl.updateDeviceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDeviceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDeviceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def getDeviceProfile(self, **args):
        """
        axl.getDeviceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def listDeviceProfile(self, **args):
        """
        axl.listDeviceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDeviceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceProfile`: ", str(err), file=sys.stderr)
            return []

    def getDeviceProfileOptions(self, **args):
        """
        axl.getDeviceProfileOptions parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDeviceProfileOptions(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceProfileOptions`: ", str(err), file=sys.stderr)
            return []

    def updateRemoteDestinationReq(self, **args):
        """
        axl.updateRemoteDestinationReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateRemoteDestinationReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateRemoteDestinationReq`: ", str(err), file=sys.stderr)
            return []

    def getRemoteDestination(self, **args):
        """
        axl.getRemoteDestination parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRemoteDestination(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteDestination`: ", str(err), file=sys.stderr)
            return []

    def listRemoteDestination(self, **args):
        """
        axl.listRemoteDestination parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRemoteDestination(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteDestination`: ", str(err), file=sys.stderr)
            return []

    def getVg224(self, **args):
        """
        axl.getVg224 parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVg224(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVg224`: ", str(err), file=sys.stderr)
            return []

    def getGateway(self, **args):
        """
        axl.getGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGateway`: ", str(err), file=sys.stderr)
            return []

    def listGateway(self, **args):
        """
        axl.listGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGateway`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointAnalogAccess(self, **args):
        """
        axl.getGatewayEndpointAnalogAccess parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatewayEndpointAnalogAccess(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointAnalogAccess`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessPri(self, **args):
        """
        axl.getGatewayEndpointDigitalAccessPri parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatewayEndpointDigitalAccessPri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessPri`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessBri(self, **args):
        """
        axl.getGatewayEndpointDigitalAccessBri parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatewayEndpointDigitalAccessBri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessBri`: ", str(err), file=sys.stderr)
            return []

    def getGatewayEndpointDigitalAccessT1(self, **args):
        """
        axl.getGatewayEndpointDigitalAccessT1 parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatewayEndpointDigitalAccessT1(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewayEndpointDigitalAccessT1`: ", str(err), file=sys.stderr)
            return []

    def updateCiscoCatalyst600024PortFXSGatewayReq(self, **args):
        """
        axl.updateCiscoCatalyst600024PortFXSGatewayReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCiscoCatalyst600024PortFXSGatewayReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCiscoCatalyst600024PortFXSGatewayReq`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst600024PortFXSGateway(self, **args):
        """
        axl.getCiscoCatalyst600024PortFXSGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCiscoCatalyst600024PortFXSGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst600024PortFXSGateway`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst600024PortFXSGateway(self, **args):
        """
        axl.listCiscoCatalyst600024PortFXSGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCiscoCatalyst600024PortFXSGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst600024PortFXSGateway`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000E1VoIPGateway(self, **args):
        """
        axl.getCiscoCatalyst6000E1VoIPGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCiscoCatalyst6000E1VoIPGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000E1VoIPGateway`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000E1VoIPGateway(self, **args):
        """
        axl.listCiscoCatalyst6000E1VoIPGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCiscoCatalyst6000E1VoIPGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000E1VoIPGateway`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000T1VoIPGatewayPri(self, **args):
        """
        axl.getCiscoCatalyst6000T1VoIPGatewayPri parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCiscoCatalyst6000T1VoIPGatewayPri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000T1VoIPGatewayPri`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000T1VoIPGatewayPri(self, **args):
        """
        axl.listCiscoCatalyst6000T1VoIPGatewayPri parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCiscoCatalyst6000T1VoIPGatewayPri(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000T1VoIPGatewayPri`: ", str(err), file=sys.stderr)
            return []

    def updateCiscoCatalyst6000T1VoIPGatewayT1Req(self, **args):
        """
        axl.updateCiscoCatalyst6000T1VoIPGatewayT1Req parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCiscoCatalyst6000T1VoIPGatewayT1Req(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCiscoCatalyst6000T1VoIPGatewayT1Req`: ", str(err), file=sys.stderr)
            return []

    def getCiscoCatalyst6000T1VoIPGatewayT1(self, **args):
        """
        axl.getCiscoCatalyst6000T1VoIPGatewayT1 parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCiscoCatalyst6000T1VoIPGatewayT1(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCiscoCatalyst6000T1VoIPGatewayT1`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCatalyst6000T1VoIPGatewayT1(self, **args):
        """
        axl.listCiscoCatalyst6000T1VoIPGatewayT1 parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCiscoCatalyst6000T1VoIPGatewayT1(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCatalyst6000T1VoIPGatewayT1`: ", str(err), file=sys.stderr)
            return []

    def updateCallPickupGroupReq(self, **args):
        """
        axl.updateCallPickupGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallPickupGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallPickupGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updateCallPickupGroupReq(self, **args):
        """
        axl.updateCallPickupGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateCallPickupGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateCallPickupGroupReq`: ", str(err), file=sys.stderr)
            return []

    def getCallPickupGroup(self, **args):
        """
        axl.getCallPickupGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCallPickupGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCallPickupGroup`: ", str(err), file=sys.stderr)
            return []

    def listCallPickupGroup(self, **args):
        """
        axl.listCallPickupGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCallPickupGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCallPickupGroup`: ", str(err), file=sys.stderr)
            return []

    def listRoutePlan(self, **args):
        """
        axl.listRoutePlan parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRoutePlan(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRoutePlan`: ", str(err), file=sys.stderr)
            return []

    def getGeoLocationPolicy(self, **args):
        """
        axl.getGeoLocationPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGeoLocationPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGeoLocationPolicy`: ", str(err), file=sys.stderr)
            return []

    def listGeoLocationPolicy(self, **args):
        """
        axl.listGeoLocationPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listGeoLocationPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listGeoLocationPolicy`: ", str(err), file=sys.stderr)
            return []

    def updateSipTrunkReq(self, **args):
        """
        axl.updateSipTrunkReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateSipTrunkReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateSipTrunkReq`: ", str(err), file=sys.stderr)
            return []

    def updateSipTrunkReq(self, **args):
        """
        axl.updateSipTrunkReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateSipTrunkReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateSipTrunkReq`: ", str(err), file=sys.stderr)
            return []

    def getSipTrunk(self, **args):
        """
        axl.getSipTrunk parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSipTrunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSipTrunk`: ", str(err), file=sys.stderr)
            return []

    def listSipTrunk(self, **args):
        """
        axl.listSipTrunk parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSipTrunk(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSipTrunk`: ", str(err), file=sys.stderr)
            return []

    def getCalledPartyTransformationPattern(self, **args):
        """
        axl.getCalledPartyTransformationPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCalledPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCalledPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def listCalledPartyTransformationPattern(self, **args):
        """
        axl.listCalledPartyTransformationPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCalledPartyTransformationPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCalledPartyTransformationPattern`: ", str(err), file=sys.stderr)
            return []

    def getExternalCallControlProfile(self, **args):
        """
        axl.getExternalCallControlProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getExternalCallControlProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getExternalCallControlProfile`: ", str(err), file=sys.stderr)
            return []

    def listExternalCallControlProfile(self, **args):
        """
        axl.listExternalCallControlProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listExternalCallControlProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listExternalCallControlProfile`: ", str(err), file=sys.stderr)
            return []

    def getSafSecurityProfile(self, **args):
        """
        axl.getSafSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSafSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def listSafSecurityProfile(self, **args):
        """
        axl.listSafSecurityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSafSecurityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafSecurityProfile`: ", str(err), file=sys.stderr)
            return []

    def getSafForwarder(self, **args):
        """
        axl.getSafForwarder parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSafForwarder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafForwarder`: ", str(err), file=sys.stderr)
            return []

    def listSafForwarder(self, **args):
        """
        axl.listSafForwarder parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSafForwarder(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafForwarder`: ", str(err), file=sys.stderr)
            return []

    def getCcdHostedDN(self, **args):
        """
        axl.getCcdHostedDN parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCcdHostedDN(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdHostedDN`: ", str(err), file=sys.stderr)
            return []

    def listCcdHostedDN(self, **args):
        """
        axl.listCcdHostedDN parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCcdHostedDN(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdHostedDN`: ", str(err), file=sys.stderr)
            return []

    def getCcdHostedDNGroup(self, **args):
        """
        axl.getCcdHostedDNGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCcdHostedDNGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdHostedDNGroup`: ", str(err), file=sys.stderr)
            return []

    def listCcdHostedDNGroup(self, **args):
        """
        axl.listCcdHostedDNGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCcdHostedDNGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdHostedDNGroup`: ", str(err), file=sys.stderr)
            return []

    def getCcdRequestingService(self, **args):
        """
        axl.getCcdRequestingService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCcdRequestingService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdRequestingService`: ", str(err), file=sys.stderr)
            return []

    def getInterClusterServiceProfile(self, **args):
        """
        axl.getInterClusterServiceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getInterClusterServiceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInterClusterServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def getRemoteCluster(self, **args):
        """
        axl.getRemoteCluster parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRemoteCluster(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRemoteCluster`: ", str(err), file=sys.stderr)
            return []

    def listRemoteCluster(self, **args):
        """
        axl.listRemoteCluster parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRemoteCluster(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRemoteCluster`: ", str(err), file=sys.stderr)
            return []

    def getCcdAdvertisingService(self, **args):
        """
        axl.getCcdAdvertisingService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCcdAdvertisingService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdAdvertisingService`: ", str(err), file=sys.stderr)
            return []

    def listCcdAdvertisingService(self, **args):
        """
        axl.listCcdAdvertisingService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCcdAdvertisingService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCcdAdvertisingService`: ", str(err), file=sys.stderr)
            return []

    def updateLdapDirectoryReq(self, **args):
        """
        axl.updateLdapDirectoryReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLdapDirectoryReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLdapDirectoryReq`: ", str(err), file=sys.stderr)
            return []

    def updateLdapDirectoryReq(self, **args):
        """
        axl.updateLdapDirectoryReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLdapDirectoryReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLdapDirectoryReq`: ", str(err), file=sys.stderr)
            return []

    def getLdapDirectory(self, **args):
        """
        axl.getLdapDirectory parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapDirectory(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapDirectory`: ", str(err), file=sys.stderr)
            return []

    def listLdapDirectory(self, **args):
        """
        axl.listLdapDirectory parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLdapDirectory(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapDirectory`: ", str(err), file=sys.stderr)
            return []

    def getEmccFeatureConfig(self, **args):
        """
        axl.getEmccFeatureConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getEmccFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEmccFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getSafCcdPurgeBlockLearnedRoutes(self, **args):
        """
        axl.getSafCcdPurgeBlockLearnedRoutes parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSafCcdPurgeBlockLearnedRoutes(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSafCcdPurgeBlockLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def listSafCcdPurgeBlockLearnedRoutes(self, **args):
        """
        axl.listSafCcdPurgeBlockLearnedRoutes parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSafCcdPurgeBlockLearnedRoutes(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSafCcdPurgeBlockLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def updateVpnGatewayReq(self, **args):
        """
        axl.updateVpnGatewayReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateVpnGatewayReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateVpnGatewayReq`: ", str(err), file=sys.stderr)
            return []

    def getVpnGateway(self, **args):
        """
        axl.getVpnGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVpnGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnGateway`: ", str(err), file=sys.stderr)
            return []

    def listVpnGateway(self, **args):
        """
        axl.listVpnGateway parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVpnGateway(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnGateway`: ", str(err), file=sys.stderr)
            return []

    def updateVpnGroupReq(self, **args):
        """
        axl.updateVpnGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateVpnGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateVpnGroupReq`: ", str(err), file=sys.stderr)
            return []

    def getVpnGroup(self, **args):
        """
        axl.getVpnGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVpnGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnGroup`: ", str(err), file=sys.stderr)
            return []

    def listVpnGroup(self, **args):
        """
        axl.listVpnGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVpnGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnGroup`: ", str(err), file=sys.stderr)
            return []

    def getVpnProfile(self, **args):
        """
        axl.getVpnProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVpnProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVpnProfile`: ", str(err), file=sys.stderr)
            return []

    def listVpnProfile(self, **args):
        """
        axl.listVpnProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVpnProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVpnProfile`: ", str(err), file=sys.stderr)
            return []

    def getImeServer(self, **args):
        """
        axl.getImeServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeServer`: ", str(err), file=sys.stderr)
            return []

    def listImeServer(self, **args):
        """
        axl.listImeServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeServer`: ", str(err), file=sys.stderr)
            return []

    def getImeRouteFilterGroup(self, **args):
        """
        axl.getImeRouteFilterGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeRouteFilterGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeRouteFilterGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeRouteFilterGroup(self, **args):
        """
        axl.listImeRouteFilterGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeRouteFilterGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeRouteFilterGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeRouteFilterElement(self, **args):
        """
        axl.getImeRouteFilterElement parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeRouteFilterElement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeRouteFilterElement`: ", str(err), file=sys.stderr)
            return []

    def listImeRouteFilterElement(self, **args):
        """
        axl.listImeRouteFilterElement parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeRouteFilterElement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeRouteFilterElement`: ", str(err), file=sys.stderr)
            return []

    def getImeClient(self, **args):
        """
        axl.getImeClient parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeClient(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeClient`: ", str(err), file=sys.stderr)
            return []

    def listImeClient(self, **args):
        """
        axl.listImeClient parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeClient(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeClient`: ", str(err), file=sys.stderr)
            return []

    def getImeEnrolledPattern(self, **args):
        """
        axl.getImeEnrolledPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeEnrolledPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeEnrolledPattern`: ", str(err), file=sys.stderr)
            return []

    def listImeEnrolledPattern(self, **args):
        """
        axl.listImeEnrolledPattern parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeEnrolledPattern(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeEnrolledPattern`: ", str(err), file=sys.stderr)
            return []

    def getImeEnrolledPatternGroup(self, **args):
        """
        axl.getImeEnrolledPatternGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeEnrolledPatternGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeEnrolledPatternGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeEnrolledPatternGroup(self, **args):
        """
        axl.listImeEnrolledPatternGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeEnrolledPatternGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeEnrolledPatternGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeExclusionNumber(self, **args):
        """
        axl.getImeExclusionNumber parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeExclusionNumber(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeExclusionNumber`: ", str(err), file=sys.stderr)
            return []

    def listImeExclusionNumber(self, **args):
        """
        axl.listImeExclusionNumber parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeExclusionNumber(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeExclusionNumber`: ", str(err), file=sys.stderr)
            return []

    def getImeExclusionNumberGroup(self, **args):
        """
        axl.getImeExclusionNumberGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeExclusionNumberGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeExclusionNumberGroup`: ", str(err), file=sys.stderr)
            return []

    def listImeExclusionNumberGroup(self, **args):
        """
        axl.listImeExclusionNumberGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeExclusionNumberGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeExclusionNumberGroup`: ", str(err), file=sys.stderr)
            return []

    def getImeFirewall(self, **args):
        """
        axl.getImeFirewall parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeFirewall(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeFirewall`: ", str(err), file=sys.stderr)
            return []

    def listImeFirewall(self, **args):
        """
        axl.listImeFirewall parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeFirewall(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeFirewall`: ", str(err), file=sys.stderr)
            return []

    def getImeE164Transformation(self, **args):
        """
        axl.getImeE164Transformation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeE164Transformation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeE164Transformation`: ", str(err), file=sys.stderr)
            return []

    def listImeE164Transformation(self, **args):
        """
        axl.listImeE164Transformation parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImeE164Transformation(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImeE164Transformation`: ", str(err), file=sys.stderr)
            return []

    def getTransformationProfile(self, **args):
        """
        axl.getTransformationProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTransformationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTransformationProfile`: ", str(err), file=sys.stderr)
            return []

    def listTransformationProfile(self, **args):
        """
        axl.listTransformationProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTransformationProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTransformationProfile`: ", str(err), file=sys.stderr)
            return []

    def getFallbackProfile(self, **args):
        """
        axl.getFallbackProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFallbackProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFallbackProfile`: ", str(err), file=sys.stderr)
            return []

    def listFallbackProfile(self, **args):
        """
        axl.listFallbackProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listFallbackProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFallbackProfile`: ", str(err), file=sys.stderr)
            return []

    def getLdapFilter(self, **args):
        """
        axl.getLdapFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapFilter`: ", str(err), file=sys.stderr)
            return []

    def listLdapFilter(self, **args):
        """
        axl.listLdapFilter parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLdapFilter(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapFilter`: ", str(err), file=sys.stderr)
            return []

    def getTvsCertificate(self, **args):
        """
        axl.getTvsCertificate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getTvsCertificate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getTvsCertificate`: ", str(err), file=sys.stderr)
            return []

    def listTvsCertificate(self, **args):
        """
        axl.listTvsCertificate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listTvsCertificate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listTvsCertificate`: ", str(err), file=sys.stderr)
            return []

    def updateFeatureControlPolicyReq(self, **args):
        """
        axl.updateFeatureControlPolicyReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateFeatureControlPolicyReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateFeatureControlPolicyReq`: ", str(err), file=sys.stderr)
            return []

    def getFeatureControlPolicy(self, **args):
        """
        axl.getFeatureControlPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFeatureControlPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFeatureControlPolicy`: ", str(err), file=sys.stderr)
            return []

    def listFeatureControlPolicy(self, **args):
        """
        axl.listFeatureControlPolicy parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listFeatureControlPolicy(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFeatureControlPolicy`: ", str(err), file=sys.stderr)
            return []

    def getMobilityProfile(self, **args):
        """
        axl.getMobilityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMobilityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobilityProfile`: ", str(err), file=sys.stderr)
            return []

    def listMobilityProfile(self, **args):
        """
        axl.listMobilityProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMobilityProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMobilityProfile`: ", str(err), file=sys.stderr)
            return []

    def getEnterpriseFeatureAccessConfiguration(self, **args):
        """
        axl.getEnterpriseFeatureAccessConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getEnterpriseFeatureAccessConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEnterpriseFeatureAccessConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listEnterpriseFeatureAccessConfiguration(self, **args):
        """
        axl.listEnterpriseFeatureAccessConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listEnterpriseFeatureAccessConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listEnterpriseFeatureAccessConfiguration`: ", str(err), file=sys.stderr)
            return []

    def getHandoffConfiguration(self, **args):
        """
        axl.getHandoffConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getHandoffConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHandoffConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listCalledPartyTracing(self, **args):
        """
        axl.listCalledPartyTracing parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCalledPartyTracing(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCalledPartyTracing`: ", str(err), file=sys.stderr)
            return []

    def getSIPNormalizationScript(self, **args):
        """
        axl.getSIPNormalizationScript parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSIPNormalizationScript(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSIPNormalizationScript`: ", str(err), file=sys.stderr)
            return []

    def listSIPNormalizationScript(self, **args):
        """
        axl.listSIPNormalizationScript parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSIPNormalizationScript(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSIPNormalizationScript`: ", str(err), file=sys.stderr)
            return []

    def getCustomUserField(self, **args):
        """
        axl.getCustomUserField parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCustomUserField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCustomUserField`: ", str(err), file=sys.stderr)
            return []

    def listCustomUserField(self, **args):
        """
        axl.listCustomUserField parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCustomUserField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCustomUserField`: ", str(err), file=sys.stderr)
            return []

    def getGatewaySccpEndpoints(self, **args):
        """
        axl.getGatewaySccpEndpoints parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getGatewaySccpEndpoints(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getGatewaySccpEndpoints`: ", str(err), file=sys.stderr)
            return []

    def listBillingServer(self, **args):
        """
        axl.listBillingServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listBillingServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listBillingServer`: ", str(err), file=sys.stderr)
            return []

    def getLbmGroup(self, **args):
        """
        axl.getLbmGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLbmGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLbmGroup`: ", str(err), file=sys.stderr)
            return []

    def listLbmGroup(self, **args):
        """
        axl.listLbmGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLbmGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLbmGroup`: ", str(err), file=sys.stderr)
            return []

    def getAnnouncement(self, **args):
        """
        axl.getAnnouncement parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAnnouncement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAnnouncement`: ", str(err), file=sys.stderr)
            return []

    def listAnnouncement(self, **args):
        """
        axl.listAnnouncement parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAnnouncement(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAnnouncement`: ", str(err), file=sys.stderr)
            return []

    def updateServiceProfileReq(self, **args):
        """
        axl.updateServiceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateServiceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateServiceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def updateServiceProfileReq(self, **args):
        """
        axl.updateServiceProfileReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateServiceProfileReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateServiceProfileReq`: ", str(err), file=sys.stderr)
            return []

    def getServiceProfile(self, **args):
        """
        axl.getServiceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getServiceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def listServiceProfile(self, **args):
        """
        axl.listServiceProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listServiceProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listServiceProfile`: ", str(err), file=sys.stderr)
            return []

    def getLdapSyncCustomField(self, **args):
        """
        axl.getLdapSyncCustomField parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapSyncCustomField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSyncCustomField`: ", str(err), file=sys.stderr)
            return []

    def updateAudioCodecPreferenceListReq(self, **args):
        """
        axl.updateAudioCodecPreferenceListReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateAudioCodecPreferenceListReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateAudioCodecPreferenceListReq`: ", str(err), file=sys.stderr)
            return []

    def getAudioCodecPreferenceList(self, **args):
        """
        axl.getAudioCodecPreferenceList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAudioCodecPreferenceList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAudioCodecPreferenceList`: ", str(err), file=sys.stderr)
            return []

    def listAudioCodecPreferenceList(self, **args):
        """
        axl.listAudioCodecPreferenceList parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAudioCodecPreferenceList(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAudioCodecPreferenceList`: ", str(err), file=sys.stderr)
            return []

    def getUcService(self, **args):
        """
        axl.getUcService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUcService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUcService`: ", str(err), file=sys.stderr)
            return []

    def listUcService(self, **args):
        """
        axl.listUcService parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUcService(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUcService`: ", str(err), file=sys.stderr)
            return []

    def getLbmHubGroup(self, **args):
        """
        axl.getLbmHubGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLbmHubGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLbmHubGroup`: ", str(err), file=sys.stderr)
            return []

    def listLbmHubGroup(self, **args):
        """
        axl.listLbmHubGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLbmHubGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLbmHubGroup`: ", str(err), file=sys.stderr)
            return []

    def getImportedDirectoryUriCatalogs(self, **args):
        """
        axl.getImportedDirectoryUriCatalogs parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImportedDirectoryUriCatalogs(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImportedDirectoryUriCatalogs`: ", str(err), file=sys.stderr)
            return []

    def listImportedDirectoryUriCatalogs(self, **args):
        """
        axl.listImportedDirectoryUriCatalogs parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listImportedDirectoryUriCatalogs(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listImportedDirectoryUriCatalogs`: ", str(err), file=sys.stderr)
            return []

    def getVohServer(self, **args):
        """
        axl.getVohServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getVohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getVohServer`: ", str(err), file=sys.stderr)
            return []

    def listVohServer(self, **args):
        """
        axl.listVohServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listVohServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listVohServer`: ", str(err), file=sys.stderr)
            return []

    def getSdpTransparencyProfile(self, **args):
        """
        axl.getSdpTransparencyProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSdpTransparencyProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSdpTransparencyProfile`: ", str(err), file=sys.stderr)
            return []

    def listSdpTransparencyProfile(self, **args):
        """
        axl.listSdpTransparencyProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listSdpTransparencyProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listSdpTransparencyProfile`: ", str(err), file=sys.stderr)
            return []

    def getFeatureGroupTemplate(self, **args):
        """
        axl.getFeatureGroupTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFeatureGroupTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFeatureGroupTemplate`: ", str(err), file=sys.stderr)
            return []

    def listFeatureGroupTemplate(self, **args):
        """
        axl.listFeatureGroupTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listFeatureGroupTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listFeatureGroupTemplate`: ", str(err), file=sys.stderr)
            return []

    def updateDirNumberAliasLookupandSyncReq(self, **args):
        """
        axl.updateDirNumberAliasLookupandSyncReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateDirNumberAliasLookupandSyncReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateDirNumberAliasLookupandSyncReq`: ", str(err), file=sys.stderr)
            return []

    def getDirNumberAliasLookupandSync(self, **args):
        """
        axl.getDirNumberAliasLookupandSync parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDirNumberAliasLookupandSync(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDirNumberAliasLookupandSync`: ", str(err), file=sys.stderr)
            return []

    def listDirNumberAliasLookupandSync(self, **args):
        """
        axl.listDirNumberAliasLookupandSync parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDirNumberAliasLookupandSync(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDirNumberAliasLookupandSync`: ", str(err), file=sys.stderr)
            return []

    def getLocalRouteGroup(self, **args):
        """
        axl.getLocalRouteGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLocalRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLocalRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def listLocalRouteGroup(self, **args):
        """
        axl.listLocalRouteGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLocalRouteGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLocalRouteGroup`: ", str(err), file=sys.stderr)
            return []

    def getAdvertisedPatterns(self, **args):
        """
        axl.getAdvertisedPatterns parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAdvertisedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAdvertisedPatterns`: ", str(err), file=sys.stderr)
            return []

    def listAdvertisedPatterns(self, **args):
        """
        axl.listAdvertisedPatterns parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAdvertisedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAdvertisedPatterns`: ", str(err), file=sys.stderr)
            return []

    def getBlockedLearnedPatterns(self, **args):
        """
        axl.getBlockedLearnedPatterns parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getBlockedLearnedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getBlockedLearnedPatterns`: ", str(err), file=sys.stderr)
            return []

    def listBlockedLearnedPatterns(self, **args):
        """
        axl.listBlockedLearnedPatterns parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listBlockedLearnedPatterns(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listBlockedLearnedPatterns`: ", str(err), file=sys.stderr)
            return []

    def getCCAProfiles(self, **args):
        """
        axl.getCCAProfiles parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCCAProfiles(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCCAProfiles`: ", str(err), file=sys.stderr)
            return []

    def listCCAProfiles(self, **args):
        """
        axl.listCCAProfiles parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCCAProfiles(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCCAProfiles`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalDeviceTemplateReq(self, **args):
        """
        axl.updateUniversalDeviceTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalDeviceTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalDeviceTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def getUniversalDeviceTemplate(self, **args):
        """
        axl.getUniversalDeviceTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUniversalDeviceTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUniversalDeviceTemplate`: ", str(err), file=sys.stderr)
            return []

    def listUniversalDeviceTemplate(self, **args):
        """
        axl.listUniversalDeviceTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUniversalDeviceTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUniversalDeviceTemplate`: ", str(err), file=sys.stderr)
            return []

    def getUserProfileProvision(self, **args):
        """
        axl.getUserProfileProvision parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUserProfileProvision(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUserProfileProvision`: ", str(err), file=sys.stderr)
            return []

    def listUserProfileProvision(self, **args):
        """
        axl.listUserProfileProvision parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUserProfileProvision(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUserProfileProvision`: ", str(err), file=sys.stderr)
            return []

    def getPresenceRedundancyGroup(self, **args):
        """
        axl.getPresenceRedundancyGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPresenceRedundancyGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPresenceRedundancyGroup`: ", str(err), file=sys.stderr)
            return []

    def listPresenceRedundancyGroup(self, **args):
        """
        axl.listPresenceRedundancyGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPresenceRedundancyGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPresenceRedundancyGroup`: ", str(err), file=sys.stderr)
            return []

    def listAssignedPresenceServers(self, **args):
        """
        axl.listAssignedPresenceServers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAssignedPresenceServers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAssignedPresenceServers`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedPresenceServers(self, **args):
        """
        axl.listUnassignedPresenceServers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUnassignedPresenceServers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedPresenceServers`: ", str(err), file=sys.stderr)
            return []

    def listAssignedPresenceUsers(self, **args):
        """
        axl.listAssignedPresenceUsers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listAssignedPresenceUsers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listAssignedPresenceUsers`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedPresenceUsers(self, **args):
        """
        axl.listUnassignedPresenceUsers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUnassignedPresenceUsers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedPresenceUsers`: ", str(err), file=sys.stderr)
            return []

    def getWifiHotspot(self, **args):
        """
        axl.getWifiHotspot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getWifiHotspot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWifiHotspot`: ", str(err), file=sys.stderr)
            return []

    def listWifiHotspot(self, **args):
        """
        axl.listWifiHotspot parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listWifiHotspot(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWifiHotspot`: ", str(err), file=sys.stderr)
            return []

    def getWlanProfileGroup(self, **args):
        """
        axl.getWlanProfileGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getWlanProfileGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWlanProfileGroup`: ", str(err), file=sys.stderr)
            return []

    def listWlanProfileGroup(self, **args):
        """
        axl.listWlanProfileGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listWlanProfileGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWlanProfileGroup`: ", str(err), file=sys.stderr)
            return []

    def getWLANProfile(self, **args):
        """
        axl.getWLANProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getWLANProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWLANProfile`: ", str(err), file=sys.stderr)
            return []

    def listWLANProfile(self, **args):
        """
        axl.listWLANProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listWLANProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWLANProfile`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalLineTemplateReq(self, **args):
        """
        axl.updateUniversalLineTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalLineTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalLineTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalLineTemplateReq(self, **args):
        """
        axl.updateUniversalLineTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalLineTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalLineTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalLineTemplateReq(self, **args):
        """
        axl.updateUniversalLineTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalLineTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalLineTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def updateUniversalLineTemplateReq(self, **args):
        """
        axl.updateUniversalLineTemplateReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateUniversalLineTemplateReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateUniversalLineTemplateReq`: ", str(err), file=sys.stderr)
            return []

    def getUniversalLineTemplate(self, **args):
        """
        axl.getUniversalLineTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getUniversalLineTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getUniversalLineTemplate`: ", str(err), file=sys.stderr)
            return []

    def listUniversalLineTemplate(self, **args):
        """
        axl.listUniversalLineTemplate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUniversalLineTemplate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUniversalLineTemplate`: ", str(err), file=sys.stderr)
            return []

    def getNetworkAccessProfile(self, **args):
        """
        axl.getNetworkAccessProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getNetworkAccessProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getNetworkAccessProfile`: ", str(err), file=sys.stderr)
            return []

    def listNetworkAccessProfile(self, **args):
        """
        axl.listNetworkAccessProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listNetworkAccessProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listNetworkAccessProfile`: ", str(err), file=sys.stderr)
            return []

    def getLicensedUser(self, **args):
        """
        axl.getLicensedUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLicensedUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLicensedUser`: ", str(err), file=sys.stderr)
            return []

    def listLicensedUser(self, **args):
        """
        axl.listLicensedUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLicensedUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLicensedUser`: ", str(err), file=sys.stderr)
            return []

    def getHttpProfile(self, **args):
        """
        axl.getHttpProfile parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getHttpProfile(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getHttpProfile`: ", str(err), file=sys.stderr)
            return []

    def getElinGroup(self, **args):
        """
        axl.getElinGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getElinGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getElinGroup`: ", str(err), file=sys.stderr)
            return []

    def listElinGroup(self, **args):
        """
        axl.listElinGroup parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listElinGroup(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listElinGroup`: ", str(err), file=sys.stderr)
            return []

    def getSecureConfig(self, **args):
        """
        axl.getSecureConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSecureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSecureConfig`: ", str(err), file=sys.stderr)
            return []

    def listUnassignedDevice(self, **args):
        """
        axl.listUnassignedDevice parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listUnassignedDevice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listUnassignedDevice`: ", str(err), file=sys.stderr)
            return []

    def getRegistrationDynamic(self, **args):
        """
        axl.getRegistrationDynamic parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getRegistrationDynamic(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getRegistrationDynamic`: ", str(err), file=sys.stderr)
            return []

    def listRegistrationDynamic(self, **args):
        """
        axl.listRegistrationDynamic parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listRegistrationDynamic(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listRegistrationDynamic`: ", str(err), file=sys.stderr)
            return []

    def getInfrastructureDevice(self, **args):
        """
        axl.getInfrastructureDevice parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getInfrastructureDevice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getInfrastructureDevice`: ", str(err), file=sys.stderr)
            return []

    def listInfrastructureDevice(self, **args):
        """
        axl.listInfrastructureDevice parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listInfrastructureDevice(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listInfrastructureDevice`: ", str(err), file=sys.stderr)
            return []

    def getLdapSearch(self, **args):
        """
        axl.getLdapSearch parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapSearch(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSearch`: ", str(err), file=sys.stderr)
            return []

    def listLdapSearch(self, **args):
        """
        axl.listLdapSearch parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLdapSearch(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapSearch`: ", str(err), file=sys.stderr)
            return []

    def getWirelessAccessPointControllers(self, **args):
        """
        axl.getWirelessAccessPointControllers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getWirelessAccessPointControllers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getWirelessAccessPointControllers`: ", str(err), file=sys.stderr)
            return []

    def listWirelessAccessPointControllers(self, **args):
        """
        axl.listWirelessAccessPointControllers parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listWirelessAccessPointControllers(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listWirelessAccessPointControllers`: ", str(err), file=sys.stderr)
            return []

    def listPhoneActivationCode(self, **args):
        """
        axl.listPhoneActivationCode parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listPhoneActivationCode(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listPhoneActivationCode`: ", str(err), file=sys.stderr)
            return []

    def getDeviceDefaults(self, **args):
        """
        axl.getDeviceDefaults parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getDeviceDefaults(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getDeviceDefaults`: ", str(err), file=sys.stderr)
            return []

    def listDeviceDefaults(self, **args):
        """
        axl.listDeviceDefaults parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listDeviceDefaults(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listDeviceDefaults`: ", str(err), file=sys.stderr)
            return []

    def getMraServiceDomain(self, **args):
        """
        axl.getMraServiceDomain parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMraServiceDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMraServiceDomain`: ", str(err), file=sys.stderr)
            return []

    def listMraServiceDomain(self, **args):
        """
        axl.listMraServiceDomain parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listMraServiceDomain(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listMraServiceDomain`: ", str(err), file=sys.stderr)
            return []

    def listCiscoCloudOnboarding(self, **args):
        """
        axl.listCiscoCloudOnboarding parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listCiscoCloudOnboarding(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listCiscoCloudOnboarding`: ", str(err), file=sys.stderr)
            return []

    def executeSQLQuery(self, **args):
        """
        axl.executeSQLQuery parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.executeSQLQuery(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLQuery`: ", str(err), file=sys.stderr)
            return []

    def executeSQLQueryInactive(self, **args):
        """
        axl.executeSQLQueryInactive parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.executeSQLQueryInactive(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLQueryInactive`: ", str(err), file=sys.stderr)
            return []

    def executeSQLUpdate(self, **args):
        """
        axl.executeSQLUpdate parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.executeSQLUpdate(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `executeSQLUpdate`: ", str(err), file=sys.stderr)
            return []

    def doAuthenticateUser(self, **args):
        """
        axl.doAuthenticateUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `doAuthenticateUser`: ", str(err), file=sys.stderr)
            return []

    def doAuthenticateUser(self, **args):
        """
        axl.doAuthenticateUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `doAuthenticateUser`: ", str(err), file=sys.stderr)
            return []

    def doAuthenticateUser(self, **args):
        """
        axl.doAuthenticateUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `doAuthenticateUser`: ", str(err), file=sys.stderr)
            return []

    def doAuthenticateUser(self, **args):
        """
        axl.doAuthenticateUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `doAuthenticateUser`: ", str(err), file=sys.stderr)
            return []

    def getOSVersion(self, **args):
        """
        axl.getOSVersion parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getOSVersion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getOSVersion`: ", str(err), file=sys.stderr)
            return []

    def getMobility(self, **args):
        """
        axl.getMobility parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getMobility(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getMobility`: ", str(err), file=sys.stderr)
            return []

    def getEnterprisePhoneConfig(self, **args):
        """
        axl.getEnterprisePhoneConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getEnterprisePhoneConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getEnterprisePhoneConfig`: ", str(err), file=sys.stderr)
            return []

    def getLdapSystem(self, **args):
        """
        axl.getLdapSystem parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapSystem(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapSystem`: ", str(err), file=sys.stderr)
            return []

    def getLdapAuthentication(self, **args):
        """
        axl.getLdapAuthentication parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getLdapAuthentication(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getLdapAuthentication`: ", str(err), file=sys.stderr)
            return []

    def getCCMVersion(self, **args):
        """
        axl.getCCMVersion parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCCMVersion(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCCMVersion`: ", str(err), file=sys.stderr)
            return []

    def getFallbackFeatureConfig(self, **args):
        """
        axl.getFallbackFeatureConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getFallbackFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getFallbackFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getImeLearnedRoutes(self, **args):
        """
        axl.getImeLearnedRoutes parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeLearnedRoutes(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeLearnedRoutes`: ", str(err), file=sys.stderr)
            return []

    def getImeFeatureConfig(self, **args):
        """
        axl.getImeFeatureConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getImeFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getImeFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def getAppServerInfo(self, **args):
        """
        axl.getAppServerInfo parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getAppServerInfo(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getAppServerInfo`: ", str(err), file=sys.stderr)
            return []

    def getSoftKeySet(self, **args):
        """
        axl.getSoftKeySet parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSoftKeySet(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSoftKeySet`: ", str(err), file=sys.stderr)
            return []

    def updateSyslogConfigurationReq(self, **args):
        """
        axl.updateSyslogConfigurationReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateSyslogConfigurationReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateSyslogConfigurationReq`: ", str(err), file=sys.stderr)
            return []

    def getSyslogConfiguration(self, **args):
        """
        axl.getSyslogConfiguration parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSyslogConfiguration(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSyslogConfiguration`: ", str(err), file=sys.stderr)
            return []

    def listLdapSyncCustomField(self, **args):
        """
        axl.listLdapSyncCustomField parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listLdapSyncCustomField(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listLdapSyncCustomField`: ", str(err), file=sys.stderr)
            return []

    def getIlsConfig(self, **args):
        """
        axl.getIlsConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getIlsConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getIlsConfig`: ", str(err), file=sys.stderr)
            return []

    def getSNMPCommunityString(self, **args):
        """
        axl.getSNMPCommunityString parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSNMPCommunityString(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPCommunityString`: ", str(err), file=sys.stderr)
            return []

    def getSNMPUser(self, **args):
        """
        axl.getSNMPUser parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSNMPUser(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPUser`: ", str(err), file=sys.stderr)
            return []

    def getSNMPMIB2List(self, **args):
        """
        axl.getSNMPMIB2List parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSNMPMIB2List(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSNMPMIB2List`: ", str(err), file=sys.stderr)
            return []

    def getBillingServer(self, **args):
        """
        axl.getBillingServer parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getBillingServer(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getBillingServer`: ", str(err), file=sys.stderr)
            return []

    def getCcdFeatureConfig(self, **args):
        """
        axl.getCcdFeatureConfig parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCcdFeatureConfig(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCcdFeatureConfig`: ", str(err), file=sys.stderr)
            return []

    def updateLocalRouteGroupReq(self, **args):
        """
        axl.updateLocalRouteGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocalRouteGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocalRouteGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updateLocalRouteGroupReq(self, **args):
        """
        axl.updateLocalRouteGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocalRouteGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocalRouteGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updateLocalRouteGroupReq(self, **args):
        """
        axl.updateLocalRouteGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocalRouteGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocalRouteGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updateLocalRouteGroupReq(self, **args):
        """
        axl.updateLocalRouteGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocalRouteGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocalRouteGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updateLocalRouteGroupReq(self, **args):
        """
        axl.updateLocalRouteGroupReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updateLocalRouteGroupReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updateLocalRouteGroupReq`: ", str(err), file=sys.stderr)
            return []

    def updatePageLayoutPreferencesReq(self, **args):
        """
        axl.updatePageLayoutPreferencesReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.updatePageLayoutPreferencesReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `updatePageLayoutPreferencesReq`: ", str(err), file=sys.stderr)
            return []

    def getPageLayoutPreferences(self, **args):
        """
        axl.getPageLayoutPreferences parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getPageLayoutPreferences(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getPageLayoutPreferences`: ", str(err), file=sys.stderr)
            return []

    def getCredentialPolicyDefault(self, **args):
        """
        axl.getCredentialPolicyDefault parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getCredentialPolicyDefault(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getCredentialPolicyDefault`: ", str(err), file=sys.stderr)
            return []

    def listChangeReq(self, **args):
        """
        axl.listChangeReq parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listChangeReq(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listChangeReq`: ", str(err), file=sys.stderr)
            return []

    def listChange(self, **args):
        """
        axl.listChange parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.listChange(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `listChange`: ", str(err), file=sys.stderr)
            return []

    def getSmartLicenseStatus(self, **args):
        """
        axl.getSmartLicenseStatus parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSmartLicenseStatus(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSmartLicenseStatus`: ", str(err), file=sys.stderr)
            return []

    def getSmartLicenseStatus(self, **args):
        """
        axl.getSmartLicenseStatus parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSmartLicenseStatus(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSmartLicenseStatus`: ", str(err), file=sys.stderr)
            return []

    def getSmartLicenseStatus(self, **args):
        """
        axl.getSmartLicenseStatus parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSmartLicenseStatus(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSmartLicenseStatus`: ", str(err), file=sys.stderr)
            return []

    def getSmartLicenseStatus(self, **args):
        """
        axl.getSmartLicenseStatus parameters
        :param name: name
        :param uuid: uuid 
        :return: result list
        """
        try:
            resp = self.client.getSmartLicenseStatus(**args)
            if resp['return']:
                soap_result = self.elements_to_dict(serialize_object(resp['return'], dict))
                
                while isinstance(soap_result, dict) and len(soap_result) == 1:
                    soap_result = soap_result[list(soap_result.keys())[0]]
                    
                if soap_result is None:
                    return []
                elif isinstance(soap_result, dict):
                    return [soap_result]
                elif isinstance(soap_result, list):
                    return soap_result
                else:
                    return [soap_result]
            return [True]

        except Exception as err:
            print(f"AXL error `getSmartLicenseStatus`: ", str(err), file=sys.stderr)
            return []
