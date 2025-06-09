import socket
import json
import time


class ChatClient:
    def __init__(self, host="192.168.1.10", port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nick=None
        self.token = None
        self.chat_uuid = None
        self.connect()

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print("Connection successful")
        except Exception as e:
            print("Connection failed:", e)

    def send_request(self, request_dict):
        try:
            message = json.dumps(request_dict)
            self.sock.sendall(message.encode())
            response = self.sock.recv(8192).decode()
            return json.loads(response)
        except Exception as e:
            print("Error during request:", e)
            return {"status": "error", "message": str(e)}

    def register(self, nick, name, surname, password):
        req = {
            "action": "register",
            "nick": nick,
            "name": name,
            "surname": surname,
            "password": password
        }
        return self.send_request(req)

    def login(self, nick, password):
        req = {
            "action": "login",
            "nick": nick,
            "password": password
        }
        response = self.send_request(req)
        if response.get("status") == "success":
            self.token = response.get("token")
            self.nick = nick
        return response

    def create_chat(self, chat_name):
        if not self.token:
            return {"status": "error", "message": "Login required"}
        req = {
            "action": "create_chat",
            "token": self.token,
            "chat_name": chat_name
        }
        response = self.send_request(req)
        if response.get("status") == "success":
            self.chat_uuid = response.get("uuid")
        return response

    def send_msg(self, message):
        if not self.token or not self.chat_uuid:
            return {"status": "error", "message": "Login and chat selection required"}
        req = {
            "action": "send_msg",
            "token": self.token,
            "chat_uuid": self.chat_uuid,
            "message": message
        }
        return self.send_request(req)

    def get_msgs(self):
        if not self.chat_uuid:
            return {"status": "error", "message": "No chat selected"}
        req = {
            "action": "get_msgs",
            "chat_uuid": self.chat_uuid
        }
        return self.send_request(req)

    def user_data(self):
        if not self.token:
            return {"status": "error", "message": "Login required"}
        req = {
            "action": "user_data",
            "token": self.token
        }
        return self.send_request(req)

    def list_chats(self):
        if not self.token:
            return {"status": "error", "message": "Login required"}
        req = {
            "action": "list_chats",
            "token": self.token
        }
        return self.send_request(req)

    def active_users(self):
        print("active_users")
        req ={
            "action": "active_users"
        }
        return self.send_request(req)

    def select_chat(self, uuid):
        self.chat_uuid = uuid

    def close(self):
        self.sock.close()


