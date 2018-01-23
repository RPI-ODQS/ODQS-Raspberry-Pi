import logging
import asyncio
import json
import time

from ubi import *
from com import *
from opi import *
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

#read building id, server address from file
with open('./Configuration_data/Config_data.txt','r') as f:
    line1 = f.readline()
    line2 = f.readline()
temp_l = line1.replace(' ', '')
temp_l = temp_l.replace('\n', '')
str_list = re.split(',|=', temp_l)

building_id = str_list[1]

temp_l = line2.replace(' ', '')
temp_l = temp_l.replace('\n', '')
str_list = re.split(',|=', temp_l)
server_address = str_list[1]

#initialize controllers for OPI and COM
opi_controller = OPI_Record()
com_controller = COM_Controller()
logger = logging.getLogger(__name__)

config = {
    'keep_alive': 10,
    'ping_delay': 1,
    'default_qos': 0,
    'default_retain': False,
    'auto_reconnect': True,
    'reconnect_max_interval': 5,
    'reconnect_retries': 10
}

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
    com_controller.new_command(server_address, building_id, time, com_id, com_type, com_p1, com_p2)

#update display names in the input
def update_display_name(input):
    data = json.loads(input)
    data_id_list = data.keys()
    displayname_list = []
    for i in range(len(data_id_list)):
        displayname_list.append(data_id_list[i])
    setNames(data_id_list, displayname_list)

@asyncio.coroutine
def get_data():
    C = MQTTClient(config = config)
    yield from C.connect(server_address)
    yield from C.subscribe([
        ('/comReq/'+building_id, QOS_1),
        ('/opi/'+building_id, QOS_1),
        ('/name/'+building_id, QOS_1)
    ])
    logger.info('---Listener is subscribing---')
    try:
        while(True):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            topic = packet.variable_header.topic_name
            # 这个data就是你接受到的内容
            data = packet.payload.data
            data = eval(data)
            print (type(topic))
            print (topic)
            print (type(data))
            print (data)
            
            out = []
            out.append(topic)
            out.append(data)
            
            return out
            
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)
    finally:
        yield from C.disconnect()

if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    
    while(True):
        try:
            logger.info("Connecting:" + server_address)
            data = asyncio.get_event_loop().run_until_complete(get_data())
            if data[0] == '/comReq/' + building_id:
                new_command(data[1])
            elif data[0] == '/opi/' + building_id:
                new_opi(data[1])
            elif data[0] == '/name/' + building_id:
                update_display_name(data[1])
        except Exception as ce:
            logger.error('Exception: %s' % ce)