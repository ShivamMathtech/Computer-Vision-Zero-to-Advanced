"""Small append-only SQLite event store. Images are not retained."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class EventStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS frames (session TEXT, frame INTEGER, timestamp REAL, report TEXT, PRIMARY KEY(session, frame))"
            )

    def connect(self):
        return sqlite3.connect(self.path, timeout=5)

    def append(self, session, frame, timestamp, report):
        with self.connect() as db:
            db.execute(
                "INSERT INTO frames VALUES (?,?,?,?)",
                (session, frame, timestamp, json.dumps(report, allow_nan=False)),
            )

    def history(self, session, limit=100):
        with self.connect() as db:
            rows = db.execute(
                "SELECT frame,timestamp,report FROM frames WHERE session=? ORDER BY frame DESC LIMIT ?",
                (session, limit),
            ).fetchall()
        return [{"frame_id": r[0], "timestamp": r[1], **json.loads(r[2])} for r in reversed(rows)]
