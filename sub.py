import logging
import asyncio
import json
import time

from hbmqtt.client import MQTTClient, ClientException
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
}

@asyncio.coroutine
def get_data():
    C = MQTTClient(config = config)
    yield from C.connect('mqtt://192.168.199.118:1883')
    yield from C.subscribe([
        ('/com', QOS_1),
    ])
    logger.info("Subscribed")
    try:
        while(True):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            # 这个data就是你接受到的内容
            data = packet.payload.data

    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(get_data())
