import sqlite3
import json

DB_NAME = "idlecraft.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            inventory TEXT,
            equipment TEXT,
            stats TEXT
        )
        ''')
        conn.commit()

def get_or_create_player(user_id: str, name: str = "Игрок"):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return parse_player(row)

        # Если игрока нет — создать
        inventory = json.dumps({})
        equipment = json.dumps({
            "helmet": None, "shoulders": None, "chest": None,
            "legs": None, "boots": None, "left_hand": None, "right_hand": None
        })
        stats = json.dumps({
            "strength": 10, "agility": 8, "endurance": 12, "intellect": 6
        })
        cursor.execute(
            "INSERT INTO players (user_id, name, inventory, equipment, stats) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, inventory, equipment, stats)
        )
        conn.commit()
        return {
            "user_id": user_id,
            "name": name,
            "inventory": {},
            "equipment": json.loads(equipment),
            "stats": json.loads(stats)
        }

def update_player_field(user_id: str, field: str, data: dict):
    with get_connection() as conn:
        conn.execute(f"UPDATE players SET {field} = ? WHERE user_id = ?",
                     (json.dumps(data), user_id))
        conn.commit()

def parse_player(row):
    return {
        "user_id": row[0],
        "name": row[1],
        "inventory": json.loads(row[2]),
        "equipment": json.loads(row[3]),
        "stats": json.loads(row[4])
    }
