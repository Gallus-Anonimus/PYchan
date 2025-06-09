import socket
import json

HOST = input() or "192.168.99.10"
PORT = 12345


def send_request(sock, request_dict):
    try:
        message = json.dumps(request_dict)
        sock.sendall(message.encode())
        response = sock.recv(8192).decode()
        return response
    except Exception as e:
        print("Error during request:", e)
        return None


def interactive_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))


        token = None
        chat_uuid = None

        while True:
            print("\nOptions: register, login, create_chat, select_chat, send_msg, get_msgs, user_data, quit")
            choice = input("Choose action: ").strip().lower()

            if choice == "register":
                nick = input("Nick: ")
                name = input("Name: ")
                surname = input("Surname: ")
                password = input("Password: ")
                req = {
                    "action": "register",
                    "nick": nick,
                    "name": name,
                    "surname": surname,
                    "password": password
                }
                print(send_request(sock, req))

            elif choice == "login":
                nick = input("Nick: ")
                password = input("Password: ")
                req = {
                    "action": "login",
                    "nick": nick,
                    "password": password
                }
                response = json.loads(send_request(sock, req))
                if response.get("status") == "success":
                    token = response.get("token")
                    print("[+] Login successful. Token saved.")
                else:
                    print(response)

            elif choice == "create_chat":
                if not token:
                    print("You must log in first.")
                    continue
                chat_name = input("Chat name: ")
                req = {
                    "action": "create_chat",
                    "token": token,
                    "chat_name": chat_name
                }
                response = json.loads(send_request(sock, req))
                chat_uuid = response.get("uuid")
                print(f"[+] Chat UUID: {chat_uuid}")
                print(response)

            elif choice == "send_msg":
                if not token or not chat_uuid:
                    print("You must be logged in and have a chat selected.")
                    continue
                msg = input("Message: ")
                req = {
                    "action": "send_msg",
                    "token": token,
                    "chat_uuid": chat_uuid,
                    "message": msg
                }
                print(send_request(sock, req))

            elif choice == "get_msgs":
                if not chat_uuid:
                    print("No chat selected.")
                    continue
                req = {
                    "action": "get_msgs",
                    "chat_uuid": chat_uuid
                }
                response = json.loads(send_request(sock, req))
                for msg in response.get("messages", []):
                    print(f"[{msg['timestamp']}] {msg['sender']}: {msg['message']}")

            elif choice == "user_data":
                if not token:
                    print("Login first.")
                    continue
                req = {
                    "action": "user_data",
                    "token": token
                }
                print(send_request(sock, req))

            elif choice == "quit":
                print("Exiting client.")
                break


            elif choice == "select_chat":
                if not token:
                    print("You must log in first.")
                    continue

                req = {
                    "action": "list_chats",
                    "token": token
                }

                response = json.loads(send_request(sock, req))
                print(response)
                chats = response.get("chats", [])

                if not chats:
                    print("No available chats.")
                    continue

                for idx, chat in enumerate(chats):
                    print(f"{idx + 1}. {chat['name']} ({chat['uuid']})")
                selection = input("Select chat number: ")

                try:

                    index = int(selection) - 1
                    if 0 <= index < len(chats):
                        chat_uuid = chats[index]["uuid"]
                        print(f"Selected chat: {chat_uuid}")
                    else:
                        print("Invalid selection.")
                except ValueError:

                    print("Invalid input.")


if __name__ == "__main__":
    interactive_client()
