"""Append-only event records for timetable changes and generation requests."""
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.getenv("TTG_AUDIT_DB", "ttg_audit.sqlite3"))


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=5)
    db.execute("CREATE TABLE IF NOT EXISTS audit_events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL)")
    return db


def record(actor: str, action: str, details: dict):
    with _connect() as db:
        db.execute("INSERT INTO audit_events(timestamp, actor, action, details) VALUES(?,?,?,?)",
                   (datetime.now(timezone.utc).isoformat(), actor, action,
                    json.dumps(details, sort_keys=True, separators=(",", ":"))))


def recent(limit=100):
    with _connect() as db:
        rows = db.execute("SELECT timestamp,actor,action,details FROM audit_events ORDER BY id DESC LIMIT ?",
                          (min(max(limit, 1), 500),)).fetchall()
    return [{"timestamp": t, "actor": a, "action": act, "details": json.loads(d)} for t, a, act, d in rows]
