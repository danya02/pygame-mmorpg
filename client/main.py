#!/usr/bin/python3
import pygame
import sys

sys.path.append('.')
import window
import gamefield

if __name__ == '__main__':
    frame = window.Window()
    frame.gamefield = gamefield.GameField()
    frame.on_keypress = lambda x: print('PRESSED ', x)
    frame.on_keypress = lambda x: print('RELEASED', x)
    frame.run()
    while 1:
        pass
