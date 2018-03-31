import paho  # Ensures paho is in PYTHONPATH
import paho.mqtt.publish as publish

import logging
import asyncio
import json

#publish command response
@asyncio.coroutine
def pub_comRes(temp, address, portnum, building_id):

    try:
        temp = str(temp)
        publish.single('/comRes/'+building_id, temp, hostname=address, port = portnum)
    except:

#publish data
@asyncio.coroutine
def pub_data(temp, address, portnum):

    try:
        temp = str(temp)
        publish.single('/data', temp, hostname=address, port = portnum)
    except:

#publish picture
@asyncio.coroutine
def pub_init(temp, address, portnum):

    try:
        temp = str(temp)
        publish.single('/init', temp, hostname = address, port = portnum)
    except:

#publish picture
@asyncio.coroutine
def pub_picture(temp, address, portnum):
    try:
        temp = str(temp)
        publish.single('/picture', temp, hostname = address, port = portnum)
    except:
