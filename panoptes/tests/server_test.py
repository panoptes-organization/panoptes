"""Unit tests for the panoptes Flask server.

These exercise the API and the ``/update_workflow_status`` ingestion path with
the exact payload shapes produced by ``snakemake-logger-plugin-panoptes`` (the
Snakemake 9 replacement for the legacy ``--wms-monitor`` flow).
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict


def _post_event(client, workflow_id: int, message: Dict[str, Any]):
    """Mirror what the logger plugin sends to /update_workflow_status."""
    return client.post(
        "/update_workflow_status",
        data={
            "msg": json.dumps(message),
            "timestamp": time.asctime(),
            "id": workflow_id,
        },
    )


# --------------------------------------------------------------------------- #
# Read-only API
# --------------------------------------------------------------------------- #


def test_service_info_reports_running(client):
    resp = client.get("/api/service-info")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "running"}


def test_about_page_shows_version(client):
    import panoptes

    resp = client.get("/about")
    assert resp.status_code == 200
    assert panoptes.__version__ in resp.get_data(as_text=True)


def test_workflows_is_empty_on_a_fresh_db(client):
    resp = client.get("/api/workflows")
    assert resp.status_code == 200
    assert resp.get_json() == {"count": 0, "workflows": []}


def test_unknown_workflow_is_404(client):
    assert client.get("/api/workflow/999").status_code == 404
    assert client.get("/api/workflow/999/jobs").status_code == 404
    assert client.get("/api/workflow/999/job/1").status_code == 404


# --------------------------------------------------------------------------- #
# Workflow registration (plugin -> /create_workflow)
# --------------------------------------------------------------------------- #


def test_create_workflow_returns_id_and_uuid_name(client):
    resp = client.get("/create_workflow")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert isinstance(payload["id"], int)
    assert isinstance(payload["name"], str) and len(payload["name"]) == 36
    assert payload["status"] == "Running"
    assert payload["jobs_done"] == 0
    assert payload["jobs_total"] == 1


def test_create_workflow_with_workflow_id_uses_it(client):
    payload = client.get("/create_workflow?workflow_id=my-run").get_json()
    assert payload["name"] == "my-run"
    assert payload["status"] == "Running"


def test_create_workflow_same_workflow_id_reuses_the_workflow(client):
    first = client.get("/create_workflow?workflow_id=nightly").get_json()
    second = client.get("/create_workflow?workflow_id=nightly").get_json()
    assert first["id"] == second["id"]
    # Only one workflow row should exist for that id.
    assert client.get("/api/workflows").get_json()["count"] == 1


def test_create_workflow_workflow_id_reuse_resets_previous_run(client):
    wf_id = client.get("/create_workflow?workflow_id=cohort").get_json()["id"]
    _post_event(client, wf_id, {
        "level": "job_info", "jobid": 1, "name": "step",
        "input": [], "output": [],
    })
    _post_event(client, wf_id, {"level": "progress", "done": 2, "total": 5})
    assert client.get(f"/api/workflow/{wf_id}/jobs").get_json()["count"] == 1

    # Re-running with the same workflow_id reuses the id but clears the prior run.
    reused = client.get("/create_workflow?workflow_id=cohort").get_json()
    assert reused["id"] == wf_id
    assert reused["status"] == "Running"
    assert reused["jobs_done"] == 0
    assert client.get(f"/api/workflow/{wf_id}/jobs").get_json()["count"] == 0


def test_create_workflow_legacy_name_param_is_still_accepted(client):
    # Plugins <= 0.2.1 send ?name=; it must map to the same workflow as ?workflow_id=.
    first = client.get("/create_workflow?name=legacy").get_json()
    second = client.get("/create_workflow?workflow_id=legacy").get_json()
    assert first["name"] == "legacy"
    assert first["id"] == second["id"]
    assert client.get("/api/workflows").get_json()["count"] == 1


# --------------------------------------------------------------------------- #
# Ingestion: same payloads the Snakemake 9 plugin emits
# --------------------------------------------------------------------------- #


def test_job_info_then_job_finished_marks_job_done(client):
    wf = client.get("/create_workflow").get_json()
    wf_id = wf["id"]

    job_info = {
        "level": "job_info",
        "jobid": 1,
        "name": "bwa_map",
        "msg": None,
        "input": ["samples/a.fq"],
        "output": ["a.bam"],
        "log": ["a.log"],
        "wildcards": {"sample": "a"},
        "is_checkpoint": False,
        "shellcmd": "bwa mem ...",
    }
    assert _post_event(client, wf_id, job_info).status_code == 200
    assert _post_event(client, wf_id, {"level": "job_started", "jobs": [1]}).status_code == 200
    assert _post_event(client, wf_id, {"level": "job_finished", "jobid": 1}).status_code == 200

    jobs = client.get(f"/api/workflow/{wf_id}/jobs").get_json()
    assert jobs["count"] == 1
    job = jobs["jobs"][0]
    assert job["name"] == "bwa_map"
    assert job["status"] == "Done"
    assert job["input"] == ["samples/a.fq"]
    assert job["wildcards"] == {"sample": "a"}
    assert job["shell_command"] == "bwa mem ..."


def test_progress_event_updates_workflow_counts(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    assert _post_event(client, wf_id, {"level": "progress", "done": 3, "total": 10}).status_code == 200

    workflow = client.get(f"/api/workflow/{wf_id}").get_json()["workflow"]
    assert workflow["jobs_done"] == 3
    assert workflow["jobs_total"] == 10
    assert workflow["status"] == "Running"


def test_progress_completion_flips_status_to_done(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    _post_event(client, wf_id, {"level": "progress", "done": 2, "total": 2})

    workflow = client.get(f"/api/workflow/{wf_id}").get_json()["workflow"]
    assert workflow["status"] == "Done"
    assert workflow["completed_at"] is not None


def test_job_error_flips_workflow_to_error(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    _post_event(
        client,
        wf_id,
        {
            "level": "job_info",
            "jobid": 2,
            "name": "samtools_sort",
            "input": ["a.bam"],
            "output": ["a.sorted.bam"],
            "log": ["sort.log"],
            "wildcards": {"sample": "a"},
            "is_checkpoint": False,
        },
    )
    _post_event(client, wf_id, {"level": "job_error", "jobid": 2})

    workflow = client.get(f"/api/workflow/{wf_id}").get_json()["workflow"]
    assert workflow["status"] == "Error"
    jobs = client.get(f"/api/workflow/{wf_id}/jobs").get_json()
    assert jobs["jobs"][0]["status"] == "Error"


def test_retried_job_is_not_duplicated(client):
    # Snakemake re-submits a failed job (e.g. --retries 1) by re-emitting a
    # job_info event with the same jobid. The job must be updated in place, not
    # duplicated. See https://github.com/panoptes-organization/panoptes/issues/188
    wf_id = client.get("/create_workflow").get_json()["id"]

    job_info = {
        "level": "job_info",
        "jobid": 7,
        "name": "flaky_rule",
        "input": ["a.in"],
        "output": ["a.out"],
        "log": ["a.log"],
        "wildcards": {"sample": "a"},
        "is_checkpoint": False,
    }

    # First attempt fails.
    assert _post_event(client, wf_id, job_info).status_code == 200
    assert _post_event(client, wf_id, {"level": "job_error", "jobid": 7}).status_code == 200

    # Retry: same jobid is re-submitted and succeeds.
    assert _post_event(client, wf_id, job_info).status_code == 200
    assert _post_event(client, wf_id, {"level": "job_finished", "jobid": 7}).status_code == 200

    jobs = client.get(f"/api/workflow/{wf_id}/jobs").get_json()
    assert jobs["count"] == 1
    job = jobs["jobs"][0]
    assert job["jobid"] == 7
    assert job["status"] == "Done"


def test_shellcmd_message_is_stored_without_crashing(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    resp = _post_event(
        client,
        wf_id,
        {"level": "shellcmd", "jobid": 1, "msg": "bash -c 'echo hi'"},
    )
    assert resp.status_code == 200


def test_unknown_event_level_is_accepted_silently(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    # RULEGRAPH / RUN_INFO / DEBUG_DAG etc. — anything we don't map should be a
    # no-op rather than a 5xx.
    resp = _post_event(client, wf_id, {"level": "rulegraph", "rulegraph": {}})
    assert resp.status_code == 200


def test_malformed_msg_returns_400(client):
    # Missing required `msg` field — schema validation should reject it cleanly.
    resp = client.post(
        "/update_workflow_status",
        data={"timestamp": time.asctime(), "id": 1},
    )
    assert resp.status_code == 400
    body = resp.get_json()
    assert "errors" in body


def test_update_status_also_accepts_json_body(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    resp = client.post(
        "/update_workflow_status",
        json={
            "msg": json.dumps({"level": "progress", "done": 1, "total": 4}),
            "timestamp": time.asctime(),
            "id": wf_id,
        },
    )
    assert resp.status_code == 200
    workflow = client.get(f"/api/workflow/{wf_id}").get_json()["workflow"]
    assert workflow["jobs_done"] == 1
    assert workflow["jobs_total"] == 4


# --------------------------------------------------------------------------- #
# Mutations
# --------------------------------------------------------------------------- #


def test_rename_and_delete_workflow(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    # Force the workflow out of the "Running" state so delete is permitted.
    _post_event(client, wf_id, {"level": "progress", "done": 1, "total": 1})

    rename = client.put(f"/api/workflow/{wf_id}", json={"name": "my-renamed-wf"})
    assert rename.status_code == 200

    deleted = client.delete(f"/api/workflow/{wf_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/workflow/{wf_id}").status_code == 404


def test_cannot_delete_running_workflow(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    resp = client.delete(f"/api/workflow/{wf_id}")
    assert resp.status_code == 403


def test_cancel_then_delete_running_workflow(client):
    # A stuck "Running" workflow (e.g. a dry run or a killed process) can't be
    # deleted directly, but can be cancelled and then deleted. See issue #177.
    wf_id = client.get("/create_workflow").get_json()["id"]

    assert client.delete(f"/api/workflow/{wf_id}").status_code == 403

    cancelled = client.post(f"/api/workflow/{wf_id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.get_json()["workflow"]["status"] == "Cancelled"

    assert client.delete(f"/api/workflow/{wf_id}").status_code == 204
    assert client.get(f"/api/workflow/{wf_id}").status_code == 404


def test_cancel_unknown_workflow_is_404(client):
    assert client.post("/api/workflow/999/cancel").status_code == 404


def test_clean_up_whole_db(client):
    wf_id = client.get("/create_workflow").get_json()["id"]
    _post_event(client, wf_id, {"level": "progress", "done": 1, "total": 1})

    resp = client.delete("/api/workflows/all")
    assert resp.status_code == 200
    assert resp.get_json()["msg"] == "Database clean up is complete"
    assert client.get("/api/workflows").get_json() == {"count": 0, "workflows": []}
