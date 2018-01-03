
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import json
import commands
from config import *
import logging
import asyncio
import threading
import traceback
import gzip
from db import Db

lock = threading.Lock()
db = Db(lock)


class Handler(WebSocketServerProtocol):
    def __init__(self):
        WebSocketServerProtocol.__init__(self)
        self.temp = db
        self.user = None
        self.user_id = None
        self.user_stat = {}
        self.game = None
        self.channel = self.temp.main_channel
        self.user_rights = 0
        self.addr = None
        self.typing = False
        self.logger = logging.getLogger('WSServer')

    def ws_send(self, message):
        data = gzip.compress(message.encode('utf-8'), compresslevel=9)
        self.sendMessage(data, isBinary=True)

    def get_information(self):
        return self.temp.get_user_information(self.user)

    def onConnect(self, request):
        self.temp.handlers.append(self)
        self.addr = request.peer[4:]
        self.logger.info('%s Запрос на подключение' % self.addr)

    def onOpen(self):
        self.ws_send(json.dumps({
            'type': 'welcome',
            'data': {
                'message': 'online-games websocket server WELCOME!',
                'version': VERSION
            }
        }))
        self.channel.join(self)

    def onMessage(self, payload, is_binary):
        try:
            message = json.loads(gzip.decompress(payload).decode('utf-8'))
            message_type = message['type']
            data = message['data']
        except:
            message_type = 'error'
            data = 'Error'
        try:
            message_type = message_type.replace('__', '')
            message_type = message_type.lower()
            resp = commands.__getattribute__(message_type)(self, data)
        except Exception as ex:
            resp = {'type': message_type + '_error', 'data': str(ex)}
            self.logger.error('%s Ошибка %s %s %s' % (self.addr, message_type, data, str(ex)))
        self.ws_send(json.dumps(resp))

    def onClose(self, *args):
        try:
            commands.leave(self, None)
            if self.channel:
                self.channel.leave(self)
            self.temp.handlers.remove(self)
            self.logger.info('%s Отключился' % (self.addr,))
        except:
            pass


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def run(secret_key):
    form = '[%(asctime)s]  %(levelname)s: %(message)s'
    logger = logging.getLogger("WSServer")
    logging.basicConfig(level=logging.INFO, format=form)

    log_handler = logging.FileHandler('logs/log.txt')
    log_handler.setFormatter(logging.Formatter(form))

    logger.addHandler(log_handler)
    logger.info('Запуск сервера %s:%s' % (IP, PORT))

    Handler.secret_key = secret_key
    factory = WebSocketServerFactory(u"ws://%s:%s" % (IP, PORT))
    factory.protocol = Handler

    l = asyncio.get_event_loop()
    coro = l.create_server(factory, IP, PORT)
    s = l.run_until_complete(coro)

    thread = Thread(l.run_forever)
    return thread


if __name__ == '__main__':
    sk = 'shouldintermittentvengeancearmagainhisredrighthandtoplagueus'
    run(sk)
    while True:
        try:
            out = eval(input())
            if out is not None:
                print(out)
        except:
            traceback.print_exc()
