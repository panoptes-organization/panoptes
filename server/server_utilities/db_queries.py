import traceback

from server.database import init_db, db_session
from server.models import Workflows, WorkflowMessages, WorkflowJobs
from sqlalchemy import update


def get_db_workflows():
    return Workflows.query.all()


def get_db_workflows_by_id(workflow_id):
    return Workflows.query.filter(Workflows.id == workflow_id).first()


def maintain_jobs(msg, wf_id):
    msg_json = eval(msg)

    if "jobid" in msg_json.keys():
        if msg_json["level"] == 'job_info':
            job = WorkflowJobs(msg_json['jobid'], wf_id, msg_json['msg'], msg_json['name'], repr(msg_json['input']),
                               repr(msg_json['output']), repr(msg_json['log']), repr(msg_json['wildcards']),
                               msg_json['is_checkpoint'])
            db_session.add(job)
            db_session.commit()
            return True

        if msg_json["level"] == 'job_finished':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id and WorkflowJobs.id == msg_json["jobid"])
            job.status = "Done"
            db_session.commit()
            return True

    if msg_json["level"] in ['shellcmd', 'progress']:
        w = WorkflowMessages(msg, wf_id)
        db_session.add(w)
        db_session.commit()
        return True
    return False


def get_db_jobs(workflow_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id)


def get_db_job_by_id(workflow_id, job_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id and WorkflowJobs.jobid == job_id).first()
