from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "learning.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS courses")

cursor.execute(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        years INTEGER NOT NULL,
        city TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        hours INTEGER NOT NULL
    )
    """
)

cursor.executemany(
    "INSERT INTO users (name, role, years, city) VALUES (?, ?, ?, ?)",
    [
        ("Ace", "Frontend Developer", 3, "Shanghai"),
        ("Lily", "Backend Developer", 5, "Beijing"),
        ("Tom", "QA Engineer", 2, "Shenzhen"),
        ("Mia", "Product Manager", 4, "Hangzhou"),
    ],
)

cursor.executemany(
    "INSERT INTO courses (title, category, difficulty, hours) VALUES (?, ?, ?, ?)",
    [
        ("Python Basics", "Python", "Beginner", 8),
        ("SQLite Basics", "Database", "Beginner", 4),
        ("FastAPI Starter", "Backend", "Intermediate", 10),
        ("Pytest Starter", "Testing", "Beginner", 6),
    ],
)

connection.commit()
connection.close()

print(f"SQLite database created: {DB_PATH}")
