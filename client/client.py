""" WSClient"""


import websocket
import json
import gzip
import threading


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
        print(gzip.decompress(data))

    def on_open(self, _):
        print('Start')

    def on_close(self, _):
        self.ws_connection.keep_running = False

    def run(self):
        self.ws_connection.run_forever()
