import threading
import tkinter as tk
from tkinter import Frame, Label, Button, LEFT

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StatsAdminPage(Frame):
    def __init__(self, parent, server):
        super().__init__(parent, )
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.accent_color = "#8e45f5"
        self.server = server
        self.configure(bg=self.bg_color)
        self.build_ui()
        self.pack()

    def build_ui(self):
        Label(self, text="Stats Panel", bg=self.bg_color, fg=self.fg_color,
              font=("Segoe UI", 16)).pack(pady=20)

        menu = Frame(self, bg=self.bg_color)
        self.activeusers=Label(self,text="Active users:",bg=self.bg_color,fg=self.fg_color,font=("Segoe UI", 16))
        self.activeusers.pack(pady=20)
        menu.pack()
        self.update()


    def update(self):
        data=self.server.active_users()
        print(data)
        if data["status"]=="success":
            self.activeusers.configure(text=f"Active users:{data['active']}")
            fig,ax=plt.subplots()

            ax.pie([data['active'],data['all']-data['active']],labels=["active","all"],autopct="%1.1f%%",startangle=90,)
            ax.axis("equal")

            canvas=FigureCanvasTkAgg(fig,master=self)


            canvas.draw()
            canvas.get_tk_widget().pack()