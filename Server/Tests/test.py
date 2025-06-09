import os
import json
from datetime import datetime, timedelta
from ..Code.DB.AuthDB import AuthDB
from ..Code.DB.ChatsDB import ChatDB
from Server.Tests.Colors import Colors


DB_FILE = "../Data/db.db"

if not os.path.exists(DB_FILE):
    print(Colors.RED+"Database file does not exist. Exiting.")
    exit(1)

auth_db = AuthDB(DB_FILE)
chat_db = ChatDB(DB_FILE)

def test_user_creation():
    print(Colors.WHITE+"[TEST] Creating user...")
    try:
        auth_db.add_user("testnick", "Test", "User", "password123",0)
        print(Colors.GREEN+"User created successfully.")
    except Exception as e:
        print(Colors.YELLOW+f"User creation might have failed (already exists?): {e}")

def test_user_authentication():
    print(Colors.WHITE+"[TEST] Authenticating user...")
    token = auth_db.verify_user("testnick", "password123")
    if token:
        print(Colors.GREEN+f"Auth successful, token: {token}")
        return token
    else:
        print(Colors.RED+"Auth failed")
        return None

def test_get_user_data():
    print(Colors.WHITE+"[TEST] Fetching user data...")
    data = auth_db.get_user_data("testnick")
    print(Colors.MAGENTA+"User data:", data)

def test_chat_creation(nick):
    print(Colors.WHITE+"[TEST] Creating chat room...")
    future_date = (datetime.now() + timedelta(days=1)).date().isoformat()
    result = chat_db.ensure_chat_exists("TestRoom", permission_level=0, self_destruction_date=future_date, user_nick=nick)
    chat_info = json.loads(result)
    if chat_info.get("status") == "created":
        print(Colors.GREEN+f"Chat created with UUID: {chat_info['uuid']}")
    else:
        print(Colors.BLUE+f"Chat already exists with UUID: {chat_info['uuid']}")
    return chat_info['uuid']

def test_send_and_get_messages(chat_uuid, sender):
    print(Colors.WHITE+"[TEST] Sending message...")
    timestamp = datetime.now().isoformat()
    chat_db.send_msg(chat_uuid, sender, "Hello, world!", timestamp)
    print(Colors.GREEN+"Message sent.")

    print(Colors.WHITE+"[TEST] Fetching messages...")
    msgs = chat_db.get_msg(chat_uuid)
    print(Colors.MAGENTA+"Messages:", msgs)

def test_cleanup():
    print(Colors.WHITE+"[TEST] Running cleanup (if any expired chats)...")
    chat_db.cleanup_expired_chats()
    print(Colors.GREEN+"Cleanup run.")

def run_all_tests():
    test_user_creation()
    token = test_user_authentication()
    if token:
        nick = auth_db.get_user_by_token(token)
        test_get_user_data()
        chat_uuid = test_chat_creation(nick)
        test_send_and_get_messages(chat_uuid, nick)
        test_cleanup()
    else:
        print(Colors.RED+"Cannot continue without valid token.")

if __name__ == "__main__":
    run_all_tests()
