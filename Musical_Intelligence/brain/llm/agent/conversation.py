"""Conversation Manager — session history and message management.

Uses SQLite for lightweight, zero-dependency persistence.
Designed for easy migration to PostgreSQL later.

Usage:
    from Musical_Intelligence.brain.llm.agent.conversation import ConversationManager

    mgr = ConversationManager()
    mgr.add_message(user_id="u1", session_id="s1", role="user", content="Merhaba")
    history = mgr.get_history(user_id="u1", session_id="s1")
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Musical_Intelligence.brain.llm.config import LLM_ROOT

# ── Database Path ───────────────────────────────────────────────────

DB_PATH = LLM_ROOT / "conversations.db"


# ── Message Type ────────────────────────────────────────────────────


class Message:
    """A single conversation message."""

    def __init__(
        self,
        role: str,
        content: str,
        *,
        message_id: str | None = None,
        timestamp: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.role = role  # "user", "assistant", "system"
        self.content = content
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.metadata = metadata or {}

    def to_api_format(self) -> dict[str, str]:
        """Convert to Claude/OpenAI API message format."""
        return {"role": self.role, "content": self.content}

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


# ── Conversation Manager ───────────────────────────────────────────


class ConversationManager:
    """SQLite-backed conversation history manager."""

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self._ensure_db()

    def _ensure_db(self) -> None:
        """Create tables if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_user
                ON sessions(user_id, updated_at)
            """)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    # ── Session Management ──────────────────────────────────────────

    def create_session(
        self,
        user_id: str,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Create a new conversation session."""
        session_id = session_id or str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        meta_json = json.dumps(metadata or {})

        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, user_id, created_at, updated_at, metadata) "
                "VALUES (?, ?, ?, ?, ?)",
                (session_id, user_id, now, now, meta_json),
            )
        return session_id

    def get_sessions(
        self,
        user_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get recent sessions for a user."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT session_id, created_at, updated_at, metadata "
                "FROM sessions WHERE user_id = ? ORDER BY updated_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        return [
            {
                "session_id": r[0],
                "created_at": r[1],
                "updated_at": r[2],
                "metadata": json.loads(r[3]),
            }
            for r in rows
        ]

    # ── Message Management ──────────────────────────────────────────

    def add_message(
        self,
        user_id: str,
        session_id: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Add a message to a session."""
        msg = Message(role=role, content=content, metadata=metadata)

        # Ensure session exists
        self.create_session(user_id, session_id)

        now = datetime.now(timezone.utc).isoformat()
        meta_json = json.dumps(msg.metadata)

        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (message_id, session_id, user_id, role, content, timestamp, metadata) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (msg.message_id, session_id, user_id, msg.role, msg.content, msg.timestamp, meta_json),
            )
            conn.execute(
                "UPDATE sessions SET updated_at = ? WHERE session_id = ?",
                (now, session_id),
            )

        return msg

    def get_history(
        self,
        user_id: str,
        session_id: str,
        limit: int = 50,
    ) -> list[Message]:
        """Get message history for a session."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT message_id, role, content, timestamp, metadata "
                "FROM messages WHERE session_id = ? AND user_id = ? "
                "ORDER BY timestamp ASC LIMIT ?",
                (session_id, user_id, limit),
            ).fetchall()

        return [
            Message(
                role=r[1],
                content=r[2],
                message_id=r[0],
                timestamp=r[3],
                metadata=json.loads(r[4]),
            )
            for r in rows
        ]

    def get_api_messages(
        self,
        user_id: str,
        session_id: str,
        max_tokens: int = 2000,
    ) -> list[dict[str, str]]:
        """Get message history formatted for Claude/OpenAI API.

        Trims older messages to stay within token budget.
        """
        messages = self.get_history(user_id, session_id)
        api_msgs = [m.to_api_format() for m in messages]

        # Trim from the front to stay within budget
        total_tokens = sum(len(m["content"]) // 4 for m in api_msgs)
        while total_tokens > max_tokens and len(api_msgs) > 2:
            removed = api_msgs.pop(0)
            total_tokens -= len(removed["content"]) // 4

        return api_msgs

    # ── Cleanup ─────────────────────────────────────────────────────

    def delete_session(self, session_id: str) -> None:
        """Delete a session and all its messages."""
        with self._connect() as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))

    def message_count(self, session_id: str) -> int:
        """Get message count for a session."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return row[0] if row else 0
