
import sqlite3, uuid, json, threading
from datetime import date

class ChatDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        # self.schedule_cleanup()

    def close(self):
        self.conn.close()

    def ensure_chat_exists(self, chat_name, permission_level=0, self_destruction_date=None, user_nick=None):
        cursor = self.conn.cursor()
        cursor.execute("SELECT uuid FROM chats WHERE name = ?", (chat_name,))
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            return json.dumps({"status": "exists", "uuid": existing[0]})

        new_uuid = str(uuid.uuid4())
        today = date.today().isoformat()

        cursor.execute(
            """INSERT INTO chats (name, uuid, permissionToAccess, DateOfCreation, DateOfSelfDestruction)
            VALUES (?, ?, ?, ?, ?)""",
            (chat_name, new_uuid, permission_level, today, self_destruction_date)
        )

        messages_table_name = f"messages_{new_uuid.replace('-', '_')}"
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {messages_table_name} (
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        if user_nick:
            cursor.execute("SELECT oid FROM users WHERE Nick = ?", (user_nick,))
            user_oid = cursor.fetchone()
            if user_oid:
                cursor.execute("INSERT INTO user_chats (user_oid, chat_uuid) VALUES (?, ?)", (user_oid[0], new_uuid))

        self.conn.commit()
        cursor.close()

        return json.dumps({
            "status": "created",
            "uuid": new_uuid,
            "messages_table": messages_table_name
        })

    def send_msg(self, chat_uuid, sender_nick, message, timestamp):
        table_name = f"messages_{chat_uuid.replace('-', '_')}"
        cursor = self.conn.cursor()

        cursor.execute(f"""
            INSERT INTO {table_name} (sender, message, timestamp)
            VALUES (?, ?, ?)""", (sender_nick, message, timestamp))

        cursor.execute("UPDATE users SET MsgSend = MsgSend + 1 WHERE Nick = ?", (sender_nick,))
        self.conn.commit()
        cursor.close()

    def get_msg(self, chat_uuid, limit=50):
        table_name = f"messages_{chat_uuid.replace('-', '_')}"
        cursor = self.conn.cursor()

        cursor.execute(f"""
            SELECT sender, message, timestamp FROM {table_name}
            ORDER BY ROWID DESC LIMIT ?""", (limit,))
        messages = cursor.fetchall()
        cursor.close()

        return json.dumps([
            {"sender": msg[0], "message": msg[1], "timestamp": msg[2]}
            for msg in reversed(messages)
        ])

    def has_permission(self, chat_uuid):
        cursor = self.conn.cursor()
        cursor.execute("SELECT permissionToAccess FROM chats WHERE uuid = ?", (chat_uuid,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def cleanup_expired_chats(self):
        cursor = self.conn.cursor()
        today = date.today().isoformat()

        cursor.execute("""
            SELECT uuid FROM chats 
            WHERE DateOfSelfDestruction IS NOT NULL 
            AND DateOfSelfDestruction <= ?""", (today,))
        expired_chats = cursor.fetchall()

        for (chat_uuid,) in expired_chats:
            messages_table = f"messages_{chat_uuid.replace('-', '_')}"
            cursor.execute(f"DROP TABLE IF EXISTS {messages_table}")
            cursor.execute("DELETE FROM chats WHERE uuid = ?", (chat_uuid,))

        self.conn.commit()
        cursor.close()

    def list_chats_by_permission(self, permission_level):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, uuid, permissionToAccess FROM chats 
            WHERE permissionToAccess <= ?""", (permission_level,))
        chats = cursor.fetchall()
        cursor.close()
        return json.dumps([
            {"name": chat[0], "uuid": chat[1], "permission": chat[2]}
            for chat in chats
        ])

    def get_saved_and_accessible_chats(self, user_nick):
        cursor = self.conn.cursor()
        cursor.execute("SELECT oid FROM users WHERE Nick = ?", (user_nick,))
        user_oid = cursor.fetchone()
        if not user_oid:
            cursor.close()
            return json.dumps({"error": "User not found"})

        user_oid = user_oid[0]
        cursor.execute("SELECT chat_uuid FROM user_chats WHERE user_oid = ?", (user_oid,))
        saved_chats = cursor.fetchall()

        cursor.execute("SELECT uuid FROM chats WHERE permissionToAccess = -1")
        accessible_chats = cursor.fetchall()

        all_chats = set([c[0] for c in saved_chats]) | set([c[0] for c in accessible_chats])
        if not all_chats:
            cursor.close()
            return json.dumps([{"error":"No Chats Avalable",}])

        cursor.execute(
            f"SELECT name, uuid, permissionToAccess FROM chats WHERE uuid IN ({','.join(['?'] * len(all_chats))})",
            tuple(all_chats)
        )

        chats = cursor.fetchall()
        cursor.close()

        return json.dumps([
            {"name": chat[0], "uuid": chat[1], "permission": chat[2]}
            for chat in chats
        ])

    def is_chat_owner(self, chat_uuid, nick):
        cursor = self.conn.execute(
            "SELECT owner FROM chats WHERE uuid = ?",
            (chat_uuid,)
        )
        row = cursor.fetchone()
        return row and row[0] == nick

    def update_chat_name(self, chat_uuid, new_name):
        with self.conn:
            cursor = self.conn.execute(
                "UPDATE chats SET name = ? WHERE uuid = ?",
                (new_name, chat_uuid)
            )
            return cursor.rowcount > 0

    def delete_chat(self, chat_uuid):
        with self.conn:
            self.conn.execute(
                "DELETE FROM messages WHERE chat_uuid = ?",
                (chat_uuid,)
            )
            cursor = self.conn.execute(
                "DELETE FROM chats WHERE uuid = ?",
                (chat_uuid,)
            )
            return cursor.rowcount > 0
