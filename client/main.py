#!/usr/bin/python3
import os
import tkinter
import time

import client as module_client
import entity
import gamefield
import login
import window
import effects


class TestClient:
    def auth(self, usr, passwd):
        print(usr, passwd)
        return {'session': 'COOKIE!'}

    def session_auth(self, cookie):
        print(cookie)

    def action(self, action_type=None, action_data=None):
        print(action_type, action_data)

def auth():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        raise PermissionError
        with open('.cookie') as i:
            client.session_auth(i.read())
    except (FileNotFoundError, PermissionError):
        root = tkinter.Tk()
        lf = login.LoginFrame(root)
        try:
            root.mainloop()
        except SystemExit:
            pass

frame = window.Window()
frame.gamefield = gamefield.GameField()
frame.gamefield.load({'bg':1, 'players':[]})
client = TestClient()
#if __name__ == '__main__':
#    auth()

if __name__ == '__main__':
    chara = entity.Player()
    chara.id = 'CHARA'
    chara.standalone = True
    chara.transmit = True
    chara.effects.append(effects.Poison(chara))
    frame.on_keypress = chara.on_keypress
    frame.on_keyrelease = chara.on_keyrelease
    frame.on_click = chara.on_click
    frame.on_unclick = chara.on_unclick
    frame.gamefield.players.add(chara)
    frame.gamefield.target = chara
    frame.start()
    while 1:
        n = -100
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': -100, 'y': n}], 'players': [], 'entities': []})
            n += 5
            time.sleep(1 / 30)
        n = -100
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': n, 'y': 50}], 'players': [], 'entities': []})
            n += 5
            time.sleep(1 / 30)
        n = 50
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': 50, 'y': n}], 'players': [], 'entities': []})
            n -= 5
            time.sleep(1 / 30)
        n = 50
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': n, 'y': -100}], 'players': [], 'entities': []})
            n -= 5
            time.sleep(1 / 30)
