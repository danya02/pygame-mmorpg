#!/usr/bin/python3
import os
import tkinter

import client as module_client
import entity
import gamefield
import login
import window


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
client = module_client.WSClient(frame.gamefield)
if __name__ == '__main__':
    auth()

if __name__ == '__main__':


    chara = entity.Player()
    chara.id = 'CHARA'
    chara.standalone = True
    chara.transmit = True
    frame.on_keypress = chara.on_keypress
    frame.on_keyrelease = chara.on_keyrelease
    frame.gamefield.players.add(chara)
    frame.start()
    while 1:
        pass
    while 1:
        n = 200
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': 200, 'y': n}], 'players': [], 'entities': []})
            n += 5
            time.sleep(1 / 30)
        n = 200
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': n, 'y': 350}], 'players': [], 'entities': []})
            n += 5
            time.sleep(1 / 30)
        n = 350
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': 350, 'y': n}], 'players': [], 'entities': []})
            n -= 5
            time.sleep(1 / 30)
        n = 350
        for i in range(30):
            frame.gamefield.update({'npcs': [{'id': 'Dummy1', 'x': n, 'y': 200}], 'players': [], 'entities': []})
            n -= 5
            time.sleep(1 / 30)
