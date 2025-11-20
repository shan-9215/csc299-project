import subprocess
import sys
from pathlib import Path
import json


def run(cmd, cwd, check=False):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def test_add_list_done(tmp_path):
    repo = tmp_path
    # run module from project root so `-m src.cli` can import the `src` package
    p = repo / "tasks.json"
    project_root = Path(__file__).parents[2]
    # add
    r = run([sys.executable, "-m", "src.cli", "add", "Hello", "--file", str(p)], cwd=project_root)
    assert r.returncode == 0
    # list
    r2 = run([sys.executable, "-m", "src.cli", "list", "--json", "--file", str(p)], cwd=project_root)
    assert r2.returncode == 0
    data = json.loads(r2.stdout)
    assert isinstance(data, list)
    assert data[0]["description"] == "Hello"
    # done
    r3 = run([sys.executable, "-m", "src.cli", "done", "1", "--file", str(p)], cwd=project_root)
    assert r3.returncode == 0
    r4 = run([sys.executable, "-m", "src.cli", "list", "--json", "--file", str(p)], cwd=project_root)
    data2 = json.loads(r4.stdout)
    assert data2[0]["completed"] is True
