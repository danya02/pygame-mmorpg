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
            on_open=self.on_open,
            on_close=self.on_close
        )
        self.ws_connection.keep_running = True
        

    def on_message(self, _, data):
        pass

    def on_open(self, _):
        print('Start')

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def run(self):
        self.ws_connection.run_forever()

ws = WSClient('ws://localhost:8000')
ws.start()
time.sleep(0.5)
t = time.time()
for _ in range(1000):
	ws.ws_connection.send('{"type": "ping", "data": ""}')
print(time.time() - t)
