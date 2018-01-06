#!/usr/bin/python3
from tkinter import *
import tkinter.messagebox as tm
import main


class LoginFrame(Frame):
    def __init__(self, master):
        """
        Basic Tkinter frame for login and password entry.
        :param master: root of this frame.
        """
        super().__init__(master)
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command = self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self) -> None:
        """
        On clik of button.
        """
        username = self.entry_1.get()
        password = self.entry_2.get()
        client = main.client
        try:
            cookie = client.auth(username, password)['session']
        except PermissionError:
            tm.showerror('Try again!', 'The login and/or password was incorrect. Please retry.')
        else:
            with open('.cookie', 'w') as o:
                o.write(cookie)


if __name__ == '__main__':
    root = Tk()
    lf = LoginFrame(root)
    try:
        root.mainloop()
    except SystemExit as e:
        print("FOO!", e)
    print("QUITTED!")