from panoptes.database import db_session
from panoptes.models import Workflows, WorkflowMessages, WorkflowJobs

import json

def get_db_workflows():
    return Workflows.query.all()


def get_db_workflows_by_id(workflow_id):
    return Workflows.query.filter(Workflows.id == workflow_id).first()


def get_db_workflows_by_status(workflow_id):
    return (db_session.query(Workflows.status).filter(Workflows.id == workflow_id).first())[0]


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
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            job.job_done()
            db_session.commit()
            return True

        if msg_json["level"] == 'job_error':
            job = WorkflowJobs.query.filter(WorkflowJobs.wf_id == wf_id)\
                .filter(WorkflowJobs.jobid == msg_json["jobid"]).first()
            job.job_error()
            db_session.commit()
            wf = Workflows.query.filter(Workflows.id == wf_id).first()
            wf.set_error()
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
