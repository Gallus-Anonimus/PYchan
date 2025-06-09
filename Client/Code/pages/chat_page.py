import tkinter as tk
from tkinter import Frame, Label, Button, scrolledtext, ttk
import threading

BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#8e45f5"
BUTTON_COLOR = "#2f2f4f"
ENTRY_BG = "#3c3c5c"


class ChatPage:
    def __init__(self, root, server):
        self.root = root
        self.server = server
        self.page = Frame(self.root, bg=BG_COLOR)

        Label(self.page, text="Chat Room", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 16)).pack(pady=10)


        select_frame = Frame(self.page, bg=BG_COLOR)
        select_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        Label(select_frame, text="Select Chat:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.chat_selector = ttk.Combobox(select_frame, state="readonly", width=50)
        self.chat_selector.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        Button(select_frame, text="Load Selected", command=self.load_selected_chat,
               bg="#f5a145", fg="white").pack(side=tk.LEFT)

        Button(select_frame, text="Refresh List", command=self.refresh_chat_list,
               bg="#8ef545", fg="black").pack(side=tk.LEFT, padx=(5, 0))


        create_frame = Frame(self.page, bg=BG_COLOR)
        create_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        Label(create_frame, text="New Chat Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.new_chat_entry = tk.Entry(create_frame, bg=ENTRY_BG, fg="white", font=("Segoe UI", 10))
        self.new_chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), ipady=3)

        Button(create_frame, text="Create Chat", command=self.create_chat,
               bg="#45f58e", fg="black").pack(side=tk.LEFT)


        uuid_frame = Frame(self.page, bg=BG_COLOR)
        uuid_frame.pack(fill=tk.X, padx=20)

        uuid_label = Label(uuid_frame, text="Chat UUID:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 10))
        uuid_label.pack(side=tk.LEFT)

        self.uuid_entry = tk.Entry(uuid_frame, bg=ENTRY_BG, fg="white", font=("Segoe UI", 10))
        self.uuid_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), ipady=3)

        Button(uuid_frame, text="Load", command=self.load_chat_by_uuid, bg="#45c2f5", fg="white").pack(side=tk.LEFT)


        self.chat_box = scrolledtext.ScrolledText(self.page, wrap=tk.WORD, bg=ENTRY_BG, fg="white",
                                                  font=("Consolas", 11), width=60, height=20)
        self.chat_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.chat_box.configure(state='disabled')


        entry_frame = Frame(self.page, bg=BG_COLOR)
        entry_frame.pack(fill=tk.X, padx=20, pady=5)

        self.placeholder = "Type your message..."
        self.entry = tk.Entry(entry_frame, fg="gray", bg=ENTRY_BG, font=("Segoe UI", 10))
        self.entry.insert(0, self.placeholder)

        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.bind("<Return>", self.insert_msg)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=4)

        Button(entry_frame, text="Send", command=self.insert_msg, bg=ACCENT_COLOR, fg="white").pack(side=tk.LEFT)

        self.page.pack(fill=tk.BOTH, expand=True)
        self.refresh_chat_list()

    def append_to_chat(self, sender, message):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, f"{sender}: {message}\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.see(tk.END)

    def clear_chat(self):
        self.chat_box.configure(state='normal')
        self.chat_box.delete("1.0", tk.END)
        self.chat_box.configure(state='disabled')

    def insert_from_json(self):
        self.clear_chat()
        json_data = self.server.get_msgs()
        if json_data.get("status") != "success":
            self.append_to_chat("System", f"Error loading messages: {json_data.get('message', 'Unknown error')}")
            return
        for message in json_data.get("messages", []):
            sender = message.get("sender", "Deleted User")
            msg = message.get("message", "")
            self.append_to_chat(sender, msg)

    def load_chat_by_uuid(self):
        chat_id = self.uuid_entry.get().strip()
        if chat_id:
            try:
                self.server.select_chat(chat_id)
                self.insert_from_json()
                t=threading.Thread(target=self.insert_from_json())
                t.daemon=False

            except Exception as e:
                self.append_to_chat("System", f"Error loading chat: {e}")

    def load_selected_chat(self):
        selection = self.chat_selector.get()
        if selection:
            try:
                uuid_start = selection.rfind('(')
                uuid_end = selection.rfind(')')
                chat_uuid = selection[uuid_start + 1:uuid_end]
                self.server.select_chat(chat_uuid)
                self.insert_from_json()
            except Exception as e:
                self.append_to_chat("System", f"Error loading selected chat: {e}")

    def refresh_chat_list(self):
        try:
            response = self.server.list_chats()
            if response.get("status") != "success":
                self.append_to_chat("System", "Failed to get chat list")
                return

            chats = response.get("chats", [])
            items = [f"{chat['name']} ({chat['uuid']})" for chat in chats]

            self.chat_selector["values"] = items
            if items:
                self.chat_selector.current(0)
            else:
                self.chat_selector.set('')

        except Exception as e:
            self.append_to_chat("System", f"Error refreshing chat list: {e}")

    def create_chat(self):
        chat_name = self.new_chat_entry.get().strip()
        if not chat_name:
            self.append_to_chat("System", "Chat name cannot be empty")
            return

        resp = self.server.create_chat(chat_name)
        if resp.get("status") == "created":
            self.append_to_chat("System", f"Chat '{chat_name}' created!")
            self.new_chat_entry.delete(0, tk.END)
            self.refresh_chat_list()

            new_uuid = resp.get("uuid")
            if new_uuid:
                self.server.select_chat(new_uuid)
                self.insert_from_json()
                for i, val in enumerate(self.chat_selector["values"]):
                    if val.endswith(f"({new_uuid})"):
                        self.chat_selector.current(i)
                        break
        else:
            self.append_to_chat("System", f"Failed to create chat: {resp.get('message', 'Unknown error')}")

    def on_entry_click(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg="white")

    def on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray")

    def insert_msg(self, event=None):
        msg = self.entry.get().strip()
        if msg and msg != self.placeholder:
            resp = self.server.send_msg(msg)
            if resp.get("status") == "success":
                self.append_to_chat(self.server.nick or "You", msg)
                self.entry.delete(0, tk.END)
            else:
                self.append_to_chat("System", f"Failed to send message: {resp.get('message', 'Unknown error')}")

