#!/usr/bin/python
import re
import time
import datetime
import random

#import pigpio
from temperature import *
from water_flow_sensor import *
from switch_motor import *
from pwm_motor import *
from pressure_and_current_sensor import *
from button import *
from ubi import *
from pub import *

print ("******")
#read configuration parameters from file
try:
    
    config_path = './Configuration_data/Config_data.txt'
    
    parameters = {}
    
    file_obj = open(config_path, 'r')
    
    for line in file_obj:
        temp_l = line.replace(' ', '')
        temp_l = temp_l.replace('\n', '')
        str_list = re.split(',|=', temp_l)
        line_name = str_list[0]
        del str_list[0]
        parameters[line_name] = str_list
        
    file_obj.close()
    if parameters['address'][0]:
        server_address = parameters['address'][0]
    else :
        print ('No address in configuration file!')
    if parameters['port'][0]:
        port_num = int(parameters['port'][0])
    else :
        print ('No port number in configuration file!')
    if parameters['timeInterval'][0]:
        time_interval = int(parameters['timeInterval'][0])
    else :
        print ('No timeInterval in configuration file!')
    if parameters['buildingid'][0] :
        buildingID = parameters['buildingid'][0]
    else :
        print ("No buildingid in configuration file!")
    if parameters['temperature'] :
        tempNames = parameters['temperature']
    else :
        print ("No temperature in configuration file!")
    if parameters['pressure']: 
        waterPressureNames = parameters['pressure']
    else :
        print ("No pressure in configuration file!")
    if parameters['flow']:
        flowRateNames = parameters['flow']
    else:
        print ("No flow in configuration file!")
    if parameters['current'] :
        currentNames = parameters['current']
    else:
        print ("No current in configuration file!")
    if parameters['switch']:
        switchNames = parameters['switch']
    else:
        print ("No switch in configuration file!")
    if parameters['output']:
        outputNames = parameters['output']
    else:
        print ("No output in configuration file!")
    
except IOError:
    print ("Could not open file:\'./Configuration_data/Config_data.txt\'")


#send display name and building id to server to make sure the configuration data is the same
data = {'buildingId' : buildingID}
for i in range(len(tempNames)):
    data['temperature '+ str(i+1)] = tempNames[i]
for i in range(len(waterPressureNames)):
    data['pressure '+ str(i+1)] = waterPressureNames[i]
for i in range(len(flowRateNames)):
    data['waterflow '+ str(i+1)] = flowRateNames[i]
for i in range(len(currentNames)):
    data['current '+ str(i+1)] = currentNames[i]
for i in range(len(switchNames)):
    data['switch ' + str(i+1)] = switchNames[i]
for i in range(len(outputNames)):
    data['output ' + str(i+1)] = outputNames[i]


#send json to server
try:

    asyncio.get_event_loop().run_until_complete(pub_init(data, server_address, port_num))
    print("Data sender initiated")

except:
    
    print ("Could not connet to server:" + server_address + ":" + str(port_num))

try:

    '''
    pi = pigpio.pi()
    if not pi.connected:
        print("Pigpio error")
        exit(0)

    #default CE pin is CE0 (GPIO 8), default MOSI, MISO, SCLK are used
    TempSensor = Temperature(pi)
    # default GPIO pin is 23
    WaterSensor1 = WaterFlow(pi)

    WaterSensor2 = WaterFlow(pi, 24)
	

    #default GPIO pins are pinMain = 21, pinControl1 = 20, pinControl2 = 16, pinControl3 = 12, pinControl4 = 25
    SwMotor = SwitchMotor(pi) 
	
    #default GPIO pins are pinMain = 26, pinControl1 = 19, pinControl2 = 13, pinControl3 = 6, pinControl4 = 5
    PwmMotor = PWMMotor(pi) 
	
    #default CE pin is CE0 (GPIO 8), default MOSI, MISO, SCLK are used
    pressure = Pressure(pi)
    current = Current(pi)
    
    btn = Button(pi, 17ctoken = 'NiMi8SLq6aLVX38HTNYYGwHqXxqpmW'
    buildingID = '000001'
    tempNames = ['Hot Water Supply', 'Cold Water Supply', 'Ambient', 'Water Heater Input', 'Water Heater Output','Tank Input', 'Tank Output', 'Outdoor', 'Evaporator Output', 'Pipe Surface 1', 'Pipe Surface 2']
    waterPressureNames = ['Hot Water Supply', 'Cold Water Supply', 'Tank Input']
    flowRateNames = ['Hot water Supply', 'Circulation Flow', 'Water Heater Input', 'Tank Input']
    currentNames = ['Building Consumption', 'Solar Generation', 'Water Heater', 'Air Conditioner', 'Dryer', 'Pool pump', 'Plugin Load 1', 'Plugin Load 2', 'Plugin Load 3', 'PL4']
    switchNames = ['s1', 's1', 's1', 's1', 's1', 's1', 's1', 's1', 's1']
    otputNames = ['OP1', 'OP1', 'OP1', 'OP1', 'OP1', 'OP1', 'OP1', 'OP1']
    '''
    token = []
    date = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    saveData = DataStore(server_address, port_num, buildingID, date, token, tempNames, waterPressureNames, flowRateNames, currentNames, switchNames, outputNames)


    '''
    print "SwMotor"
    SwMotor.startMotor()
    time.sleep(2)
    
    SwMotor.setControlOn(1)
    time.sleep(2)
	
    SwMotor.setControlOff(1)
    time.sleep(2)
	
    SwMotor.stopMotor()
    time.sleep(1)
	
    print "PmwMotor"
    print "Starting"
    PwmMotor.startMotor()
    time.sleep(2)
    print "Started"
	
    PwmMotor.setControlLevel(1, 50)
    time.sleep(2)
	
    PwmMotor.setControlOff(1)
    time.sleep(2)
	
    PwmMotor.stopMotor()
    
    print btn.isDown()
    print btn.isUp()
    '''	
    while True:
        
        #random data for testing
        temp = []
        rand_count = random.randint(1,len(tempNames))
        i = 0
        while i < rand_count:
            temp.append(random.uniform(-5,45))
            print("Temp  from chanel {}: {} deg C".format(i, temp[i]))
            i += 1
        while i < len(tempNames):
            temp.append(None)
            i += 1
        
        pres = []
        for i in range(len(waterPressureNames)):
            pres.append(random.uniform(10,11))
            print("WaterPressure: {} MPa".format(pres[i]))
        
        
        flowRate = []
        for i in range(len(flowRateNames)):
            flowRate.append(random.uniform(2,3))
            print("WaterFlow: {} Litres per Hour".format(flowRate[i]))
        
        cur = []
        for i in range(len(currentNames)):
            cur.append(random.uniform(5,6))
            print("Current: {} A".format(cur[i]))
		
        switch = []
        for i in range(len(switchNames)):
            switch.append(True)
        
        output = []
        for i in range(len(outputNames)):
            output.append(random.uniform(0.5, 100))
        '''
	temp = []
	# Loop sensor channels
	for temp_chanel in range(5):
            ## Read the temp sensor data
	    temp.append(TempSensor.getTemp(temp_chanel))

	    ## Print out results
            print("Temp  from chanel {}: {} deg C".format(temp_chanel, temp[temp_chanel]))    
		
	pres = []
	pres.append(pressure.getPressure(0))
	pres.append(pressure.getPressure(1))
		
	print("WaterPressure: {} MPa".format(pres[0]))    
	print("WaterPressure: {} MPa".format(pres[1]))    
	#print "--------------------------------------------"  

	flowRate = []
	flowRate.append(WaterSensor1.getFlowRate())
	flowRate.append(WaterSensor2.getFlowRate())
	print("WaterFlow: {} Litres per Hour".format(flowRate[0]))
	print("WaterFlow: {} Litres per Hour".format(flowRate[1]))    
		
	cur = []
	cur.append(current.calcIrms(0,1480))
	cur.append(current.calcIrms(1,1480))
	cur.append(current.calcIrms(2,1480))
	cur.append(current.calcIrms(3,1480))
		
	print("Current: {} A".format(cur[0]))    
	print("Current: {} A".format(cur[1]))    
	print("Current: {} A".format(cur[2]))    
	print("Current: {} A".format(cur[3]))    
	print "--------------------------------------------"  
		
	'''	
	
	

        saveData.saveAllData(temp, pres, flowRate, cur, switch, output)
        #wait for some seconds
        print("-----------------Now sleeping for " + str(time_interval) + " seconds-----------------")
        time.sleep(time_interval)

finally: 
    '''
    TempSensor.delete()
	
    WaterSensor1.delete()
    WaterSensor2.delete()
	
    SwMotor.delete();
    PwmMotor.delete();
	
    pressure.delete()
    current.delete()
	
    pi.stop()
    '''
    print ("Goodbye")