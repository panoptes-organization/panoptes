from panoptes.database import db_session
from panoptes.models import Workflows, WorkflowMessages, WorkflowJobs


def get_db_workflows():
    return Workflows.query.all()


def get_db_workflows_by_id(workflow_id):
    return Workflows.query.filter(Workflows.id == workflow_id).first()


def maintain_jobs(msg, wf_id):
    msg_json = eval(msg)

    if "jobid" in msg_json.keys():
        if msg_json["level"] == 'job_info':
            job = WorkflowJobs(
                    msg_json['jobid'],
                    wf_id, msg_json['msg'],
                    msg_json['name'],
                    repr(msg_json['input']),
                    repr(msg_json['output']),
                    repr(msg_json['log']),
                    repr(msg_json['wildcards']),
                    msg_json['is_checkpoint'],

                )
            db_session.add(job)
            db_session.commit()
            return True

        if msg_json["level"] == 'job_finished':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id).filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            job.job_done()
            db_session.commit()
            return True

        if msg_json["level"] == 'job_error':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id).filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            job.job_error()
            db_session.commit()
            return True

    if msg_json["level"] == 'info':
        if msg_json['msg'] == 'Nothing to be done.':
            wf = Workflows.query.filter(Workflows.id == wf_id).first()
            wf.set_not_executed()
            db_session.commit()
            return True

    if msg_json["level"] == 'progress':
        wf = Workflows.query.filter(Workflows.id == wf_id).first()
        wf.edit_workflow(msg_json['done'], msg_json['total'])
        db_session.commit()
        return True

    if msg_json["level"] == 'error':
        wf = Workflows.query.filter(Workflows.id == wf_id).first()
        wf.set_error()
        db_session.commit()
        return True

    if msg_json["level"] in ['shellcmd', '']:
        w = WorkflowMessages(msg, wf_id=wf_id)
        db_session.add(w)
        db_session.commit()
        return True
    return False


def get_db_jobs(workflow_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id)


def get_db_job_by_id(workflow_id, job_id):
    return WorkflowJobs.query.filter(WorkflowJobs.wf_id == workflow_id).filter(WorkflowJobs.jobid == job_id).first()
