
import sqlite3, uuid, bcrypt, json
from datetime import date

class AuthDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def close(self):
        self.conn.close()

    def add_user(self, nick, name, surname, password, rank):
        pdw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        today = date.today().isoformat()
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users WHERE Nick = ?", (nick,))
        if cursor.fetchone():
            return json.dumps({"error": "Nick already exists"})

        cursor.execute(
            """INSERT INTO users (Nick, Name, Surname, Password, RegisterDate, Rank,MsgSend)
            VALUES (?, ?, ?, ?, ?,?,0)""",
            (nick, name, surname, pdw, today, rank)
        )
        self.conn.commit()
        cursor.close()
        return json.dumps({"status": "user_created"})

    def verify_user(self, nick, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT Password FROM users WHERE Nick = ?', (nick,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode(), result[0]):
            token = str(uuid.uuid4())
            cursor.execute("UPDATE users SET Token = ? WHERE Nick = ?", (token, nick))
            self.conn.commit()
            cursor.close()
            return token

        cursor.close()
        return None

    def get_user_by_token(self, token):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Nick FROM users WHERE Token = ?", (token,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_user_data(self, nick):
        cursor = self.conn.cursor()
        row = cursor.execute(
            'SELECT oid, Nick, Name, Surname, RegisterDate, MsgSend, Rank FROM users WHERE Nick = ?',
            (nick,)
        ).fetchone()
        self.conn.commit()
        cursor.close()

        if row:
            return json.dumps({
                "oid": row[0], "Nick": row[1], "Name": row[2],
                "Surname": row[3], "RegisterDate": row[4],
                "MsgSend": row[5], "Rank": row[6]
            })
        else:
            return json.dumps({"error": "User not found"})

    def get_user_level(self, nick):
        cursor = self.conn.execute(
            "SELECT permission_level FROM users WHERE nick = ?",
            (nick,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def user_count(self):
        cursor = self.conn.cursor()
        num = cursor.execute("Select Count(*) from users")
        num=num.fetchone()
        x=num[0]
        self.conn.commit()
        cursor.close()
        return x