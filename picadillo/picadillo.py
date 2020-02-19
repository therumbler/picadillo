import asyncio
import logging


logger = logging.getLogger(__name__)

class Picadillo():
    def __init__(self):
        self.updated = False
        self.width = 255
        self.height = 255
        self.canvas = [255 for _ in range(self.width * self.height)]
        self.clients = list()
        asyncio.create_task(self._interval())

    async def _interval(self):
        while True:
            await self.update_clients()
            await asyncio.sleep(0.5)

    async def add_client(self, ws):
        self.clients.append(ws)
        await ws.send_json(self.canvas)

    async def remove_client(self, ws):
        self.clients.remove(ws)
    async def update_clients(self):
        if self.updated:
            return

        logger.info('sending updates...')
        for client in self.clients:
            await client.send_json(self.canvas)
        self.updated = True

    async def process_input(self, input):
        logger.debug('process_input %s', input)
        position = input['x'] + int(input['y']) * self.width
        logger.debug('position = %s', position)
        self.canvas[position] = input['colour']
        self.updated = False
    


