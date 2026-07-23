import argparse
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "users.db"
SEED_PATH = BASE_DIR / "data" / "users_seed.json"


@dataclass
class User:
    user_id: int
    name: str
    role: str
    active: bool


class UserRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    active INTEGER NOT NULL DEFAULT 1
                )
                """
            )

    def add_user(self, name: str, role: str, active: bool = True) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, role, active) VALUES (?, ?, ?)",
                (name, role, int(active)),
            )
            return int(cur.lastrowid)

    def list_users(self) -> list[User]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, role, active FROM users ORDER BY id"
            ).fetchall()
        return [User(user_id=r[0], name=r[1], role=r[2], active=bool(r[3])) for r in rows]

    def get_user(self, user_id: int) -> User | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, role, active FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
        if row is None:
            return None
        return User(user_id=row[0], name=row[1], role=row[2], active=bool(row[3]))

    def deactivate_user(self, user_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("UPDATE users SET active = 0 WHERE id = ?", (user_id,))
            return cur.rowcount > 0

    def count_by_role(self) -> dict[str, int]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY role"
            ).fetchall()
        return {role: count for role, count in rows}


def seed_users(repo: UserRepository, seed_path: Path) -> None:
    text = seed_path.read_text(encoding="utf-8")
    users = json.loads(text)
    for item in users:
        repo.add_user(
            name=item["name"],
            role=item["role"],
            active=bool(item.get("active", True)),
        )


def print_users(users: list[User]) -> None:
    if not users:
        print("No users found.")
        return
    for user in users:
        print(
            {
                "id": user.user_id,
                "name": user.name,
                "role": user.role,
                "active": user.active,
            }
        )


def print_report(repo: UserRepository) -> None:
    users = repo.list_users()
    report = {
        "total": len(users),
        "active_count": len([u for u in users if u.active]),
        "role_count": repo.count_by_role(),
        "frontend_names": [u.name for u in users if u.role == "frontend"],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="User Data Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db")
    sub.add_parser("seed")
    sub.add_parser("list")
    sub.add_parser("report")

    get_parser = sub.add_parser("get")
    get_parser.add_argument("--user-id", type=int, required=True)

    add_parser = sub.add_parser("add")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--active", choices=["true", "false"], default="true")

    deact_parser = sub.add_parser("deactivate")
    deact_parser.add_argument("--user-id", type=int, required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    repo = UserRepository(DB_PATH)

    if args.command == "init-db":
        repo.init_db()
        print(f"Initialized DB: {DB_PATH}")
        return

    if args.command == "seed":
        repo.init_db()
        seed_users(repo, SEED_PATH)
        print(f"Seeded from: {SEED_PATH}")
        return

    if args.command == "list":
        repo.init_db()
        print_users(repo.list_users())
        return

    if args.command == "get":
        repo.init_db()
        user = repo.get_user(args.user_id)
        if user is None:
            print("User not found")
            return
        print(
            {
                "id": user.user_id,
                "name": user.name,
                "role": user.role,
                "active": user.active,
            }
        )
        return

    if args.command == "add":
        repo.init_db()
        user_id = repo.add_user(
            name=args.name,
            role=args.role,
            active=args.active == "true",
        )
        print(f"Created user id={user_id}")
        return

    if args.command == "deactivate":
        repo.init_db()
        ok = repo.deactivate_user(args.user_id)
        print("Updated" if ok else "User not found")
        return

    if args.command == "report":
        repo.init_db()
        print_report(repo)
        return


if __name__ == "__main__":
    main()
