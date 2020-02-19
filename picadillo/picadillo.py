import asyncio
import logging


logger = logging.getLogger(__name__)

class Picadillo():
    def __init__(self):
        self.updated = False
        self.width = 255
        self.height = 255
        self.canvas = [
            [255 for _ in range(self.width)]
            for __ in range(self.height)
        ]
        self.clients = list()

    def _current_state(self):
        state = list()
        for x in range(self.width):
            for y in range(self.height):
                if self.canvas[x][y] == 0:
                    state.append({'x': x, 'y': y, 'colour': 0})
        return state

    async def add_client(self, ws):
        self.clients.append(ws)
        for state in self._current_state():
            await ws.send_json(state)

    async def remove_client(self, ws):
        self.clients.remove(ws)
    
    async def process_input(self, input):
        logger.debug('process_input %s', input)
        position = input['x'] + int(input['y']) * self.width
        logger.debug('position = %s', position)
        x = input['x']
        y = int(input['y'])
        self.canvas[x][y] = input['colour']
        self.updated = False
        for client in self.clients:
            await client.send_json(input)
    


