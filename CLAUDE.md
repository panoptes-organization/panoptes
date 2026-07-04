# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Panoptes is a Flask web app that monitors Snakemake workflows in real time. It stores workflow/job state in SQLite and serves both a server-rendered UI and a JSON API. It is the `panoptes-ui` package on PyPI/bioconda.

## Commands

```bash
pip install '.[dev]'                 # editable-ish dev install with pytest/requests
pytest panoptes/tests -v             # unit tests + internal e2e (e2e auto-skips if deps missing)
pytest panoptes/tests/server_test.py::test_retried_job_is_not_duplicated   # a single test
panoptes                             # run the dev server (default 0.0.0.0:5000)
panoptes --ip 127.0.0.1 --port 5001  # override host/port
gunicorn --bind :5000 panoptes.app:app   # production WSGI entrypoint
```

- **Isolated DB:** set `PANOPTES_DB_URL` (e.g. `sqlite:///./scratch.db?check_same_thread=False`) before starting the server or running scripts, to avoid touching the default `.panoptes.db`. PostgreSQL is supported too (`postgresql+psycopg2://...`, driver via `pip install '.[postgres]'`); setting `PANOPTES_TEST_DB_URL` makes the test suite run against that URL instead of its throwaway SQLite file — CI uses this to test against a real PostgreSQL.
- **e2e tests** (`panoptes/tests/e2e_test.py`, marked `@pytest.mark.e2e`) spin up a real server subprocess and run Snakemake through the logger plugin. They auto-skip unless both `snakemake>=9` and `snakemake-logger-plugin-panoptes` are importable. Run explicitly with `pytest panoptes/tests/e2e_test.py -m e2e`.
- On macOS, port 5000 is often taken by the AirPlay Receiver; use another port.

## Architecture

**The integration boundary is the key thing to understand.** Snakemake 9 removed the old `--wms-monitor` flag. Monitoring now flows through a **separate** logger plugin repo, `snakemake-logger-plugin-panoptes`, which the user typically has cloned alongside this repo (`../snakemake-logger-plugin-panoptes`, example workflow at `../snakemake_example_workflow`). The plugin:
1. calls `GET /create_workflow` (optionally `?workflow_id=<stable-id>`) once to register a workflow, then
2. translates Snakemake `LogEvent`s into JSON and `POST`s them to `/update_workflow_status`.

Because event semantics are split across two repos, **changes to how events are produced/consumed usually require coordinated PRs in both**, released together.

**Event ingestion is the heart of the server.** `panoptes/server_utilities/db_queries.py::maintain_jobs(msg, wf_id)` is the central dispatcher: it parses the JSON message and mutates DB state based on the event `level` (`job_info`, `job_started`, `job_finished`, `job_error`, `progress`, `error`, `workflow_success`, `info`, `shellcmd`). It must **never raise on an unrecognized event** — unknown levels return `False` and are dropped so the plugin never crashes a running workflow.

**Workflow completion semantics** (subtle, and the source of several fixed bugs):
- A workflow is marked `Done` when a `progress` event reports `done == total`.
- With `snakemake --until`, Snakemake reports the *full-DAG* total while only a subset runs, so `done` never reaches `total`. The plugin therefore emits a `workflow_success` event at end-of-run; the server reconciles a still-`Running` workflow to `Done` using the actually-recorded job rows. Terminal states (`Done`/`Error`/`Cancelled`) are left untouched so a failed run is never resurrected.
- A `Running` workflow can't be deleted directly (`DELETE` returns 403); it must be cancelled first (`POST /api/workflow/<id>/cancel` → `Cancelled`).
- Re-registering a known `workflow_id` (`GET /create_workflow?workflow_id=...`) resets and reuses the entry **only if the previous run is in a finished state** (incl. `Stale`). A still-`Running` entry is protected the same way as for delete: the new run gets a fresh suffixed entry (`<id>-<8 hex chars>`) instead of wiping a possibly-live run's history. Ctrl+C/failed runs end as `Error` (terminal), so normal restarts reuse the id without extra steps.
- Every ingested event touches `workflows.updated_at`; the read paths flip `Running` workflows silent for more than `PANOPTES_STALE_HOURS` (default 48, `0` disables) to `Stale` — reversible: the next event revives them to `Running`. `Stale` (unlike `Running`) is deletable.

**Layers:**
- `panoptes/models.py` — SQLAlchemy models `Workflows`, `WorkflowJobs`, `WorkflowMessages`, plus their state-transition methods (`edit_workflow`, `mark_finished`, `set_error`, `set_cancelled`, `job_done`, `restart`, …). State changes live on the models; query/orchestration lives in `db_queries.py`.
- `panoptes/database.py` — binds the SQLAlchemy engine to `PANOPTES_DB_URL` **at import time**. Anything that needs an isolated DB (tests, scripts) must set the env var *before* importing `panoptes` — see `panoptes/tests/conftest.py`. There is no Alembic: columns added to existing tables must be bolted on in `_migrate()` (`create_all` only creates missing tables).
- `panoptes/routes/api.py` — the read/JSON + mutation API under `/api/...`, registered as a Flask blueprint. Also holds the template helpers registered as Jinja globals in `app.py` (`get_jobs`, `get_job`, `get_rule_progress`).
- `panoptes/app.py` — page routes (Jinja) and the two plugin-facing ingestion endpoints (`/create_workflow`, `/update_workflow_status`).
- `panoptes/static/src/*.html` — server-rendered templates extending `index.html` (a CoreUI/Bootstrap admin template). Frontend interactivity (delete/cancel/rename via AJAX to the API, sidebar toggle, per-table status filters, live updates that poll the JSON API and reload on change) lives in `panoptes/static/src/js/src/init.js`. Note CoreUI's own JS is **not** bundled, so behaviors like the sidebar hamburger are wired manually in `init.js`.

## Sibling repos

All three are under the `panoptes-organization` GitHub org and are typically cloned next to each other (`~/Desktop/` in this environment):

| Path | Repo | Default branch | Role |
| --- | --- | --- | --- |
| `.` (`../panoptes`) | `panoptes` | `master` | this server (`panoptes-ui`) |
| `../snakemake-logger-plugin-panoptes` | `snakemake-logger-plugin-panoptes` | `main` | Snakemake 9 logger plugin that emits events to this server; `src/.../log_handler.py` is where `LogEvent`s are translated |
| `../snakemake_example_workflow` | `snakemake_example_workflow` | — | a small conda-based reference pipeline wired up with `--logger panoptes`, used for manual/e2e verification (`bash run_local.sh`) |

When changing event ingestion, check whether the plugin's `log_handler.py` also needs updating, and release the two together.

## Conventions / gotchas

- **Version is single-sourced in `panoptes/_version.py`** and read (via `exec`, not import) by `setup.py`; it's also exposed as `panoptes.__version__` and shown on the About page. Bump it per change.
- `WorkflowJobs.get_job_json()` uses `eval()` on the stored `input`/`output`/`log`/`wildcards` fields, which are persisted with `repr()` at ingestion time — keep those two sides in sync.
- Contribution flow (see `CONTRIBUTING.md`): branch off `master`, add tests, open a PR after discussing via an issue; add yourself to `contributors.md`.
