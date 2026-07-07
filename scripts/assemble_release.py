#!/usr/bin/env python3
"""Helper to assemble split executable parts into a single file.

Usage:
  python3 scripts/assemble_release.py --repo /path/to/repo

The script concatenates files matching `AntiVirus0.1.0.exe.part*` into
`AntiVirus0.1.0.exe` in the repository root.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def assemble(repo_root: Path, target_name: str = "AntiVirus0.1.0.exe", pattern: str = "AntiVirus0.1.0.exe.part*") -> int:
    repo_root = Path(repo_root)
    target = repo_root / target_name

    if target.exists():
        print(f"{target} already exists; skipping assembly.")
        return 0

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
        return 0
    except Exception as exc:
        if target.exists():
            try:
                target.unlink()
            except Exception:
                pass
        print("Assembly failed:", exc, file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assemble split executable parts into a single file")
    parser.add_argument("--repo", default=".", help="Path to repository root")
    parser.add_argument("--target", default="AntiVirus0.1.0.exe", help="Output executable name")
    parser.add_argument("--pattern", default="AntiVirus0.1.0.exe.part*", help="Glob pattern for parts")
    args = parser.parse_args(argv)
    return assemble(Path(args.repo), args.target, args.pattern)


if __name__ == "__main__":
    raise SystemExit(main())
