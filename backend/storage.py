
import json
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = Path(
    os.getenv(
        "CINEMATCH_DB_PATH",
        str(BASE_DIR / "data" / "cinematch.sqlite3")
    )
)

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH, timeout=30)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anonymous_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                movie_data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(anonymous_id, movie_id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS movie_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anonymous_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                feedback TEXT NOT NULL
                    CHECK(feedback IN ('like', 'dislike')),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(anonymous_id, movie_id)
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_watchlist_user
            ON watchlist(anonymous_id)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_user
            ON movie_feedback(anonymous_id)
        """)


def get_watchlist(anonymous_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT movie_data, created_at
            FROM watchlist
            WHERE anonymous_id = ?
            ORDER BY created_at DESC
            """,
            (anonymous_id,)
        ).fetchall()

    return [
        {
            **json.loads(row["movie_data"]),
            "saved_at": row["created_at"]
        }
        for row in rows
    ]


def add_to_watchlist(anonymous_id, movie):
    movie_id = int(movie["movieId"])

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO watchlist (
                anonymous_id,
                movie_id,
                movie_data
            )
            VALUES (?, ?, ?)
            ON CONFLICT(anonymous_id, movie_id)
            DO UPDATE SET movie_data = excluded.movie_data
            """,
            (
                anonymous_id,
                movie_id,
                json.dumps(movie)
            )
        )

    return get_watchlist(anonymous_id)


def remove_from_watchlist(anonymous_id, movie_id):
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM watchlist
            WHERE anonymous_id = ? AND movie_id = ?
            """,
            (anonymous_id, int(movie_id))
        )

    return get_watchlist(anonymous_id)


def get_feedback(anonymous_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT movie_id, feedback
            FROM movie_feedback
            WHERE anonymous_id = ?
            """,
            (anonymous_id,)
        ).fetchall()

    return [
        {
            "movieId": row["movie_id"],
            "feedback": row["feedback"]
        }
        for row in rows
    ]


def save_feedback(anonymous_id, movie_id, feedback):
    if feedback not in ("like", "dislike"):
        raise ValueError("Feedback must be like or dislike.")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO movie_feedback (
                anonymous_id,
                movie_id,
                feedback
            )
            VALUES (?, ?, ?)
            ON CONFLICT(anonymous_id, movie_id)
            DO UPDATE SET
                feedback = excluded.feedback,
                created_at = CURRENT_TIMESTAMP
            """,
            (anonymous_id, int(movie_id), feedback)
        )

    return get_feedback(anonymous_id)


def delete_feedback(anonymous_id, movie_id):
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM movie_feedback
            WHERE anonymous_id = ? AND movie_id = ?
            """,
            (anonymous_id, int(movie_id))
        )

    return get_feedback(anonymous_id)
