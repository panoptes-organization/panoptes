from flask import Flask, jsonify
from panoptes.server_utilities.db_queries import get_db_workflows_by_id, get_db_workflows, get_db_jobs, get_db_job_by_id
from . import routes

'''
/api/workflows
/api/workflow/<workflow_id>
/api/workflow/<workflow_id>/jobs
/api/workflow<workflow_id>/job/<job_id>
'''

@routes.route('/api/service-info', methods=['GET'])
def get_service_info():
    return jsonify({'status': "running"})

@routes.route('/api/workflows', methods=['GET'])
def get_workflows():
    workflows = [wf.get_workflow() for wf in get_db_workflows()]
    return jsonify({'workflows': workflows,
                    'count': len(workflows)})


@routes.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow_by_id(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        return jsonify({'workflow': workflows.get_workflow()})
    else:
        return jsonify({'msg': "Workflow not found"})


@routes.route('/api/workflow/<workflow_id>/jobs', methods=['GET'])
def get_jobs_of_workflow(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        jobs = [j.get_job_json() for j in get_db_jobs(workflows.id)]
        return jsonify({'jobs': jobs,
                        'count': len(jobs)})
    else:
        return jsonify({'msg': 'Workflow not found',
                        'jobs': [],
                        'count': 0})


def get_jobs(wf_id):
    return [j.get_job_json() for j in get_db_jobs(wf_id)]


def get_job(wf_id, job_id):
    return get_db_job_by_id(wf_id, job_id).get_job_json()


@routes.route('/api/workflow/<workflow_id>/job/<job_id>', methods=['GET'])
def get_job_of_workflow(workflow_id, job_id):
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        job = get_db_job_by_id(workflows.id, job_id)
        if job:
            return jsonify({'jobs': job.get_job_json()})
        else:
            return jsonify({'msg': 'Job not found'})
    else:
        return jsonify({'msg': 'Workflow not found',
                        'jobs': [],
                        'count': 0})
