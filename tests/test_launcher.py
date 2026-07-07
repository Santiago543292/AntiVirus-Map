import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "src" / "launcher.py"

spec = importlib.util.spec_from_file_location("launcher", MODULE_PATH)
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def test_resolve_executable_finds_repo_binary(self):
        self.assertEqual(
            launcher.resolve_executable(REPO_ROOT),
            REPO_ROOT / "AntiVirus0.1.0.exe",
        )

    def test_build_launch_command_is_dry_run_safe(self):
        command = launcher.build_launch_command(REPO_ROOT, dry_run=True)
        self.assertEqual(command, [str(REPO_ROOT / "AntiVirus0.1.0.exe")])


if __name__ == "__main__":
    unittest.main()
