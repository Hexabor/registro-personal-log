from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1

REQUIRED_FIELDS = {
    "id",
    "schema_version",
    "created_at",
    "event_date",
    "title",
    "body",
    "summary",
    "type",
    "scopes",
    "tags",
    "people",
    "places",
    "projects",
    "importance",
    "follow_ups",
    "source",
    "raw_input",
    "cleanup_level",
    "content_hash",
    "processing_notes",
}

LIST_FIELDS = {
    "scopes",
    "tags",
    "people",
    "places",
    "projects",
    "follow_ups",
    "processing_notes",
}

ALLOWED_CLEANUP_LEVELS = {"none", "light", "medium", "heavy"}
ALLOWED_TYPES = {
    "event",
    "conversation",
    "idea",
    "decision",
    "task",
    "reflection",
    "learning",
    "health",
    "work",
    "personal",
    "finance",
    "relationship",
    "memory",
    "observation",
    "note",
}


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("pragma foreign_keys = on")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        create table if not exists entries (
          id text primary key,
          schema_version integer not null,
          created_at text not null,
          event_date text not null,
          event_time text null,
          title text not null,
          body text not null,
          summary text not null,
          type text not null,
          scopes text not null,
          tags text not null,
          people text not null,
          places text not null,
          projects text not null,
          mood text null,
          importance integer not null check (importance between 1 and 5),
          follow_ups text not null,
          source text not null,
          raw_input text not null,
          cleanup_level text not null check (cleanup_level in ('none', 'light', 'medium', 'heavy')),
          content_hash text not null,
          processing_notes text not null,
          import_warnings text not null default '[]',
          imported_at text not null default (datetime('now'))
        );

        create index if not exists entries_content_hash_idx on entries (content_hash);
        create index if not exists entries_event_date_idx on entries (event_date);
        create index if not exists entries_type_idx on entries (type);
        """
    )
    conn.commit()


def normalized_hash_value(entry: dict[str, Any]) -> str:
    people = sorted(str(item).strip() for item in entry.get("people", []) if str(item).strip())
    tags = sorted(str(item).strip().lower() for item in entry.get("tags", []) if str(item).strip())
    parts = [
        str(entry.get("event_date", "")).strip(),
        str(entry.get("title", "")).strip(),
        str(entry.get("body", "")).strip(),
        str(entry.get("type", "")).strip(),
        ";".join(people),
        ";".join(tags),
    ]
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_entry(entry: Any, line_number: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return [f"line {line_number}: expected a JSON object"]

    missing = sorted(REQUIRED_FIELDS - entry.keys())
    if missing:
        errors.append(f"line {line_number}: missing required fields: {', '.join(missing)}")

    if entry.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"line {line_number}: schema_version must be {SCHEMA_VERSION}")

    for field in LIST_FIELDS:
        if field in entry and not isinstance(entry[field], list):
            errors.append(f"line {line_number}: {field} must be a list")

    source = entry.get("source")
    if source is not None:
        if not isinstance(source, dict):
            errors.append(f"line {line_number}: source must be an object")
        else:
            for key in ("kind", "batch_id", "assistant"):
                if key not in source:
                    errors.append(f"line {line_number}: source.{key} is required")

    importance = entry.get("importance")
    if not isinstance(importance, int) or not 1 <= importance <= 5:
        errors.append(f"line {line_number}: importance must be an integer from 1 to 5")

    cleanup_level = entry.get("cleanup_level")
    if cleanup_level not in ALLOWED_CLEANUP_LEVELS:
        errors.append(f"line {line_number}: cleanup_level must be one of {sorted(ALLOWED_CLEANUP_LEVELS)}")

    entry_type = entry.get("type")
    if entry_type not in ALLOWED_TYPES:
        errors.append(f"line {line_number}: type must be one of {sorted(ALLOWED_TYPES)}")

    event_time = entry.get("event_time")
    if event_time is not None and not isinstance(event_time, str):
        errors.append(f"line {line_number}: event_time must be HH:MM or null")

    for field in ("id", "created_at", "event_date", "title", "body", "summary", "type", "raw_input", "content_hash"):
        if field in entry and not isinstance(entry[field], str):
            errors.append(f"line {line_number}: {field} must be a string")

    return errors


def canonical_entry_payload(entry: dict[str, Any]) -> str:
    stored = {field: entry.get(field) for field in REQUIRED_FIELDS}
    stored["event_time"] = entry.get("event_time")
    stored["mood"] = entry.get("mood")
    stored["content_hash"] = normalized_hash_value(stored)
    return json.dumps(stored, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue
            errors.extend(validate_entry(entry, line_number))
            if not errors or not any(error.startswith(f"line {line_number}:") for error in errors):
                entries.append(entry)
    return entries, errors


def insert_entry(conn: sqlite3.Connection, entry: dict[str, Any]) -> str:
    current_hash = normalized_hash_value(entry)
    entry = dict(entry)
    entry["content_hash"] = current_hash

    existing = conn.execute("select * from entries where id = ?", (entry["id"],)).fetchone()
    if existing:
        stored_entry = row_to_entry(existing)
        if canonical_entry_payload(stored_entry) == canonical_entry_payload(entry):
            return "skipped_same_id_same_content"
        return "conflict_same_id_different_content"

    warnings: list[str] = []
    duplicate = conn.execute(
        "select id from entries where content_hash = ? and id <> ? limit 1",
        (current_hash, entry["id"]),
    ).fetchone()
    if duplicate:
        warnings.append(f"possible_duplicate_of:{duplicate['id']}")

    conn.execute(
        """
        insert into entries (
          id, schema_version, created_at, event_date, event_time, title, body, summary,
          type, scopes, tags, people, places, projects, mood, importance, follow_ups,
          source, raw_input, cleanup_level, content_hash, processing_notes, import_warnings
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry["id"],
            entry["schema_version"],
            entry["created_at"],
            entry["event_date"],
            entry.get("event_time"),
            entry["title"],
            entry["body"],
            entry["summary"],
            entry["type"],
            json.dumps(entry["scopes"], ensure_ascii=False),
            json.dumps(entry["tags"], ensure_ascii=False),
            json.dumps(entry["people"], ensure_ascii=False),
            json.dumps(entry["places"], ensure_ascii=False),
            json.dumps(entry["projects"], ensure_ascii=False),
            entry.get("mood"),
            entry["importance"],
            json.dumps(entry["follow_ups"], ensure_ascii=False),
            json.dumps(entry["source"], ensure_ascii=False),
            entry["raw_input"],
            entry["cleanup_level"],
            entry["content_hash"],
            json.dumps(entry["processing_notes"], ensure_ascii=False),
            json.dumps(warnings, ensure_ascii=False),
        ),
    )
    return "inserted_with_warning" if warnings else "inserted"


def import_jsonl(db_path: Path, input_path: Path) -> int:
    entries, errors = read_jsonl(input_path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    counts = {
        "inserted": 0,
        "inserted_with_warning": 0,
        "skipped_same_id_same_content": 0,
        "conflict_same_id_different_content": 0,
    }
    with connect(db_path) as conn:
        init_db(conn)
        for entry in entries:
            result = insert_entry(conn, entry)
            counts[result] += 1
        conn.commit()

    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 1 if counts["conflict_same_id_different_content"] else 0


def row_to_entry(row: sqlite3.Row) -> dict[str, Any]:
    entry = dict(row)
    for field in LIST_FIELDS:
        entry[field] = json.loads(entry[field])
    entry["source"] = json.loads(entry["source"])
    entry["import_warnings"] = json.loads(entry["import_warnings"])
    return entry


def fetch_entries(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "select * from entries order by event_date desc, coalesce(event_time, '99:99') desc, created_at desc"
    ).fetchall()
    return [row_to_entry(row) for row in rows]


def export_entries(db_path: Path, output_path: Path, export_format: str) -> None:
    with connect(db_path) as conn:
        init_db(conn)
        entries = fetch_entries(conn)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if export_format == "json":
        output_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    elif export_format == "jsonl":
        lines = [json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries]
        output_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    elif export_format == "csv":
        export_csv(output_path, entries)
    elif export_format == "markdown":
        export_markdown(output_path, entries)
    else:
        raise ValueError(f"unknown export format: {export_format}")

    print(f"exported {len(entries)} entries to {output_path}")


def export_csv(output_path: Path, entries: list[dict[str, Any]]) -> None:
    fields = [
        "id",
        "event_date",
        "event_time",
        "title",
        "summary",
        "type",
        "scopes",
        "tags",
        "people",
        "places",
        "projects",
        "mood",
        "importance",
        "follow_ups",
        "content_hash",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for entry in entries:
            row = {field: entry.get(field) for field in fields}
            for field in LIST_FIELDS - {"processing_notes"}:
                row[field] = "; ".join(entry[field])
            writer.writerow(row)


def export_markdown(output_path: Path, entries: list[dict[str, Any]]) -> None:
    chunks = ["# Exportacion de registros", ""]
    for entry in entries:
        chunks.extend(
            [
                f"## {entry['event_date']} - {entry['title']}",
                "",
                f"- ID: {entry['id']}",
                f"- Tipo: {entry['type']}",
                f"- Ambitos: {', '.join(entry['scopes'])}",
                f"- Personas: {', '.join(entry['people']) if entry['people'] else '-'}",
                f"- Tags: {', '.join(entry['tags']) if entry['tags'] else '-'}",
                f"- Importancia: {entry['importance']}",
                "",
                entry["body"],
                "",
            ]
        )
        if entry["follow_ups"]:
            chunks.append("Seguimientos:")
            chunks.append("")
            chunks.extend(f"- {item}" for item in entry["follow_ups"])
            chunks.append("")
    output_path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import and export structured personal journal records.")
    parser.add_argument("--db", type=Path, default=Path("journal.sqlite3"), help="SQLite database path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create the SQLite database schema.")

    import_parser = subparsers.add_parser("import", help="Import a JSONL file.")
    import_parser.add_argument("input", type=Path)

    export_parser = subparsers.add_parser("export", help="Export stored entries.")
    export_parser.add_argument("--format", choices=["csv", "markdown", "json", "jsonl"], required=True)
    export_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "init":
        with connect(args.db) as conn:
            init_db(conn)
        print(f"initialized {args.db}")
        return 0
    if args.command == "import":
        return import_jsonl(args.db, args.input)
    if args.command == "export":
        export_entries(args.db, args.output, args.format)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
