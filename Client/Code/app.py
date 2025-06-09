import tkinter as tk
from tkinter import Frame, Button, Label, LEFT, X
from Settings import SCREENSIZE, RESIZEX, RESIZEY
from pages import chat_page as cp, account_page as ap
from pages.Admin import admin_page as adp
from User import *

from pages.Login.login_page import LoginPage as lp

class Main:
    def __init__(self):
        self.server = ChatClient()
        self.root = tk.Tk()
        self.root.title("PYchan")
        self.root.geometry(SCREENSIZE)
        self.root.resizable(RESIZEX, RESIZEY)
        self.logindata = None
        self.permission_level = 0

        self.setup_styles()
        self.show_login()
        self.root.mainloop()

    def setup_styles(self):
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.accent_color = "#8e45f5"
        self.button_color = "#2f2f4f"
        self.entry_bg = "#3c3c5c"
        self.root.configure(bg=self.bg_color)

    def show_login(self):

        self.login_page = lp(
            self.root,
            self.server,
            on_login_success=self.on_login_success,
            bg_color=self.bg_color,
            fg_color=self.fg_color,
            accent_color=self.accent_color,
        )

    def on_login_success(self, logindata):
        self.logindata = logindata
        self.permission_level = int(self.logindata["Rank"])
        self.login_page = None
        self.show_menu()

    def show_menu(self):
        devclear(self.root)
        self.menu_frame = Frame(self.root, bg=self.accent_color)

        def make_button(text, command, color=None):
            return Button(self.menu_frame, text=text, command=command,
                          bg=color or self.button_color, fg="white",
                          font=("Segoe UI", 10), relief="flat")

        buttons = [
            make_button("Account", self.accout_page),
            make_button("Chats", self.chat_page),
        ]

        if self.permission_level >= 1:
            buttons.append(make_button("Admin", self.admin_page))

        buttons.append(make_button("Exit", self.root.destroy, "#FF3B3B"))

        for btn in buttons:
            btn.pack(side=LEFT, padx=10, pady=10, ipadx=10, ipady=5)

        self.menu_frame.pack(fill=X)

    def chat_page(self):
        self.show_menu()
        self.chat_page_instance = cp.ChatPage(self.root, self.server)

    def accout_page(self):
        self.show_menu()
        self.account_page_instance = ap.AccountPage(self.root, self.server)

    def admin_page(self):
        self.show_menu()
        self.admin_page_nstance= adp.AdminPage(self.root,self.server)


def devclear(root):
    for widget in root.winfo_children():
        widget.destroy()


if __name__ == "__main__":
    app = Main()
