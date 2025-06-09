import socket
import threading
import json
from DB.AuthDB import AuthDB
from DB.ChatsDB import ChatDB
from datetime import datetime

DB_FILE = "../Data/db.db"
auth_db = AuthDB(DB_FILE)
chat_db = ChatDB(DB_FILE)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

clients = []

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                request = json.loads(data.decode())
                response = process_request(request)
            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON format."}

            conn.sendall((json.dumps(response) + "\n").encode())

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected {addr}")


def process_request(req):
    action = req.get("action")

    if action == "register":
        try:
            auth_db.add_user(req["nick"], req["name"], req["surname"], req["password"], 0)
            return {"status": "success", "message": "User registered"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif action == "login":
        token = auth_db.verify_user(req["nick"], req["password"])
        if token:
            return {"status": "success", "token": token}
        return {"status": "error", "message": "Invalid credentials"}

    elif action == "create_chat":
        nick = auth_db.get_user_by_token(req["token"])
        if not nick:
            return {"status": "error", "message": "Invalid token"}
        chat_json = chat_db.ensure_chat_exists(req["chat_name"], user_nick=nick)
        return json.loads(chat_json)

    elif action == "send_msg":
        nick = auth_db.get_user_by_token(req["token"])
        if not nick:
            return {"status": "error", "message": "Invalid token"}
        chat_db.send_msg(req["chat_uuid"], nick, req["message"], datetime.now().isoformat())
        return {"status": "success", "message": "Message sent"}

    elif action == "get_msgs":
        messages = chat_db.get_msg(req["chat_uuid"])
        return {"status": "success", "messages": json.loads(messages)}

    elif action == "user_data":
        nick = auth_db.get_user_by_token(req["token"])
        if not nick:
            return {"status": "error", "message": "Invalid token"}
        data = auth_db.get_user_data(nick)
        return {"status": "success", "data": json.loads(data)}

    elif action == "list_chats":
        token = req["token"]
        nick = auth_db.get_user_by_token(token)
        if not nick:
            return json.dumps({"status": "error", "message": "Invalid token"})
        chats_json = chat_db.get_saved_and_accessible_chats(nick)
        return {"status": "success", "chats": json.loads(chats_json)}

    elif action == "update_chat":
        nick = auth_db.get_user_by_token(req["token"])
        if not nick:
            return {"status": "error", "message": "Invalid token"}

        chat_uuid = req["chat_uuid"]
        new_name = req["new_name"]
        user_level = auth_db.get_user_level(nick)

        if chat_db.is_chat_owner(chat_uuid, nick) or user_level >= 1:
            success = chat_db.update_chat_name(chat_uuid, new_name)
            if success:
                return {"status": "success", "message": "Chat name updated"}
            else:
                return {"status": "error", "message": "Update failed"}
        else:
            return {"status": "error", "message": "Permission denied"}

    elif action == "delete_chat":
        nick = auth_db.get_user_by_token(req["token"])
        if not nick:
            return {"status": "error", "message": "Invalid token"}

        chat_uuid = req["chat_uuid"]
        user_level = auth_db.get_user_level(nick)

        if chat_db.is_chat_owner(chat_uuid, nick) or user_level >= 1:
            success = chat_db.delete_chat(chat_uuid)
            if success:
                return {"status": "success", "message": "Chat deleted"}
            else:
                return {"status": "error", "message": "Delete failed"}
        else:
            return {"status": "error", "message": "Permission denied"}

    elif action == "active_users":
        x=threading.active_count()-1
        y=auth_db.user_count()
        print(y)
        return {"status": "success", "active": x,"all":y}


    else:
        return {"status": "error", "message": "Unknown action"}


def start_server():
    print(f"[SERVER] Starting server at {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("[SERVER] Server is listening...")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    start_server()
