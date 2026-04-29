from __future__ import annotations

import argparse
import csv
import shutil
import sqlite3
import subprocess
import zipfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path, help="Path to .zip/.apkg/.colpkg")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output CSV path. Defaults to <archive stem>.csv beside the archive.",
    )
    parser.add_argument(
        "--extract-dir",
        type=Path,
        help="Extraction directory. Defaults to <archive stem>_extracted beside the archive.",
    )
    return parser.parse_args()


def extract_archive(archive: Path, extract_dir: Path) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(extract_dir)


def ensure_sqlite_db(extract_dir: Path) -> Path:
    anki21b = extract_dir / "collection.anki21b"
    anki2 = extract_dir / "collection.anki2"
    sqlite_path = extract_dir / "collection.sqlite"

    if anki21b.exists():
        if shutil.which("zstd") is None:
            raise SystemExit("zstd command is required to read collection.anki21b")
        subprocess.run(
            ["zstd", "-d", "-q", "-f", str(anki21b), "-o", str(sqlite_path)],
            check=True,
        )
        return sqlite_path

    if anki2.exists():
        return anki2

    raise SystemExit("collection.anki21b or collection.anki2 was not found in the archive")


def get_field_names(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    cur.execute("select distinct mid from notes order by mid")
    mids = [row[0] for row in cur.fetchall()]

    cur.execute("select ntid, ord, name from fields order by ntid, ord")
    fields_by_type: dict[int, list[str]] = {}
    for ntid, ord_, name in cur.fetchall():
        fields_by_type.setdefault(ntid, [])
        fields = fields_by_type[ntid]
        while len(fields) <= ord_:
            fields.append(f"field_{len(fields) + 1}")
        fields[ord_] = name

    if len(mids) == 1 and mids[0] in fields_by_type:
        return fields_by_type[mids[0]]

    max_fields = cur.execute(
        """
        select max(
            length(flds) - length(replace(flds, char(31), "")) + 1
        ) from notes
        """
    ).fetchone()[0]
    return [f"field_{index}" for index in range(1, (max_fields or 0) + 1)]


def export_csv(db_path: Path, output_path: Path) -> int:
    conn = sqlite3.connect(db_path)
    try:
        field_names = get_field_names(conn)
        header = ["note_id", "guid", "notetype_id", "tags", *field_names]

        cur = conn.cursor()
        cur.execute("select id, guid, mid, tags, flds from notes order by id")

        row_count = 0
        with output_path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for note_id, guid, mid, tags, flds in cur.fetchall():
                fields = flds.split("\x1f")
                if len(fields) < len(field_names):
                    fields.extend([""] * (len(field_names) - len(fields)))
                writer.writerow([note_id, guid, mid, tags, *fields])
                row_count += 1
        return row_count
    finally:
        conn.close()


def main() -> None:
    args = parse_args()
    archive = args.archive.resolve()
    extract_dir = (
        args.extract_dir.resolve()
        if args.extract_dir
        else archive.with_name(f"{archive.stem}_extracted")
    )
    output_path = (
        args.output.resolve()
        if args.output
        else archive.with_suffix(".csv")
    )

    extract_archive(archive, extract_dir)
    db_path = ensure_sqlite_db(extract_dir)
    row_count = export_csv(db_path, output_path)
    print(f"wrote {row_count} rows to {output_path}")


if __name__ == "__main__":
    main()
