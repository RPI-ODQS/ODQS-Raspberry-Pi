from pub import *
import asyncio
packet = {'buildingId' : '1', 'commmandId' : '1', 'actionTime' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'actionStatus' : 1}

asyncio.get_event_loop().run_until_complete(pub_comRes(packet, self.server_addr, self.port_num, self.buildingId))