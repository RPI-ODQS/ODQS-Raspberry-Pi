#!/usr/bin/python

#from ubidots import ApiClient
from pub import *
import re
import csv
import sys
import json
import random
import os
import datetime

class DataStore:
	
    def __init__(self, server_address, portnum, buildingID, fileName, token, temperatureNames, pressureNames, waterFlowName, currentName, switchNames, outPutNames):
        
        self.server_address = server_address
        self.portnum = portnum
        self.buildingID = buildingID
        self.fileName = fileName
        self.token = token
        
        self.temperatureNames = temperatureNames[:]
        self.pressureNames = pressureNames[:]
        self.waterFlowName = waterFlowName[:]
        self.currentName = currentName[:]
        self.switchNames = switchNames[:]
        self.outPutNames = outPutNames[:]
        
        #Create an "API" object
        #self.api = ApiClient(token=self.token)
        #Write file header
        display_name_row = ['Display name']
        dataID_row = ['Data ID']
        unit_row = ['Unit']
        display_name_row.extend(self.temperatureNames)
        display_name_row.extend(self.pressureNames)
        display_name_row.extend(self.waterFlowName)
        display_name_row.extend(self.currentName)
        display_name_row.extend(self.switchNames)
        display_name_row.extend(self.outPutNames)
        
        for i in range(len(self.temperatureNames)) :
            dataID_row.append("Temperature " + str(i+1))
            unit_row.append("DegF")
        for i in range(len(self.pressureNames)) :
            dataID_row.append("Pressure " + str(i+1))
            unit_row.append("PSI")
        for i in range(len(self.waterFlowName)) :
            dataID_row.append("Flow " + str(i+1))
            unit_row.append("GPM")
        for i in range(len(self.currentName)) :
            dataID_row.append("Current " + str(i+1))
            unit_row.append("Amp")
        for i in range(len(self.switchNames)) :
            dataID_row.append("Switch " + str(i+1))
            unit_row.append("No unit")
        for i in range(len(self.outPutNames)) :
            dataID_row.append("Output " + str(i+1))
            unit_row.append("Undefined")
        
        #write SOS property
        try:
            f = open('./SOS_data/data_property.csv','w')
            writer = csv.writer(f)
            writer.writerows([display_name_row, dataID_row, unit_row])
            print ('Write property succeed: SOS_data/data_property.csv')
            f.close()
        except IOError:
            print ("Could not write to file: SOS_data/data_property.csv")
        finally:
            f.close()
        
        if os.path.exists('./SOS_data/'+self.fileName):
            return #data file exists
        
        try:
            f = open('./SOS_data/'+self.fileName,'w')
            writer = csv.writer(f)
            writer.writerow(dataID_row)
            print ('Write new file succeed: SOS_data/' + self.fileName)
            f.close()
        except IOError:
            print ("Could not write to file:" + self.fileName)
        finally:
            f.close()

    def setToken(self, token):
        self.token = token
        self.api = ApiClient(token=self.token)
		
    def setTempNames(self, tempVarList):
        self.temperatureNames = tempVarList[:]
	
    def setPressureNames(self, presVarList):
        self.pressureNames = presVarList[:]
		
    def setCurrentNames(self, curVarList):
        self.currentName = curVarList[:]
		
    def setFlowRateNames(self, flowRateVarList):
        self.waterFlowName = flowRateVarList[:]
        
    def newDataFile(self):
        
        if os.path.exists('./SOS_data/'+self.fileName):
            print ("File: \"./SOS_data/" + self.fileName + "\" existed")
            return #data file exist
    
        dataID_row = ['Data ID']
        for i in range(len(self.temperatureNames)) :
            dataID_row.append("Temperature " + str(i+1))
        for i in range(len(self.pressureNames)) :
            dataID_row.append("Pressure " + str(i+1))
        for i in range(len(self.waterFlowName)) :
            dataID_row.append("Flow " + str(i+1))
        for i in range(len(self.currentName)) :
            dataID_row.append("Current " + str(i+1))
        for i in range(len(self.switchNames)) :
            dataID_row.append("Switch " + str(i+1))
        for i in range(len(self.outPutNames)) :
            dataID_row.append("Output " + str(i+1))
        
        try:
            f = open('./SOS_data/'+self.fileName,'w')
            writer = csv.writer(f)
            writer.writerow(dataID_row)
            print ('Write new file succeed: SOS_data/' + self.fileName)
            f.close()
        except IOError:
            print ("Could not write to file:" + self.fileName)
        finally:
            f.close()
	
    def saveAllData(self, temperature, pressure, flowRate, current, switch, output):
        
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #produce data to send and to write
        write_data = [time_stamp]
        #transfer data into json
        #packet = {'Building ID' : self.buildingID, 'Time Stamp' : time_stamp, 'Data' : data}
        data = {}
        write_data = [time_stamp]
        for i in range(len(temperature)):
            if temperature[i]:
                data['temperature '+ str(i+1)] = temperature[i]
            write_data.append(temperature[i])
        for i in range(len(pressure)):
            if pressure[i]:
                data['pressure '+ str(i+1)] = pressure[i]
            write_data.append(pressure[i])
        for i in range(len(flowRate)):
            if flowRate[i]:
                data['waterflow '+ str(i+1)] = flowRate[i]
            write_data.append(flowRate[i])
        for i in range(len(current)):
            if current[i]:
                data['current '+ str(i+1)] = current[i]
            write_data.append(current[i])
        for i in range(len(switch)):
            if switch[i]:
                data['switch ' + str(i+1)] = switch[i]
            write_data.append(True)
        for i in range(len(output)):
            if output[i]:
                data['output ' + str(i+1)] = output[i]
            write_data.append(output[i])
        packet = {'buildingId' : self.buildingID, 'timeStamp' : time_stamp, 'data' : data}
##        json_dic = json.dumps(packet, sort_keys = True, indent = 4, separators = (',',':'), ensure_ascii = True)
##        print (json_dic)
        
        #send data to server
        try:
            asyncio.get_event_loop().run_until_complete(pub_data(packet, self.server_address, self.portnum))
            print("Data sended")

        except Error:
    
            print ("Could not connet to server:" + self.server_address + ":" + str(self.portnum))
        #new date, new file
        if datetime.datetime.now().strftime("%Y-%m-%d")+".csv" != self.fileName:
            self.fileName = datetime.datetime.now().strftime("%Y-%m-%d")+".csv"
            self.newDataFile()
            
        #add record
        try:
                f = open('./SOS_data/'+self.fileName,'a')
                writer = csv.writer(f)
                writer.writerow(write_data)
                print ('Write succeed' + self.fileName)
        except IOError:
                print ("Could not write to file:" + self.fileName)
        finally:
                f.close()
		
def setNames(data_id_list, displayname_list):
    
    #open configuration data file
    with open('./Configuration_data/Config_data.txt','r') as f:
        lines = f.readlines()
    
    parameters = {}
    for line in lines:
        temp_l = line.replace(' ', '')
        temp_l = temp_l.replace('\n', '')
        str_list = re.split(',|:', temp_l)
        line_name = str_list[0]
        del str_list[0]
        parameters[line_name] = str_list
    
    for i in range(len(data_id_list)):
        temp_data_id = data_id_list[i].split()
        print('Display name of data \"' + data_id_list[i] +'\" changed: ' + parameters[temp_data_id[0]][int(temp_data_id[1])-1] + '-->' +displayname_list[i])
        parameters[temp_data_id[0]][int(temp_data_id[1])-1] = displayname_list[i]
    
    if parameters['buildingid'][0] :
        buildingID = parameters['buildingid'][0]
    else :
        print ("No buildingid in configuration file")
    if parameters['temperature'] :
        tempNames = parameters['temperature']
    else :
        print ("No temperature in configuration file")
    if parameters['pressure']: 
        pressureNames = parameters['pressure']
    else :
        print ("No pressure in configuration file")
    if parameters['flow']:
        waterflowName = parameters['flow']
    else:
        print ("No flow in configuration file")
    if parameters['current'] :
        currentNames = parameters['current']
    else:
        print ("No current in configuration file")
    if parameters['switch']:
        switchNames = parameters['switch']
    else:
        print ("No switch in configuration file")
    if parameters['output']:
        outputNames = parameters['output']
    else:
        print ("No output in configuration file")
     
    
    rows = []
    rows.append('buildingid: '+ buildingID)
    row = 'temperature: '
    for i in range(len(tempNames)):
        row = row + tempNames[i]
        if i < len(tempNames)-1:
            row = row + ', '
    rows.append(row)
    row = 'pressure: '
    for i in range(len(pressureNames)):
        row = row + pressureNames[i]
        if i < len(pressureNames)-1:
            row = row + ', '
    rows.append(row)
    row = 'flow: '
    for i in range(len(waterflowName)):
        row = row + waterflowName[i]
        if i < len(waterflowName)-1:
            row = row + ', '
    rows.append(row)
    row = 'current: '
    for i in range(len(currentNames)):
        row = row + currentNames[i]
        if i < len(currentNames)-1:
            row = row + ', '
    rows.append(row)
    row = 'switch: '
    for i in range(len(switchNames)):
        row = row + switchNames[i]
        if i < len(switchNames)-1:
            row = row + ', '
    rows.append(row)
    row = 'output: '
    for i in range(len(outputNames)):
        row = row + outputNames[i]
        if i < len(outputNames)-1:
            row = row + ', '
    rows.append(row)
    
    display_name_row = ['Display name']
    display_name_row.extend(tempNames)
    display_name_row.extend(pressureNames)
    display_name_row.extend(waterflowName)
    display_name_row.extend(currentNames)
    display_name_row.extend(switchNames)
    display_name_row.extend(outputNames)
	    
    dataID_row = ['Data ID']
    unit_row = ['Unit']
    for i in range(len(tempNames)) :
        dataID_row.append("Temperature " + str(i+1))
        unit_row.append("DegF")
    for i in range(len(pressureNames)) :
        dataID_row.append("Pressure " + str(i+1))
        unit_row.append("PSI")
    for i in range(len(waterflowName)) :
        dataID_row.append("Flow " + str(i+1))
        unit_row.append("GPM")
    for i in range(len(currentNames)) :
        dataID_row.append("Current " + str(i+1))
        unit_row.append("Amp")
    for i in range(len(switchNames)) :
        dataID_row.append("Switch " + str(i+1))
        unit_row.append("No unit")
    for i in range(len(outputNames)) :
        dataID_row.append("Output " + str(i+1))
        unit_row.append("Undefined")
	    
	    
            
    #update Config data
    try:
        file_obj = open('./Configuration_data/Config_data.txt', 'w')
        for i in range(len(rows)):
            file_obj.write(rows[i] + '\n')
        file_obj.close()
        print ("SetName Complete")
    except IOError:
        print ("Could not write to file:/Configuration_data/Config_data.txt")
    finally:
        file_obj.close()
    #update property
    try:
        f = open('./SOS_data/data_property.csv','w')
        writer = csv.writer(f)
        writer.writerows([display_name_row, dataID_row, unit_row])
        print ('Write property succeed: SOS_data/data_property.csv')
        f.close()
    except IOError:
        print ("Could not write to file: SOS_data/data_property.csv")
    finally:
        f.close()