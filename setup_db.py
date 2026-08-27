#!/usr/bin/env python3
"""Initialize database schema and seed data."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import mysql.connector
from config import Config


def run_sql_file(cursor, filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    statements = []
    current = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        current.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(current))
            current = []

    for stmt in statements:
        stmt = stmt.strip()
        if stmt.upper().startswith("USE "):
            continue
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as e:
            if e.errno not in (1050, 1062, 1061):
                print(f"Warning: {e}")

    print(f"  ✓ {os.path.basename(filepath)}")


def main():
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
    )
    cursor = conn.cursor()

    db_dir = os.path.join(os.path.dirname(__file__), "database")
    print("Running schema...")
    run_sql_file(cursor, os.path.join(db_dir, "schema.sql"))
    conn.commit()

    cursor.execute(f"USE {Config.DB_NAME}")
    print("Running seed...")
    run_sql_file(cursor, os.path.join(db_dir, "seed.sql"))
    conn.commit()

    cursor.close()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    main()
