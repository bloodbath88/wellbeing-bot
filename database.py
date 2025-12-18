# database.py
import sqlite3
from datetime import datetime
from typing import Optional, List

DB_PATH = "database.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# === Пользователи ===
def add_user(user_id: int, first_name: str, username: str = None):
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO users (id, username, first_name) VALUES (?, ?, ?)",
                 (user_id, username, first_name))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

# === Настроение ===
def has_mood_today(user_id: int) -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM moods WHERE user_id = ? AND date = ?", (user_id, today))
    result = cur.fetchone() is not None
    conn.close()
    return result

def save_mood(user_id: int, mood: str, note: str = ""):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    conn.execute("""INSERT OR REPLACE INTO moods (user_id, date, mood, note)
                     VALUES (?, ?, ?, ?)""", (user_id, today, mood, note))
    add_points(user_id, 10)
    conn.commit()
    conn.close()

# === Трекеры (вода, сон) ===
def update_daily_trackers(user_id: int, water_liters: float = None, sleep_hours: int = None):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    conn.execute("""INSERT INTO trackers (user_id, date, water, sleep)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id, date) DO UPDATE SET
                        water = COALESCE(excluded.water, water),
                        sleep = COALESCE(excluded.sleep, sleep)""",
                 (user_id, today, water_liters, sleep_hours))
    conn.commit()
    conn.close()

def get_today_trackers(user_id: int) -> sqlite3.Row:
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT water, sleep FROM trackers WHERE user_id = ? AND date = ?", (user_id, today))
    row = cur.fetchone()
    conn.close()
    return row

# === Челленджи ===
def set_daily_challenge(user_id: int, text: str):
    conn = get_conn()
    conn.execute("DELETE FROM challenges WHERE user_id = ? AND completed = 0", (user_id,))
    conn.execute("""INSERT INTO challenges (user_id, challenge_name, start_date)
                    VALUES (?, ?, date('now'))""", (user_id, text))
    conn.commit()
    conn.close()

def get_today_challenge(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""SELECT challenge_name FROM challenges
                    WHERE user_id = ? AND completed = 0""", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["challenge_name"] if row else None

def complete_today_challenge(user_id: int):
    conn = get_conn()
    conn.execute("""UPDATE challenges SET completed = 1 WHERE user_id = ? AND completed = 0""", (user_id,))
    add_points(user_id, 50)
    conn.commit()
    conn.close()

# === Очки и ачивки ===
def add_points(user_id: int, points: int):
    conn = get_conn()
    conn.execute("""INSERT INTO user_points (user_id, points) VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET points = points + ?""",
                 (user_id, points, points))
    check_achievements(user_id)
    conn.commit()
    conn.close()

def get_points(user_id: int) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT points FROM user_points WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["points"] if row else 0

def unlock_achievement(user_id: int, title: str, desc: str = "", emoji: str = "Trophy"):
    conn = get_conn()
    conn.execute("""INSERT OR IGNORE INTO achievements (user_id, title, description, emoji)
                    VALUES (?, ?, ?, ?)""", (user_id, title, desc, emoji))
    conn.commit()
    conn.close()

def check_achievements(user_id: int):
    points = get_points(user_id)
    mood_count = len([r for r in get_conn().execute("SELECT date FROM moods WHERE user_id = ?", (user_id,)).fetchall()])
    if points >= 100 and not get_conn().execute("SELECT 1 FROM achievements WHERE user_id = ? AND title = ?", (user_id, "100 очков")).fetchone():
        unlock_achievement(user_id, "100 очков", "Настоящий мастер заботы!", "Star")
    if mood_count >= 7:
        unlock_achievement(user_id, "Неделя настроения", "7 дней подряд отмечал настроение", "Calendar")

def get_achievements(user_id: int) -> List[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT title, description, emoji FROM achievements WHERE user_id = ?", (user_id,))
    achs = cur.fetchall()
    conn.close()
    return achs