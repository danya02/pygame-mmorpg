#!/usr/bin/python3
import time
import connection
import effects
import entity
import gamefield
import window

frame = window.Window()
frame.gamefield = gamefield.GameField()
frame.gamefield.load({'bg': 1, 'players': []})

# if __name__ == '__main__':
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
