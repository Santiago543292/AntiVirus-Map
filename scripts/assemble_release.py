#!/usr/bin/env python3
"""Helper to assemble split executable parts into a single file.

Usage:
  python3 scripts/assemble_release.py --repo /path/to/repo

The script can concatenate files matching `AntiVirus0.1.0.exe.part*` into
`AntiVirus0.1.0.exe`, and can also package a discovered executable or legacy
payload into a ZIP archive for easier distribution.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Optional, List


def assemble(repo_root: Path, target_name: str = "AntiVirus0.1.0.exe", pattern: str = "AntiVirus0.1.0.exe.part*", archive_name: Optional[str] = None) -> int:
    repo_root = Path(repo_root)
    target = repo_root / target_name

    if target.exists():
        print(f"{target} already exists; skipping assembly.")
    else:
        parts = sorted(repo_root.glob(pattern))
        if not parts:
            print(f"No parts matching '{pattern}' found in {repo_root}", file=sys.stderr)
            return 2

        try:
            with target.open("wb") as out_f:
                for part in parts:
                    with part.open("rb") as in_f:
                        shutil.copyfileobj(in_f, out_f)

            try:
                target.chmod(target.stat().st_mode | 0o111)
            except Exception:
                pass

            print(f"Assembled {target} from {len(parts)} part(s).")
        except Exception as exc:
            if target.exists():
                try:
                    target.unlink()
                except Exception:
                    pass
            print("Assembly failed:", exc, file=sys.stderr)
            return 1

    if archive_name:
        archive_path = repo_root / archive_name
        if archive_path.exists():
            print(f"{archive_path} already exists; skipping archive creation.")
        else:
            try:
                with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    archive.write(target, target.name)
                print(f"Created {archive_path} from {target}.")
            except Exception as exc:
                print("Archive creation failed:", exc, file=sys.stderr)
                return 1

    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Assemble split executable parts into a single file")
    parser.add_argument("--repo", default=".", help="Path to repository root")
    parser.add_argument("--target", default="AntiVirus0.1.0.exe", help="Output executable name")
    parser.add_argument("--pattern", default="AntiVirus0.1.0.exe.part*", help="Glob pattern for parts")
    parser.add_argument("--archive", default=None, help="Optional .zip archive name to create from the assembled executable")
    args = parser.parse_args(argv)
    try:
        return assemble(Path(args.repo), args.target, args.pattern, args.archive)
    except Exception as exc:
        print("Error during assembly:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
