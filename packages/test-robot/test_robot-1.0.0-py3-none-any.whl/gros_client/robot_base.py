import asyncio
import json
import threading
from typing import Callable, Dict, Any

import requests
import websocket
from websocket import *


class RobotBase:

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
                 on_open: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):

        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close
        self.on_error = on_error

        if ssl:
            self.baseurl = f'https://{host}:{port}'
            self.ws_url = f'wss://{host}:{port}/ws'
        else:
            self.baseurl = f'http://{host}:{port}'
            self.ws_url = f'ws://{host}:{port}/ws'

        self.ws: WebSocket = create_connection(self.ws_url)
        if self.on_open:
            asyncio.run(self.on_open(self.ws))

        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.start()

    def _receive_loop(self):
        while True:
            try:
                message = self.ws.recv()
                if self.on_message:
                    asyncio.run(self.on_message(self.ws, message))
            except websocket.WebSocketConnectionClosedException as e:
                if self.on_close:
                    asyncio.run(self.on_close(self.ws))
            except websocket.WebSocketException as e:
                if self.on_close:
                    asyncio.run(self.on_error(self.ws, e))

    def get_video_status(self) -> Dict[str, Any]:
        response = requests.get(f'{self.baseurl}/control/camera_status')
        return response.json()

    def get_video_stream_url(self) -> str:
        return f'{self.baseurl}/control/camera'

    def exit(self):
        self.ws.close()

    def _send_websocket_msg(self, message: json):
        self.ws.send(json.dumps(message))

    @classmethod
    def _cover_param(cls, param: float, value: str, min_threshold: float, max_threshold: float) -> float:
        if param is None:
            print(f"Illegal parameter: {value} = {param}")
            param = 0
        if param > max_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be greater than {max_threshold}, actual {param}")
            param = max_threshold
        if param < min_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be less than {min_threshold}, actual {param}")
            param = min_threshold
        return param
