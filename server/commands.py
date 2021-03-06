

"""Commands"""


import json
import time
import sessions
from config import *


def perms_check(user_rights):
    def decorator(func):
        def wrapper(self, data):
            if self.user_rights >= user_rights:
                return func(self, data)
            else:
                return {'type': 'denied', 'data': 'Not enough rights'}
        return wrapper
    return decorator


def __auth(self, user, session=None, auth_type='auth_ok'):
    """
    :param self: class Handler

    :type user: str
    :param user: user name

    :type session: str, None
    :param session: flask session

    :type auth_type: str
    :param auth_type: type of answer

    :return: {
        'type': auth_type,
        'data': self.get_information(), 'session': str
    }
    """
    self.user = user
    self.user_id = self.temp.users[user]['user_id']
    self.user_rights = self.temp.users[user]['user_rights']
    self.player_info = self.temp.users[user]['player_info']
    for handler in self.temp.handlers:
        hand_user = handler.user
        if (hand_user == self.user) and (handler is not self):
            resp = {'type': 'disconnected', 'data': 'Disconnected!'}
            handler.ws_send(json.dumps(resp))
            handler.onClose()
    resp = {
        'type': auth_type,
        'data': self.get_information()
    }
    if not session:
        session = sessions.encode_flask_cookie(self.secret_key, resp['data'])
    resp['data']['session'] = session
    self.channel.send({
        'type': 'user_logged_in',
        'data': self.get_information()
    })
    self.me = self.game.add_player(self)
    return resp


@perms_check(0)
def auth(self, data):
    """
    :param self: class Handler
    :param data: {
        'user': str
        'password': str
    }

    :raise: You are already logged in
            Wrong login or password

    :return: __auth(self, data['user'])
    """
    if self.user:
        raise Exception('You are already logged in')
    if (data['user'] in self.temp.users) and (self.temp.users[data['user']]['password'] == data['password']):
        return __auth(self, data['user'])
    elif data['user'] not in self.temp.users:
        return reg(self, data)
    raise Exception('Wrong login or password')


@perms_check(0)
def session_auth(self, data):
    """
    :param self: class Handler
    :param data: {
        'session': str (flask session)
    }

    :return: __auth(self, user, data['session'])
    """
    session = sessions.decode_flask_cookie(self.secret_key, data['session'])
    user = session['user']
    return __auth(self, user, data['session'])


@perms_check(0)
def reg(self, data):
    """
    :param self: class Handler
    :param data: {
        'user': str,
        'password: str
    }

    :raise: This login is already in use

    :return: __auth(self, data['user'], auth_type='reg_ok')
    """
    if len(data['user']) < 3:
        raise Exception('Too small name')
    if len(data['password']) == 0:
        raise Exception('Bad password')
    if data['user'] not in self.temp.users:
        user_id = [self.temp.users[i]['user_id'] for i in self.temp.users]
        self.user_id = max(user_id) + 1
        self.temp.users[data["user"]] = {
            'user': data["user"],
            'password': data["password"],
            'user_rights': 1,
            'user_id': self.user_id,
            'player_info': {
                'inventory': [],
                'effects': [],
                'hp': 100,
                'x': 100,
                'y': 100,
                'direction': 0,
                'active_item': None,
            }
        }
        self.temp.db_save(USERS, self.temp.users)
        return __auth(self, data['user'], auth_type='reg_ok')
    raise Exception('This login is already in use')


@perms_check(1)
def start_typing(self, _):
    if self.typing:
        raise Exception('You are already typing')
    self.typing = True
    self.channel.send({'type': 'user_start_typing', 'data': {'user': self.user, 'user_id': self.user_id}})
    return {'type': 'start_typing_ok', 'data': ''}


@perms_check(1)
def stop_typing(self, _):
    if not self.typing:
        raise Exception('You are not typing')
    self.typing = False
    self.channel.send({'type': 'user_stop_typing', 'data': {'user': self.user, 'user_id': self.user_id}})
    return {'type': 'stop_typing_ok', 'data': ''}


@perms_check(0)
def send_message(self, data):
    """
    :param self: class Handler
    :param data: {
        'text': str
    }
    :return: dict
    """
    resp = {
        'type': 'message',
        'data': {
            'name': self.user,
            'rights': self.user_rights,
            'time': time.time(),
            'text': data['text']
        }
    }
    self.channel.send(resp)
    return {'type': 'send_ok', 'data': ''}


def action1(self, action, data):
    resp = self.me.action(action, data)
    return {'type': 'action_%s_ok' % action, 'data': resp}


@perms_check(0)
def get_channel_information(self, _):
    if self.channel:
        users = {}
        user_count = 0
        for handler in self.channel.handlers:
            user_count += 1
            if handler.user:
                users[handler.user] = handler.get_information()
        return {
            'type': 'channel',
            'data': {
                'name': self.channel.name,
                'users_count': user_count,
                'unauthorized_count': user_count - len(self.channel.handlers),
                'users': users
            }
        }
    return {'type': 'channel_information', 'data': ''}


@perms_check(0)
def leave(self, _):
    if (not self.game) or (not self.me):
        return {'type': 'leave_ok', 'data': ''}
    self.game.delete_player(self)
    self.player_info = {
        'inventory': list(map(lambda x: x.id, self.me.inventory)),
        'effects': list(map(lambda x: x.id, self.me.effects)),
        'hp': self.me.hp,
        'x': self.me.rect.x,
        'y': self.me.rect.y,
        'direction': self.me.direction,
        'active_item': self.me.active_item.get_index(self.me.inventory)
        if getattr(self.me, 'active_item', None) else 0,
    }
    self.temp.users[self.user]['player_info'] = self.player_info
    self.me = None
    self.game = None
    self.temp.db_save_all()
    return {'type': 'leave_ok', 'data': ''}


@perms_check(0)
def get_image(self, data):
    return {'type': 'img', 'data': self.game.get_img(data)}


@perms_check(5)
def player_add_effect(self, data):
    for player in self.game.field.players:
        if player.name == data['name']:
            effect = self.game.field.get_object_by_id(data['id'])
            self.game.field.add_effect(effect(self.me, data['ticks']))


@perms_check(0)
def ping(_, data):
    """
    :param _: None
    :param data: send time or None
    :return: dict
    """
    if not data:
        return {'type': 'pong', 'data': 'Pong!'}
    return {'type': 'pong', 'data': time.time() - data}


def error(*_):
    """
    System method
    """
    return {'type': 'error', 'data': 'Bad request'}
