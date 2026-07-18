# AntiVirus-Map

AntiVirus-Map is a simple map-based project that can be explored by walking around inside it and used for testing movement, layout, and interaction in the environment.

## What this project is

This repository contains the Godot game project files under GoDotGames, along with supporting scripts and tests so the project can be opened, inspected, and run from a source-based workspace.

The main game source and project assets live in the GoDotGames folder.

## How it works

The project is centered around a map that you can run and explore. The main purpose is to walk through the environment, test how it feels to move around inside it, and use it as a basic testing space for the map experience.

## How to use it

1. Clone the repository.
2. If a single `AntiVirus0.1.0.exe` file is present, open it from the repository root and run it.
3. If the executable has been split into parts (for example `AntiVirus0.1.0.exe.part01`, `AntiVirus0.1.0.exe.part02`, ...), join the parts to produce the real executable before running.

Joining examples:

- On Linux / macOS:

```bash
cd /path/to/repo
cat AntiVirus0.1.0.exe.part* > AntiVirus0.1.0.exe
```

- On Windows (cmd.exe):

```cmd
copy /b AntiVirus0.1.0.exe.part01+AntiVirus0.1.0.exe.part02 AntiVirus0.1.0.exe
```

After assembling the executable you can run it directly, or use the included launcher which will try to auto-assemble split parts if needed:

```bash
python3 src/launcher.py
```

The launcher will attempt to locate `AntiVirus0.1.0.exe`. If it only finds split parts it will concatenate them into `AntiVirus0.1.0.exe` and then launch the resulting file.

Automated assembly script

If you'd prefer a helper script that assembles parts for you, there's a small utility in `scripts/assemble_release.py`:

```bash
python3 scripts/assemble_release.py --repo .
```

This will create `AntiVirus0.1.0.exe` in the repository root if it can find files matching `AntiVirus0.1.0.exe.part*`.

## Open source notes

The repository is now organized as an open-source project with source files, tests, and contribution guidance so others can inspect or improve it.

## Acknowledgements

This project was helped by Quaternius as well.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
