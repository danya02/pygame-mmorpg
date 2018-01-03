""" WSClient"""


import websocket
import json
import gzip
import threading
import time


class WSClient(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self, target=self.run)
        self.url = url
        self.ws_connection = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_open=lambda x: print('Start'),
            on_close=self.on_close
        )
        self.ws_connection.keep_running = True

    def send(self, data):
        self.ws_connection.send(gzip.compress(data.encode('utf-8')), 2)

    def on_message(self, _, data):
        pass

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def run(self):
        self.ws_connection.run_forever()


ws = WSClient('ws://localhost:8000')
ws.start()
time.sleep(0.5)
t = time.time()
for _ in range(1000):
    ws.send('{"type": "ping", "data": ""}')
print(time.time() - t)
