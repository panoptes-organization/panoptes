"""End-to-end Snakemake 9 -> panoptes integration test.

Spins up the panoptes Flask server in a subprocess (against an isolated SQLite
DB), then runs a tiny Snakefile through ``snakemake --logger panoptes`` and
verifies the workflow + jobs were recorded via the read API.

Skipped automatically when either ``snakemake`` or the logger plugin isn't
importable, since both are runtime requirements that aren't part of the
panoptes server's install. Run explicitly with::

    pytest panoptes/tests/e2e_test.py -m e2e
"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
from importlib.util import find_spec
from pathlib import Path

import pytest
import requests

pytestmark = pytest.mark.e2e

_FIXTURE_SNAKEFILE = Path(__file__).parent / "fixtures" / "Snakefile"


def _have(mod: str) -> bool:
    try:
        return find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


_PLUGIN_AVAILABLE = _have("snakemake") and _have("snakemake_logger_plugin_panoptes")


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for(url: str, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(0.2)
    raise RuntimeError(f"server did not become ready at {url} within {timeout}s")


@pytest.fixture
def panoptes_server(tmp_path):
    """Start a panoptes server with an isolated DB on a free port."""
    port = _free_port()
    db_path = tmp_path / "e2e-panoptes.db"
    env = {
        **os.environ,
        "PANOPTES_DB_URL": f"sqlite:///{db_path}?check_same_thread=False",
    }
    # Reuse the conftest tmp DB if anything has touched it — we don't want
    # cross-contamination from the unit suite.
    env.pop("WERKZEUG_RUN_MAIN", None)

    log_path = tmp_path / "panoptes.log"
    with log_path.open("w") as log:
        proc = subprocess.Popen(
            [sys.executable, "-m", "panoptes.panoptes",
             "--ip", "127.0.0.1", "--port", str(port)],
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    try:
        _wait_for(f"http://127.0.0.1:{port}/api/service-info")
        yield f"http://127.0.0.1:{port}", log_path
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.skipif(
    not _PLUGIN_AVAILABLE,
    reason="snakemake and snakemake-logger-plugin-panoptes must be installed for e2e",
)
def test_snakemake_run_populates_panoptes(panoptes_server, tmp_path):
    base_url, log_path = panoptes_server

    workdir = tmp_path / "workflow"
    workdir.mkdir()
    shutil.copy(_FIXTURE_SNAKEFILE, workdir / "Snakefile")

    # Invoke snakemake via the active interpreter so the test works whether or
    # not the venv's bin/ is on PATH.
    result = subprocess.run(
        [
            sys.executable, "-m", "snakemake",
            "--snakefile", "Snakefile",
            "--cores", "1",
            "--logger", "panoptes",
            "--logger-panoptes-address", base_url,
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"snakemake exited {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}\n"
        f"--- panoptes log ---\n{log_path.read_text()}"
    )

    # Allow the plugin a brief moment to drain any in-flight events.
    time.sleep(0.5)

    workflows = requests.get(f"{base_url}/api/workflows").json()
    assert workflows["count"] == 1, workflows
    wf = workflows["workflows"][0]
    assert wf["status"] in {"Done", "Running"}, wf
    # The fixture Snakefile schedules exactly four jobs (make_input x2,
    # finalize x2). PROGRESS should reflect that.
    assert wf["jobs_total"] >= 4

    jobs = requests.get(f"{base_url}/api/workflow/{wf['id']}/jobs").json()
    assert jobs["count"] >= 4, jobs
    rule_names = {j["name"] for j in jobs["jobs"]}
    assert {"make_input", "finalize"}.issubset(rule_names), rule_names
    # If the workflow finished, every job should be marked Done.
    if wf["status"] == "Done":
        assert all(j["status"] == "Done" for j in jobs["jobs"]), jobs
