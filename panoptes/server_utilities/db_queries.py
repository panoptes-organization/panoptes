from panoptes.database import db_session
from panoptes.models import Workflows, WorkflowMessages, WorkflowJobs

import json


# Events emitted by the Snakemake 9 logger plugin
# (snakemake-logger-plugin-panoptes) that the server understands. Anything else
# is ignored without raising, so the plugin never causes a workflow to crash.
_KNOWN_LEVELS = {
    "job_info",
    "job_started",
    "job_finished",
    "job_error",
    "info",
    "progress",
    "error",
    "workflow_success",
    "shellcmd",
    "",
}


def get_db_workflows():
    return Workflows.query.all()


def get_db_workflows_by_id(workflow_id):
    return Workflows.query.filter(Workflows.id == workflow_id).first()


def get_db_workflows_by_status(workflow_id):
    return (db_session.query(Workflows.status).filter(Workflows.id == workflow_id).first())[0]


def get_db_workflow_by_name(name):
    return Workflows.query.filter(Workflows.name == name).first()


def get_db_table_is_empty(table_name):
    if(table_name == 'User'):
        result = db_session.query(User.id).all()
    elif (table_name == 'Workflows'):
        result = db_session.query(Workflows.id).all()
    elif (table_name == 'WorkflowJobs'):
        result = db_session.query(WorkflowJobs.id).all()
    elif (table_name == 'WorkflowMessages'):
        result = db_session.query(WorkflowMessages.id).all()
    if len(result) <= 0:
        return True
    else:
        return False
    return


def maintain_jobs(msg, wf_id):

    # The message should be a json dump
    msg_json = json.loads(msg)
    level = msg_json.get("level", "")

    if "jobid" in msg_json and msg_json.get("jobid") is not None:
        if level == 'job_info':
            job_fields = (
                msg_json.get('msg'),
                msg_json.get('name', ''),
                repr(msg_json.get('input', [])),
                repr(msg_json.get('output', [])),
                repr(msg_json.get('log', [])),
                repr(msg_json.get('wildcards', {})),
                bool(msg_json.get('is_checkpoint', False)),
                msg_json.get('shellcmd'),
            )
            # A job_info event may arrive for a jobid that already exists when
            # Snakemake re-submits a failed job (e.g. via --retries). Reuse the
            # existing row in that case so the job is not duplicated.
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            if job is not None:
                job.restart(*job_fields)
            else:
                job = WorkflowJobs(msg_json['jobid'], wf_id, *job_fields)
                db_session.add(job)
            db_session.commit()
            return True

        if level == 'job_finished':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            if job is not None:
                job.job_done()
                db_session.commit()
            return True

        if level == 'job_error':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            if job is not None:
                job.job_error()
                db_session.commit()
            wf = Workflows.query.filter(Workflows.id == wf_id).first()
            if wf is not None:
                wf.set_error()
                db_session.commit()
            return True

    if level == 'job_started':
        # Snakemake 9 fires JOB_STARTED with a list of job ids when execution
        # actually begins. Jobs are already created at JOB_INFO time with
        # status="Running", so nothing extra to persist here.
        return True

    if level == 'info':
        if msg_json.get('msg') == 'Nothing to be done.':
            wf = Workflows.query.filter(Workflows.id == wf_id).first()
            if wf is not None:
                wf.set_not_executed()
                db_session.commit()
            return True
        return True

    if level == 'progress':
        wf = Workflows.query.filter(Workflows.id == wf_id).first()
        if wf is not None:
            wf.edit_workflow(msg_json.get('done', 0), msg_json.get('total', 0))
            db_session.commit()
        return True

    if level == 'error':
        wf = Workflows.query.filter(Workflows.id == wf_id).first()
        if wf is not None:
            wf.set_error()
            db_session.commit()
        return True

    if level == 'workflow_success':
        # The plugin sends this when a run finishes without error. Only reconcile
        # workflows still stuck as "Running": that is the `snakemake --until`
        # case, where Snakemake reports the full DAG total so done never reaches
        # total. Use the jobs we actually recorded as the real counts. Workflows
        # already marked Done/Error/etc. are left untouched.
        wf = Workflows.query.filter(Workflows.id == wf_id).first()
        if wf is not None and wf.status == 'Running':
            total = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id).count()
            done = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.status == 'Done').count()
            wf.mark_finished(done, total)
            db_session.commit()
        return True

    if level in ('shellcmd', ''):
        w = WorkflowMessages(msg, wf_id=wf_id)
        db_session.add(w)
        db_session.commit()
        return True

    # Unknown / not-yet-mapped LogEvent — just drop it so the workflow keeps
    # running.
    return False


def get_db_jobs(workflow_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id)


def get_db_job_by_id(workflow_id, job_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id).filter(WorkflowJobs.jobid == job_id).first()


def cancel_db_wf(workflow_id):
    """Mark a workflow as Cancelled so it can be deleted. Snakemake dry runs and
    workflows whose process was killed get stuck as "Running"; cancelling gives
    the user an explicit way to move them out of that state. See issues #177/#99."""
    try:
        wf = Workflows.query.filter(Workflows.id == workflow_id).first()
        if wf is None:
            return None
        wf.set_cancelled()
        db_session.commit()
        return wf
    except Exception:
        db_session.rollback()
        return None


def rename_db_wf(workflow_id, new_name):
    try:
        d_wf = Workflows.query.filter(Workflows.id == workflow_id).first()
        d_wf.name = new_name
        db_session.commit()
        return True
    except:
        return False


def rename_db_job(workflow_id, job_id, new_name):
    try:
        job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id)\
            .filter(WorkflowJobs.jobid == job_id).first()
        job.name = new_name
        db_session.commit()
        return True
    except:
        return False


def delete_db_wf(workflow_id):
    try:
        db_session.query(WorkflowMessages).filter(
            WorkflowMessages.wf_id == workflow_id).delete()
        db_session.query(WorkflowJobs).filter(
            WorkflowJobs.wf_id == workflow_id).delete()
        d_wf = Workflows.query.filter(Workflows.id == workflow_id).first()
        db_session.delete(d_wf)
        db_session.commit()
        msg_garbage_collector()
        job_garbage_collector()
        return True
    except:
        return False


def reset_db_workflow(workflow_id):
    """Clear a workflow's jobs/messages and return it to a fresh Running state,
    so a re-run that reuses the same name starts clean instead of stacking the
    previous run's rows."""
    try:
        db_session.query(WorkflowMessages).filter(
            WorkflowMessages.wf_id == workflow_id).delete()
        db_session.query(WorkflowJobs).filter(
            WorkflowJobs.wf_id == workflow_id).delete()
        wf = Workflows.query.filter(Workflows.id == workflow_id).first()
        if wf is not None:
            wf.reset()
        db_session.commit()
        return wf
    except Exception:
        db_session.rollback()
        return None


def delete_whole_db():
    try:
        db_session.query(WorkflowMessages).delete()
        db_session.query(WorkflowJobs).delete()
        db_session.query(Workflows).delete()
        db_session.commit()
        return True
    except:
        return False


def msg_garbage_collector():
    result = db_session.query(Workflows.id).all()
    notin_list_tuple = tuple([r[0] for r in result])
    result = db_session.query(WorkflowMessages.id).filter(
        ~WorkflowMessages.wf_id.in_(notin_list_tuple)).distinct()
    in_list_tuple = tuple([r[0] for r in result])
    if in_list_tuple:
        delete_q = WorkflowMessages.__table__.delete().where(
            WorkflowMessages.id.in_(in_list_tuple))
        db_session.execute(delete_q)
        db_session.commit()
    return True


def job_garbage_collector():
    result = db_session.query(Workflows.id).all()
    notin_list_tuple = tuple([r[0] for r in result])
    result = db_session.query(WorkflowJobs.id).filter(
        ~WorkflowJobs.wf_id.in_(notin_list_tuple)).distinct()
    in_list_tuple = tuple([r[0] for r in result])
    if in_list_tuple:
        delete_q = WorkflowJobs.__table__.delete().where(
            WorkflowJobs.id.in_(in_list_tuple))
        db_session.execute(delete_q)
        db_session.commit()
    return True
