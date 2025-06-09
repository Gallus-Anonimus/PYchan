import sqlite3
import os

DB_FILE = "../Data/db.db"

def GhostProtocol(db_path=DB_FILE):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Creating new database: {db_path}")


    cursor.execute("""
    CREATE TABLE users (
        oid INTEGER PRIMARY KEY AUTOINCREMENT,
        Nick TEXT UNIQUE NOT NULL,
        Name TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Password BLOB NOT NULL,
        RegisterDate TEXT NOT NULL,
        MsgSend INTEGER DEFAULT 0,
        Rank INTEGER DEFAULT 0,
        Token TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        uuid TEXT UNIQUE NOT NULL,
        permissionToAccess INTEGER NOT NULL DEFAULT 0,
        DateOfCreation TEXT NOT NULL,
        DateOfSelfDestruction TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE user_chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_oid INTEGER NOT NULL,
        chat_uuid TEXT NOT NULL,
        FOREIGN KEY (user_oid) REFERENCES users(oid) ON DELETE CASCADE,
        FOREIGN KEY (chat_uuid) REFERENCES chats(uuid) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("Database created and initialized successfully.")

if __name__ == "__main__":
    GhostProtocol()
