#!/usr/bin/python3
import os
import pygame
import login
import tkinter
import client as module_client

class TestClient:
    def auth(self, usr, passwd):
        print(usr, passwd)
        return {'session': 'COOKIE!'}

    def session_auth(self, cookie):
        print(cookie)

    def action(self, action_type=None, action_data=None):
        print(action_type, action_data)

    def get_image(self, name, callback):
        print(name)
        callback({"name": name, "size": (1, 1), "src": str(pygame.image.tostring(pygame.Surface((1, 1)), "RGBA"))})


def auth(callback):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        raise PermissionError
        with open('.cookie') as i:
            client.session_auth(i.read())
    except (FileNotFoundError, PermissionError):
        root = tkinter.Tk()
        lf = login.LoginFrame(root, callback)
        try:
            root.mainloop()
        except SystemExit:
            pass

