#!/usr/bin/env python3
"""Small cross-platform launcher for the bundled AntiVirus executable."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import List

EXE_NAME = "AntiVirus0.1.0.exe"
LEGACY_PAYLOAD_NAME = "AntiVirus0.1.0.exen"
PART_PATTERN = "AntiVirus0.1.0.exe.part*"


def _assemble_parts(repo_root: Path, target: Path) -> Path:
    parts = sorted(repo_root.glob(PART_PATTERN))
    if not parts:
        raise FileNotFoundError("No split executable parts were found.")

    try:
        with target.open("wb") as out_f:
            for part in parts:
                with part.open("rb") as in_f:
                    shutil.copyfileobj(in_f, out_f)
        return target
    except Exception:
        if target.exists():
            try:
                target.unlink()
            except Exception:
                pass
        raise


def _extract_zip_archive(archive_path: Path, target: Path) -> Path:
    with zipfile.ZipFile(archive_path) as archive:
        candidates = [
            member for member in archive.namelist()
            if not member.endswith("/") and member.lower().endswith(".exe")
        ]
        if not candidates:
            raise FileNotFoundError(f"No executable found inside {archive_path}")

        chosen = sorted(candidates, key=lambda item: item.lower())[0]
        with archive.open(chosen) as source, target.open("wb") as destination:
            shutil.copyfileobj(source, destination)
        return target


def resolve_executable(repo_root: Path) -> Path:
    """Return the packaged executable path if it exists."""
    final_exe = repo_root / EXE_NAME

    if final_exe.exists():
        return final_exe

    legacy_payload = repo_root / LEGACY_PAYLOAD_NAME
    if legacy_payload.exists():
        with legacy_payload.open("rb") as source, final_exe.open("wb") as destination:
            shutil.copyfileobj(source, destination)
        return final_exe

    for archive_path in sorted(repo_root.glob("*.zip")):
        try:
            return _extract_zip_archive(archive_path, final_exe)
        except Exception:
            if final_exe.exists():
                try:
                    final_exe.unlink()
                except Exception:
                    pass
            continue

    try:
        return _assemble_parts(repo_root, final_exe)
    except FileNotFoundError:
        pass

    raise FileNotFoundError(
        "Unable to find the bundled AntiVirus executable in the repository. "
        "Looked for an .exe, a legacy .exen payload, a .zip archive, or split .part files. "
        "If you distributed the release as split parts, run `scripts/assemble_release.py` "
        "to assemble or create a .zip archive before launching."
    )


def build_launch_command(repo_root: Path, dry_run: bool = False) -> List[str]:
    """Build the command used to launch the bundled executable."""
    executable = resolve_executable(repo_root)
    if dry_run:
        return [str(executable)]
    return [str(executable)]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    try:
        executable = resolve_executable(repo_root)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Launching {executable}")
    if os.name == "nt":
        os.startfile(str(executable))  # type: ignore[attr-defined]
    else:
        if shutil.which("wine"):
            subprocess.run(["wine", str(executable)], check=False)
        else:
            subprocess.run([str(executable)], check=False)
    return 0


if __name__ == "__main__":
    main()
