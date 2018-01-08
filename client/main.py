#!/usr/bin/python3
import time
import connection
import client
import effects
import entity
import gamefield
import window

frame = window.Window()
frame.gamefield = gamefield.GameField()
#frame.gamefield.load({'bg': 1, 'players': []})
if __name__ == '__main__':
    connection.client = client.WSClient(frame.gamefield, "ws://10.42.0.233:8000")
    time.sleep(1)
    chara = entity.Player()
    frame.gamefield.players.add(chara)
    frame.gamefield.target = chara
    connection.auth(chara.load)
    #connection.client.auth('admin', '1234')

# if __name__ == '__main__':
#    auth()

if __name__ == '__main__':

    chara.id = 1
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
        pass
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
