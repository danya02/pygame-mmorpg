""" WSClient"""


import websocket
import gzip
import threading
import json
import client_commands
# import time


class WSClient(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self, target=self.run)
        # self.field = field
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
        # TODO: Debug
        data = gzip.decompress(data)
        data = json.loads(data)
        message_type = data['type']
        data = data['data']
        client_commands.__getattribute__(message_type)(self, data)

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def run(self):
        self.ws_connection.run_forever()


# ws = WSClient('ws://localhost:8000')
# ws.start()
# time.sleep(2)
# t = time.time()
# for _ in range(1000):
#     ws.send_message({"type": "count", "data": ""})
# print('Finish' + str(time.time() - t))
