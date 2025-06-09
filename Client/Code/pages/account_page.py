import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk

BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#8e45f5"
ENTRY_BG = "#3c3c5c"


class AccountPage:
    def __init__(self, root, server):
        self.root = root
        self.server = server
        self.page = Frame(self.root, bg=BG_COLOR)

        Label(self.page, text="Account Information", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 16)).pack(pady=15)

        try:
            img = Image.open("../Client/user.jpg")
            img = img.resize((100, 100))
            self.photo = ImageTk.PhotoImage(img)
            self.photo_label = Label(self.page, image=self.photo, bg=BG_COLOR)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.photo_label = Label(self.page, text="No Photo", bg=BG_COLOR, fg="gray")

        self.photo_label.pack(pady=10)
        self.info_frame = Frame(self.page, bg=BG_COLOR)
        self.info_frame.pack(pady=10, padx=20, fill=tk.X)

        # Labels for info (initially empty)
        self.nick_label = Label(self.info_frame, text="Nick: ", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12))
        self.nick_label.pack(anchor="w", pady=5)

        self.name_label = Label(self.info_frame, text="Name: ", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12))
        self.name_label.pack(anchor="w", pady=5)

        self.surname_label = Label(self.info_frame, text="Surname: ", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12))
        self.surname_label.pack(anchor="w", pady=5)

        self.RegisterDate = Label(self.info_frame, text="Register date: ", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12))
        self.RegisterDate.pack(anchor="w", pady=5)

        self.MsgSend = Label(self.info_frame, text="Messages send: ", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12))
        self.MsgSend.pack(anchor="w", pady=5)
        # Refresh button
        self.refresh_btn = Button(self.page, text="Refresh Info", command=self.load_user_data,
                                  bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 11), width=15)
        self.refresh_btn.pack(pady=15)

        self.status_label = Label(self.page, text="", bg=BG_COLOR, fg="yellow", font=("Segoe UI", 10))
        self.status_label.pack()

        self.page.pack(fill=tk.BOTH, expand=True)
        self.load_user_data()

    def load_user_data(self):
        self.status_label.config(text="Loading user info...")
        data = self.server.user_data()
        print(data)
        if data.get("status") == "success":
            user=data["data"]
            self.nick_label.config(text=f"Nick: {user.get('Nick', 'N/A')}")
            self.name_label.config(text=f"Name: {user.get('Name', 'N/A')}")
            self.surname_label.config(text=f"Surname: {user.get('Surname', 'N/A')}")
            self.RegisterDate.config(text=f"Register date: {user.get('RegisterDate', 'N/A')}")
            self.MsgSend.config(text=f"Messages send: {user.get('MsgSend', 'N/A')}")
            self.status_label.config(text="User info loaded successfully.")
        else:
            self.nick_label.config(text="Nick: -")
            self.name_label.config(text="Name: -")
            self.surname_label.config(text="Surname: -")
            self.status_label.config(text=f"Failed to load user info: {data.get('message', 'Unknown error')}", fg="red")
