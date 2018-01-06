""" WSClient"""


import websocket
import gzip
import threading
import json
import time


class WSClient(threading.Thread):
    def __init__(self, field, url='ws://localhost:8000'):
        threading.Thread.__init__(self, target=self.run)
        self.field = field
        self.url = url
        self.ws_connection = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_open=lambda x: print('Start'),
            on_close=self.on_close
        )
        self.ws_connection.keep_running = True

    def send_message(self, data):
        """
        Send message
        :param data: dict
        :return: None
        """
        data = json.dumps(data)
        self.ws_connection.send(gzip.compress(data.encode('utf-8')), 2)

    def on_message(self, _, data):
        data = gzip.decompress(data)
        data = json.loads(data.decode('utf-8'))
        typ = data['type']
        data = data['data']
        if typ == 'tick':
            self.field.update(data)
        else:
            print(typ, data)

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def action(self, action_type, data=''):
        self.send_message({'action': action_type, 'data': data})

    def auth(self, user, password):
        self.send_message({'type': 'auth', 'data': {'user': user, 'password': password}})

    def run(self):
        self.ws_connection.run_forever()
