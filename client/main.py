#!/usr/bin/python3
import pygame
import sys
import math
import time

sys.path.append('.')
import window
import gamefield
import player

if __name__ == '__main__':
    frame = window.Window()
    frame.gamefield = gamefield.GameField()
    frame.on_keypress = lambda x: print('PRESSED ', x)
    frame.on_keyrelease = lambda x: print('RELEASED', x)
    chara = player.Player()
    chara.id = 'CHARA'
    frame.gamefield.players.add(chara)
    frame.start()
    while 1:
        frame.gamefield.update(
            {'players': [{'id': 'CHARA', 'x': abs(int(math.sin(time.time()) * 400)), 'y': abs(int(math.sin(time.time())*400))}],
             'npcs': [], 'entities': []})
        frame.update()
        time.sleep(0.05)
