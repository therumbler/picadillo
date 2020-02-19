import asyncio
import logging


logger = logging.getLogger(__name__)

class Picadillo():
    def __init__(self):
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
    
    async def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.canvas[x][y] = 255
        for client in self.clients:
            await client.send_json({'event': 'clear'})

    async def process_input(self, input):
        logger.debug('process_input %s', input)
        if 'event' in input:
            if input['event'] == 'clear':
                await self.clear()

            return
        x = int(input['x'])
        y = int(input['y'])
        try:
            self.canvas[x][y] = input['colour']
            await self.update_clients(input)
        except IndexError:
            logger.error('position %d, %d is outside of the canvas', x, y)

    async def update_clients(self, state):
        for client in self.clients:
            await client.send_json(state)
    


