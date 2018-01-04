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
            {'players': [{'id': 'CHARA', 'x': 400+(int(math.sin(time.time()) * 300)), 'y': 300+(int(math.cos(time.time())*250))}],
             'npcs': [], 'entities': []})
        frame.update()
