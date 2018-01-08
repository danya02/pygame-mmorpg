""" WSClient"""


import websocket
import gzip
import threading
import json
import pygame
import uuid


def sync(func):
    def wrapper(self, data, call_back):
        rand = str(uuid.uuid4())
        self.call_backs[rand] = call_back
        return func(self, data, rand)

    return wrapper


class WSClient(threading.Thread):
    def __init__(self, field, url='ws://92.63.105.60:8000'):
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
        self.start()
        self.call_backs = {}

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
        msg = json.loads(data.decode('utf-8'))
        typ = msg['type']
        data = msg['data']
        if msg.get('id'):
            self.call_backs[msg['id']](data)
            self.call_backs.pop(msg['id'])
            return
        if typ == 'auth_ok':
            with open('.cookie', 'w') as o:
                o.write(data['session'])
        elif typ == 'tick':
            self.field.update(data)
        elif typ == 'image':
            s = pygame.image.fromstring(data['src'], data['size'], 'RGBA')
            pygame.image.save(s, 'sprites/' + data['name'])
        else:
            pass

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def action(self, action_type, data=''):
        self.send_message({'action': action_type, 'data': data})

    def auth(self, user, password, call_back):
        rand = str(uuid.uuid4())
        self.call_backs[rand] = call_back
        self.send_message({'type': 'auth', 'data': {'user': user, 'password': password, 'id': rand}})

    def run(self):
        self.ws_connection.run_forever()

    @sync
    def session_auth(self, session, func):
        self.send_message({'type': 'session_auth', 'data': {'session': session}, 'id': func})

    @sync
    def get_image(self, data, func):
        self.send_message({'type': 'get_image', 'data': data, 'id': func})
