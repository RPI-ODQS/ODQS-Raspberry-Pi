import logging
import asyncio
import json

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

logger = logging.getLogger(__name__)

config = {
    'keep_alive': 10,
    'ping_delay': 1,
    'default_qos': 0,
    'default_retain': False,
    'auto_reconnect': True,
    'reconnect_max_interval': 5,
    'reconnect_retries': 10,
    'topics': {
        '/init': { 'qos': 1 },
        '/data': { 'qos': 1 },
        '/picture': { 'qos': 1 },
        '/comRes': { 'qos': 1 },
    }
}

@asyncio.coroutine
def pub_comRes(temp, address, building_id):
    C = MQTTClient(config=config)
    yield from C.connect(address)
    temp = json.dumps(temp)
    temp = str.encode(temp)
    print (temp)
    tasks = [
        asyncio.ensure_future(C.publish('/comRes/'+building_id, temp)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()

@asyncio.coroutine
def pub_data(temp, address):
    C = MQTTClient(config=config)
    yield from C.connect(address)
    temp = json.dumps(temp)
    temp = str.encode(temp)
    tasks = [
        asyncio.ensure_future(C.publish('/data', temp)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()

@asyncio.coroutine
def pub_init(temp, address):
    C = MQTTClient(config=config)
    yield from C.connect(address)
    temp = json.dumps(temp)
    temp = str.encode(temp)
    tasks = [
        asyncio.ensure_future(C.publish('/init', temp)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()
    
@asyncio.coroutine
def pub_picture(temp, address):
    C = MQTTClient(config=config)
    yield from C.connect(address)
    #temp = json.dumps(temp)
    temp = str.encode(temp)
    tasks = [
        asyncio.ensure_future(C.publish('/picture', temp)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()

if __name__ == '__main__':
    temp =  {
        "BuildingId":1,
        "Data":{
            "Current 1":5.1440216394607745,
            "Current 10":5.14088348555882,
            "Current 2":5.289398279252106,
            "Current 3":5.610020451534119,
            "Current 4":5.655938869110828,
            "Current 5":5.5416430050932775,
            "Current 6":5.961722787926706,
            "Current 7":5.138329191630669,
            "Current 8":5.454193804893637,
            "Current 9":5.46792812909779,
            "Flow 1":2.070613097081067,
            "Flow 2":2.1754076279726053,
            "Flow 3":2.1743976060748436,
            "Flow 4":2.4636671889730772,
            "Output 1":57.49238232759026,
            "Output 2":1.9862143869965756,
            "Output 3":45.18929845199536,
            "Output 4":89.99551610022546,
            "Output 5":95.59638676009206,
            "Output 6":26.43479070774834,
            "Output 7":45.98361720122603,
            "Output 8":82.82747801886424,
            "Pressure 1":10.869988959815457,
            "Pressure 2":10.41526529408265,
            "Pressure 3":10.17866531809292,
            "Temperature 1":33.189206972454876,
            "Temperature 2":-3.2310923899230026,
            "Temperature 3":11.931119851036847,
            "Temperature 4":20.550511456957388,
            "Temperature 5":-0.8437674005783169,
            "Temperature 6":35.44979474820467,
            "Temperature 7":18.520460585525278,
            "Temperature 8":28.16953478684097,
            "Temperature 9":-0.34914147841974064
        },
        "TimeStamp":"2017-12-08 17:39:38.972363"
    }
    asyncio.get_event_loop().run_until_complete(test_coro(temp))
    
