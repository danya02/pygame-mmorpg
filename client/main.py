#!/usr/bin/python3
import pygame
import sys
import math
import time
import tkinter
import os

sys.path.append('.')
import window
import gamefield
import entity
import login


class TestClient:
    def auth(self, usr, passwd):
        print(usr, passwd)
        return 'COOKIE!'

    def session_auth(self, cookie):
        print(cookie)

    def action(self, action_type=None):
        print(action_type)


client = TestClient()


def auth():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open('.cookie') as i:
            client.session_auth(i.read())
    except [FileNotFoundError, PermissionError]:
        root = tkinter.Tk()
        lf = login.LoginFrame(root)
        root.mainloop()


if __name__ == '__main__':
    auth()

    frame = window.Window()
    frame.gamefield = gamefield.GameField()
    client.field = frame.gamefield

    chara = entity.Player()
    chara.id = 'CHARA'
    chara.standalone = True
    chara.transmit = True
    frame.on_keypress = chara.on_keypress
    frame.on_keyrelease = chara.on_keyrelease
    frame.gamefield.players.add(chara)
    frame.start()
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
