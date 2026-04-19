import sqlite3
import secrets
import datetime
from pathlib import Path
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

DB_DIR = Path(__file__).resolve().parent / 'db'
DB_PATH = DB_DIR / 'cookai.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        db.row_factory = sqlite3.Row
        g._database = db
    return db


def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                token TEXT UNIQUE,
                created_at TEXT NOT NULL
            )
            '''
        )
        db.execute(
            '''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                result_count INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            '''
        )
        db.commit()


def create_user(username, password):
    db = get_db()
    token = secrets.token_hex(16)
    password_hash = generate_password_hash(password)
    created_at = datetime.datetime.utcnow().isoformat()
    db.execute(
        'INSERT INTO users (username, password_hash, token, created_at) VALUES (?, ?, ?, ?)',
        (username, password_hash, token, created_at),
    )
    db.commit()
    return token


def update_user_token(user_id, token):
    db = get_db()
    db.execute('UPDATE users SET token = ? WHERE id = ?', (token, user_id))
    db.commit()


def get_user_by_username(username):
    db = get_db()
    return db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()


def get_user_by_token(token):
    if not token:
        return None
    db = get_db()
    return db.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()


def save_history(user_id, query, result_count):
    db = get_db()
    created_at = datetime.datetime.utcnow().isoformat()
    db.execute(
        'INSERT INTO history (user_id, query, result_count, created_at) VALUES (?, ?, ?, ?)',
        (user_id, query, result_count, created_at),
    )
    db.commit()


def get_history(user_id, limit=20):
    db = get_db()
    rows = db.execute(
        'SELECT query, result_count, created_at FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?',
        (user_id, limit),
    ).fetchall()
    return [dict(row) for row in rows]
