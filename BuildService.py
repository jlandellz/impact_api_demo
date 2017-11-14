'''
Created on 13 Nov 2017

@author: jlandells
'''

import sys
import os

import json
from ZenAPIConnector import ZenAPIConnector, ZenDeviceUidFinder, ZenDeviceUuidFinder

def ServiceOrganizerExists(dynamicOrganiserName):
    
    foundDynamicOrganiser = False
    
    router = 'ImpactRouter'
    method = 'getServiceOrganizers'
    data = { "data": "" }
    
    api = ZenAPIConnector(router, method, data)
    response = api.send()
    
    result = response.json()["result"]
    serviceOrgsList = result["serviceOrgs"]
    
    for servOrg in serviceOrgsList:
        if servOrg["name"] == dynamicOrganiserName:
            foundDynamicOrganiser = True
            break
        
    return foundDynamicOrganiser


def CreateDynamicOrganizer(dynamicOrganizerName):
    
    router = 'ImpactRouter'
    method = 'addOrganizer'
    data = { "contextUid": "", "id": dynamicOrganizerName }
    
    api = ZenAPIConnector(router, method, data)
    _response = api.send()
    
    return


def ServiceExists(dynamicOrganizerURI, serviceName):

    foundService = False
    
    router = 'ImpactRouter'
    method = 'getTree'
    data = { "id": dynamicOrganizerURI }
    
    api = ZenAPIConnector(router, method, data)
    response = api.send()
    
    result = response.json()["result"]
    serviceList = result[0]["children"]
    
    for service in serviceList:
        if service["text"]["text"] == serviceName:
            foundService = True
            break
        
    return foundService
  
def CreateService(dynamicOrganizerURI, serviceName):
    
    router = "ImpactRouter"
    method = "addNode"
    data = { "contextUid": dynamicOrganizerURI, "id": serviceName }
    
    api = ZenAPIConnector(router, method, data) 
    _response = api.send()
    
    return 


def GetComponentUID(deviceName, componentName):

    componentUID = None
    
    dev = ZenDeviceUidFinder(name=deviceName)
    devUID = dev.getFirstUid()
    
    router = 'DeviceRouter'
    method = 'getComponents'
    data = { "uid": devUID, "keys": ["name"], "name": componentName }
    
    api = ZenAPIConnector(router, method, data)
    response = api.send()
    
    result = response.json()["result"]
    
    if result["success"]:
        componentUID = result["data"][0]["uid"]
    
    return componentUID
    

def AddComponentsToService(serviceURI, componentList):
    
    router = "ImpactRouter"
    method = 'addToDynamicService'
    
    data = { "targetUid": serviceURI, "uids": componentList }
        
    api = ZenAPIConnector(router, method, data)
    _response = api.send()
        
    return

data = json.loads(sys.argv[1])

dynamicOrganizer = data["dynamicOrganiser"]
doList = dynamicOrganizer.split('/')
dynamicOrganizerName = doList[-1]
dynamicOrganizerURI = "/zport/dmd/DynamicServices" + dynamicOrganizer
serviceName = data["dynamicService"]
serviceURI = dynamicOrganizerURI + "/services/" + serviceName
components = data["components"]

if not ServiceOrganizerExists(dynamicOrganizer):
    print "INFO: Creating Dynamic Organizer"
    CreateDynamicOrganizer(dynamicOrganizerName)
else:
    print "INFO: Dynamic Organizer already exists"
    
if not ServiceExists(dynamicOrganizerURI, serviceName):
    print "INFO: Creating Service"
    CreateService(dynamicOrganizerURI, serviceName)
else:
    print "INFO: Service already exists"
    
componentUIDs = []

for component in components:
    componentUID = GetComponentUID(component["device"], component["component"])
    if componentUID:
        componentUIDs.append(componentUID)

print "INFO: Adding components to Service"

AddComponentsToService(serviceURI, componentUIDs)

print "INFO: Complete!"

sys.exit(0)
    
    
