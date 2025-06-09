import threading
import tkinter as tk
from tkinter import Label, Button, Toplevel
from .login import Login as log

class LoginPage:
    def __init__(self, root, server, on_login_success, bg_color, fg_color, accent_color):
        self.root = root
        self.server = server
        self.on_login_success = on_login_success
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent_color = accent_color

        self.login_screen = None
        self._login_button = None

        self.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = Label(self.root, text="Please log in to continue", bg=self.bg_color, fg=self.fg_color,
                      font=("Segoe UI", 14))
        label.pack(pady=20)

        login_btn = Button(self.root, text="Login", bg=self.accent_color, fg="white", font=("Segoe UI", 12))
        login_btn.pack(pady=10, ipadx=10, ipady=5)

        login_btn.config(command=self.on_login_click)
        self._login_button = login_btn

    def on_login_click(self):
        self._login_button.config(state="disabled")

        login_window = Toplevel(self.root)
        login_window.grab_set()
        self.login_screen = log(self.server)
        self.login_screen.root = login_window
        self.login_screen.LoginScreen()

        threading.Thread(target=self.check_login_status, daemon=True).start()

    def check_login_status(self):
        while not self.login_screen.IsLogged():

            threading.Event().wait(0.1)

        logindata = self.server.user_data()["data"]

        def handle_success():
            if self._login_button:
                self._login_button.destroy()
            self.on_login_success(logindata)

        self.root.after(0, handle_success)