#!/usr/bin/env python3
"""Initialize database schema and seed data."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import mysql.connector
from config import Config

# MySQL error codes that are safe to ignore on re-run
IGNORE_ERRNO = {1050, 1061, 1062}  # table exists, duplicate key name, duplicate entry


def parse_sql_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    statements: list[str] = []
    current: list[str] = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        current.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(current).strip())
            current = []
    return statements


def run_sql_file(cursor, filepath: str, db_name: str) -> None:
    statements = parse_sql_file(filepath)
    errors: list[str] = []

    for stmt in statements:
        upper = stmt.upper().lstrip()

        if upper.startswith("USE "):
            cursor.execute(stmt)
            continue

        if upper.startswith("CREATE DATABASE"):
            cursor.execute(stmt)
            cursor.execute(f"USE `{db_name}`")
            continue

        try:
            cursor.execute(stmt)
        except mysql.connector.Error as e:
            if e.errno in IGNORE_ERRNO:
                continue
            errors.append(f"  [{e.errno}] {e.msg}\n    → {stmt[:120]}...")

    if errors:
        print(f"  ✗ {os.path.basename(filepath)} — {len(errors)} error(s):")
        for err in errors:
            print(err)
        raise RuntimeError(f"Failed to apply {os.path.basename(filepath)}")

    print(f"  ✓ {os.path.basename(filepath)}")


def ensure_recipe_instructions(cursor, db_name: str) -> None:
    cursor.execute(
        """
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema = %s AND table_name = 'recipes' AND column_name = 'instructions'
        """,
        (db_name,),
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute("ALTER TABLE recipes ADD COLUMN instructions TEXT NULL AFTER description")
        print("  ✓ recipes.instructions added")
    else:
        print("  ✓ recipes.instructions already exists")


def ensure_rating_count(cursor, db_name: str) -> None:
    cursor.execute(
        """
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema = %s AND table_name = 'recipes' AND column_name = 'rating_count'
        """,
        (db_name,),
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "ALTER TABLE recipes ADD COLUMN rating_count INT UNSIGNED NOT NULL DEFAULT 0 AFTER rating"
        )
        print("  ✓ recipes.rating_count added")
    else:
        print("  ✓ recipes.rating_count already exists")


def apply_migrations(cursor, db_name: str) -> None:
    db_dir = os.path.join(os.path.dirname(__file__), "database")
    run_sql_file(cursor, os.path.join(db_dir, "migrations.sql"), db_name)


def verify_tables(cursor, db_name: str) -> None:
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = %s",
        (db_name,),
    )
    count = cursor.fetchone()[0]
    if count == 0:
        raise RuntimeError(f"No tables found in database `{db_name}`")
    print(f"  ✓ Verified {count} tables in `{db_name}`")


def verify_seed(cursor) -> None:
    checks = {
        "ingredient_categories": 10,
        "recipe_categories": 7,
        "recipes": 100,
    }
    for table, minimum in checks.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE is_active = 1")
        count = cursor.fetchone()[0]
        if count < minimum:
            raise RuntimeError(f"{table}: expected at least {minimum} rows, found {count}")
        print(f"  ✓ {table}: {count}")

    cursor.execute("SELECT COUNT(*) FROM ingredients WHERE is_active = 1")
    ingredients = cursor.fetchone()[0]
    if ingredients < 100:
        raise RuntimeError(f"ingredients: expected at least 100 rows, found {ingredients}")
    cursor.execute("SELECT COUNT(*) FROM recipe_ingredients")
    links = cursor.fetchone()[0]
    cursor.execute(
        """
        SELECT COUNT(*) FROM recipes r
        WHERE r.is_active = 1 AND (
            r.instructions IS NULL OR r.instructions = ''
            OR NOT EXISTS (SELECT 1 FROM recipe_ingredients ri WHERE ri.recipe_id = r.id)
        )
        """
    )
    incomplete = cursor.fetchone()[0]
    if incomplete:
        raise RuntimeError(f"{incomplete} recipes are missing instructions or ingredients")
    print(f"  ✓ ingredients: {ingredients}")
    print(f"  ✓ recipe_ingredients: {links}")


def main():
    db_name = Config.DB_NAME
    print(f"Connecting to MySQL as {Config.DB_USER}@{Config.DB_HOST}...")

    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
    )
    cursor = conn.cursor()

    db_dir = os.path.join(os.path.dirname(__file__), "database")

    print("Running schema...")
    run_sql_file(cursor, os.path.join(db_dir, "schema.sql"), db_name)
    conn.commit()

    cursor.execute(f"USE `{db_name}`")
    print("Running migrations...")
    ensure_recipe_instructions(cursor, db_name)
    ensure_rating_count(cursor, db_name)
    apply_migrations(cursor, db_name)
    conn.commit()

    print("Running seed...")
    from database.seed_data import apply_seed
    apply_seed(cursor)
    conn.commit()

    verify_tables(cursor, db_name)
    verify_seed(cursor)

    cursor.close()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nSetup failed: {exc}")
        sys.exit(1)
