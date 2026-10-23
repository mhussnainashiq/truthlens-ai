
import json
import sqlite3
from pathlib import Path

from app.config import get_settings
from app.models import CredibilityReport


def get_connection():
    settings = get_settings()
    database_path = Path(settings.database_path)

    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(database_path),
        timeout=10,
    )
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                headline TEXT NOT NULL DEFAULT '',
                content_type TEXT NOT NULL,
                assessment TEXT NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (
                    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                )
            )
            """
        )


def save_analysis(
    headline: str,
    content_type: str,
    report: CredibilityReport,
) -> int:
    report_json = report.model_dump_json()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analyses (
                headline,
                content_type,
                assessment,
                report_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                headline.strip() or "Untitled analysis",
                content_type,
                report.overall_assessment.value,
                report_json,
            ),
        )
        return cursor.lastrowid


def list_analyses(limit: int = 100) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, headline, content_type, assessment, created_at
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
            """,
            (max(1, min(limit, 100)),),
        ).fetchall()

    return [dict(row) for row in rows]


def get_analysis(analysis_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM analyses
            WHERE id = ?
            """,
            (analysis_id,),
        ).fetchone()

    if row is None:
        return None

    record = dict(row)
    record["report"] = CredibilityReport.model_validate_json(
        record.pop("report_json")
    )
    return record


def delete_analysis(analysis_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM analyses WHERE id = ?",
            (analysis_id,),
        )
        return cursor.rowcount > 0
