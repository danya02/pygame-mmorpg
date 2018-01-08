#!/usr/bin/python3
from tkinter import *
import tkinter.messagebox as tm
import connection


class LoginFrame(Frame):
    def __init__(self, master, callback):
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

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()
        self.callback = callback

    def _login_btn_clicked(self) -> None:
        """
        On click of button.
        """
        username = self.entry_1.get()
        password = self.entry_2.get()
        client = connection.client
        client.auth(username, password, self._login_callback)

    def _login_callback(self, result: dict) -> None:
        """
        For when the async login has completed.
        :param result: The returned dict of data.
        """
        if result != 'Wrong login or password':
            self.callback(result)
            raise SystemExit
        else:
            tm.showerror("Wrong credentials!", "The username and/or password given was incorrect. Please try again.")


if __name__ == '__main__':
    root = Tk()
    lf = LoginFrame(root)
    try:
        root.mainloop()
    except SystemExit as e:
        print("FOO!", e)
    print("QUITTED!")
