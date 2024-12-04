import subprocess
import sys

from bimorph_adaptive_plan import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "bimorph_adaptive_plan", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
