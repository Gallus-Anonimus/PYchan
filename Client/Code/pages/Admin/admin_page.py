import tkinter as tk
from tkinter import Frame, Label, Button, LEFT
from Code.pages.Admin.Statisctics import StatsAdminPage


class AdminPage(Frame):
    def __init__(self, parent,server):
        super().__init__(parent,)
        self.parent=parent
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.accent_color = "#8e45f5"
        self.server=server
        self.configure(bg=self.bg_color)
        self.build_ui()
        self.pack()

    def build_ui(self):
        Label(self, text="Admin Panel", bg=self.bg_color, fg=self.fg_color,
              font=("Segoe UI", 16)).pack(pady=20)

        menu = Frame(self, bg=self.bg_color)

        Button(menu, text="Accounts", bg=self.accent_color, fg="white", relief="flat", command=self.ChatsPage,font=("Segoe UI", 10)).pack(side=LEFT, padx=10, pady=5, ipadx=10, ipady=5)
        Button(menu, text="Chats", bg=self.accent_color, fg="white", relief="flat", command=self.AccountsPage,font=("Segoe UI", 10)).pack(side=LEFT, padx=10, pady=5, ipadx=10, ipady=5)
        Button(menu, text="Stats", bg=self.accent_color, fg="white", relief="flat", command=self.StatsPage,font=("Segoe UI", 10)).pack(side=LEFT, padx=10, pady=5, ipadx=10, ipady=5)

        menu.pack()
        self.pageFrame=Frame(self,bg=self.bg_color)
        self.pageFrame.pack()


    def StatsPage(self):
        devclear(self.pageFrame)
        self.Stats_page_intance = StatsAdminPage(self.pageFrame, self.server)

    def AccountsPage(self):
        devclear(self.pageFrame)
        self.Stats_page_intance = StatsAdminPage(self.pageFrame, self.server)

    def ChatsPage(self):
        devclear(self.pageFrame)
        self.Stats_page_intance = StatsAdminPage(self.pageFrame, self.server)



def devclear(root):
    for widget in root.winfo_children():
        widget.destroy()
