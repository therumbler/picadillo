import logging

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from picadillo import Picadillo

logger = logging.getLogger(__name__)

def make_app():
    app = FastAPI(__name__)

    with open('static/index.html') as f:
        index_html = f.read()

    picadillo = Picadillo()

    @app.get('/')
    async def index():
        return HTMLResponse(index_html)

    @app.websocket("/ws/")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        logger.info("websocket opened...")


        await picadillo.add_client(ws)
        while True:
            try:
                input = await ws.receive_json()
                await picadillo.process_input(input)
            except WebSocketDisconnect:
                logger.info('WebSocketDisconnect')
                await picadillo.remove_client(ws)
                break
        logger.info('end of websocket_endpoint')



    return app

