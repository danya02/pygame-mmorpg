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
        n=200
        for i in range(30):
            frame.gamefield.update({'players': [{'id': 'FRISK', 'x': 200, 'y': n}],'npcs': [], 'entities': []})
            n+=5
            time.sleep(1/30)
        n=200
        for i in range(30):
            frame.gamefield.update({'players': [{'id': 'FRISK', 'x': n, 'y': 350}],'npcs': [], 'entities': []})
            n+=5
            time.sleep(1 / 30)
        n=350
        for i in range(30):
            frame.gamefield.update({'players': [{'id': 'FRISK', 'x': 350, 'y': n}],'npcs': [], 'entities': []})
            n-=5
            time.sleep(1 / 30)
        n=350
        for i in range(30):
            frame.gamefield.update({'players': [{'id': 'FRISK', 'x': n, 'y': 200}],'npcs': [], 'entities': []})
            n-=5
            time.sleep(1 / 30)
