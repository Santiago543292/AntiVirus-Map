#!/usr/bin/env python3
"""Create a distributable ZIP containing AntiVirus0.1.0.exe.

This script will look for, in order:
 - AntiVirus0.1.0.exe (use it directly)
 - AntiVirus0.1.0.exen (treat as payload and include as the .exe)
 - split parts matching AntiVirus0.1.0.exe.part* (assemble temporarily and include)

It writes a zip file named `AntiVirus0.1.0.zip` in the repository root.
"""
from __future__ import annotations

import shutil
import sys
import zipfile
import tempfile
from pathlib import Path
from typing import Optional

from scripts.assemble_release import assemble

ZIP_NAME = "AntiVirus0.1.0.zip"
EXE_NAME = "AntiVirus0.1.0.exe"
LEGACY_PAYLOAD = "AntiVirus0.1.0.exen"
PART_PATTERN = "AntiVirus0.1.0.exe.part*"


def create_zip_from_path(source_path: Path, dest_zip: Path) -> None:
    with zipfile.ZipFile(dest_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(source_path, EXE_NAME)


def create_zip_from_payload(payload_path: Path, dest_zip: Path) -> None:
    with zipfile.ZipFile(dest_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        with payload_path.open("rb") as src:
            data = src.read()
        archive.writestr(EXE_NAME, data)


def main(argv: Optional[list[str]] = None) -> int:
    repo_root = Path((argv and argv[0]) or ".").resolve()
    repo_root = Path(repo_root)
    dest_zip = repo_root / ZIP_NAME

    if dest_zip.exists():
        print(f"{dest_zip} already exists; skipping.")
        return 0

    exe_path = repo_root / EXE_NAME
    if exe_path.exists():
        create_zip_from_path(exe_path, dest_zip)
        print(f"Created {dest_zip} from {exe_path}")
        return 0

    payload = repo_root / LEGACY_PAYLOAD
    if payload.exists():
        create_zip_from_payload(payload, dest_zip)
        print(f"Created {dest_zip} from legacy payload {payload}")
        return 0

    # Try to assemble parts into a temporary file and zip that
    parts = list(repo_root.glob(PART_PATTERN))
    if parts:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / EXE_NAME
            try:
                rc = assemble(repo_root, target_name=EXE_NAME, pattern=PART_PATTERN, archive_name=None)
            except Exception as exc:
                print("Assembly failed:", exc, file=sys.stderr)
                return 1
            # If assemble returned non-zero it already printed, but assemble returns int; however when invoked here it performs assembly
            # The assemble function in scripts returns 0 on success and creates the target in repo_root.
            assembled = repo_root / EXE_NAME
            if assembled.exists():
                create_zip_from_path(assembled, dest_zip)
                print(f"Created {dest_zip} from assembled parts")
                return 0

    print("No executable, legacy payload, or split parts found to package.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
