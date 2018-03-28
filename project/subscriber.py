#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.
from ubi import *
from com import *
from opi import *
import paho  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import logging
import asyncio

#read building id, server address and port number from file
with open('./Configuration_data/Config_data.txt','r') as f:
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()

temp_l = line1.replace(' ', '')
temp_l = temp_l.replace('\n', '')
str_list = re.split(',|=', temp_l)
building_id = str_list[1]

temp_l = line2.replace(' ', '')
temp_l = temp_l.replace('\n', '')
str_list = re.split(',|=', temp_l)
server_address = str_list[1]

temp_l = line3.replace(' ', '')
temp_l = temp_l.replace('\n', '')
str_list = re.split(',|=', temp_l)
port_num = int(str_list[1])

#initialize controllers for OPI and COM
opi_controller = OPI_Record()
com_controller = COM_Controller(server_address, port_num, building_id)
logger = logging.getLogger(__name__)

print("--------------------Subscribing--------------------")
print("Server Address: " + server_address + ":" + str(port_num))
print("BuildingId: " + building_id)

#update opi record
def new_opi(data):
    time = data['time']
    opt_type = data['type']
    opt_parameter = []
    opt_parameter.append(data['input1'])
    opt_parameter.append(data['input2'])
    water_demand = data['hotWater']
    elec_price = data['elePrice']
    amb_temp = data['ambTemperature']
    solar_gen = data['solarEnergyOutput']
    demand_res = data['demandResponseScaler']
    opi_controller.new_record(time, opt_type, opt_parameter, water_demand, elec_price, amb_temp, solar_gen, demand_res)

#add command record and execute it
def new_command(data):
    time = data['time']
    com_id = str(data['id'])
    com_type = int(data['type'])
    com_p1 = float(data['parameterVar1'])
    com_p2 = float(data['parameterVar2'])
    com_controller.new_command(time, com_id, com_type, com_p1, com_p2)

#update display names in the input
def update_display_name(input):
    data = json.loads(input)
    data_id_list = data.keys()
    displayname_list = []
    for i in range(len(data_id_list)):
        displayname_list.append(data_id_list[i])
    setNames(data_id_list, displayname_list)

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    mqttc.subscribe('/comReq/' + building_id, 0)
    mqttc.subscribe('/opi/' + building_id, 0)
    mqttc.subscribe('/name/' + building_id, 0)

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    payload = eval(msg.payload)
    if msg.topic == '/comReq/' + building_id:
        new_command(payload)
    elif msg.topic == '/opi/' + building_id:
        new_opi(payload)
    elif msg.topic == '/name/' + building_id:
        update_display_name(payload)
    print("--------------------Subscribing--------------------")
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

##test_com = {'time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'id' : 25, 'type' : 2, 'parameterVar1' : 2.2, 'parameterVar2': 1.2}
##new_command(test_com)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect(server_address, port_num, 60)

mqttc.loop_forever()
