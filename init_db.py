# init_db.py
# Запускать один раз: python init_db.py
# Создаёт файл database.db со всеми таблицами для бота

import sqlite3
from pathlib import Path

DB_PATH = "database.db"
db_file = Path(DB_PATH)

if db_file.exists():
    print(f"База данных {DB_PATH} уже существует. Пропускаем создание.")
else:
    print(f"Создаём новую базу данных: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ===================== ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ =====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,     -- Telegram user_id
    username    TEXT,                    -- @username (может быть NULL)
    first_name  TEXT,
    registered  TEXT DEFAULT (date('now')) -- дата регистрации
)
''')

# ===================== ФИЗИЧЕСКОЕ БЛАГОПОЛУЧИЕ (Тело) =====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS trackers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    date       TEXT NOT NULL,           -- формат YYYY-MM-DD
    water      REAL  DEFAULT 0,         -- литры воды
    sleep      INTEGER DEFAULT 0,       -- часы сна
    steps      INTEGER DEFAULT 0,       -- шаги (если захотим добавить позже)
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
)
''')

# ===================== ПСИХОЛОГИЧЕСКОЕ БЛАГОПОЛУЧИЕ (Душа) =====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS moods (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    date       TEXT NOT NULL,           -- YYYY-MM-DD
    mood       TEXT NOT NULL,           -- например: "Хорошо", "Плохо", "Нормально"
    note       TEXT,                    -- необязательная заметка
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
)
''')

# ===================== ЧЕЛЛЕНДЖИ И ГЕЙМИФИКАЦИЯ =====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS challenges (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    challenge_name  TEXT NOT NULL,           -- например: "Зарядка 5 дней подряд"
    start_date      TEXT NOT NULL,
    current_day     INTEGER DEFAULT 1,       -- текущий день челленджа
    total_days      INTEGER DEFAULT 5,       -- сколько дней нужно
    completed       INTEGER DEFAULT 0,       -- 0 = в процессе, 1 = выполнен
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# ===================== ДОПОЛНИТЕЛЬНО: очки и ачивки (для вау-фактора) =====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS achievements (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    title       TEXT NOT NULL,           -- например: "Гидратация мастер"
    description TEXT,
    emoji       TEXT DEFAULT "Trophy",
    unlocked_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_points (
    user_id     INTEGER PRIMARY KEY,
    points      INTEGER DEFAULT 0,
    level       INTEGER DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных успешно создана / обновлена!")
print("Таблицы:")
print("  • users")
print("  • trackers")
print("  • moods")
print("  • challenges")
print("  • achievements")
print("  • user_points")
print("\nГотово! Теперь можно запускать бота: python main.py")