#!/usr/bin/env python3
"""Small cross-platform launcher for the bundled AntiVirus executable."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def resolve_executable(repo_root: Path) -> Path:
    """Return the packaged executable path if it exists."""
    candidates = [
        repo_root / "AntiVirus0.1.0.exe",
        repo_root / "AntiVirus0.1.0.exe.part01",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Unable to find the bundled AntiVirus executable in the repository.")


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
