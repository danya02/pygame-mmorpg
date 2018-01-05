#!/usr/bin/python3
import pygame
import sys
import math
import time

sys.path.append('.')
import window
import gamefield
import entity

if __name__ == '__main__':
    frame = window.Window()
    frame.gamefield = gamefield.GameField()

    chara = entity.Player()
    chara.id = 'CHARA'
    chara.standalone = True
    frame.on_keypress = chara.on_keypress
    frame.on_keyrelease = chara.on_keyrelease
    frame.gamefield.players.add(chara)
    frame.start()
    while 1:
        frame.gamefield.update(
            {'players': [{'id': 'FRISK', 'x': 400+(int(math.sin(time.time()) * 300)), 'y': 300+(int(math.cos(time.time())*250))}],
             'npcs': [], 'entities': []})
        time.sleep(1/30)
