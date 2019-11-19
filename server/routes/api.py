from flask import Flask, jsonify
from server.server_utilities.db_queries import get_db_workflows_by_id, get_db_workflows
from . import routes

'''
/api/workflows
/api/workflow/<workflow_id>
/api/workflow/<workflow_id>/jobs
/api/workflow<workflow_id>/<job_id>
'''


@routes.route('/api/workflows', methods=['GET'])
def get_workflows():
    workflows = [wf.get_workflow() for wf in get_db_workflows()]
    return jsonify({'workflows': workflows,
                    'size': len(workflows)})


@routes.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow_by_id(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)

    return jsonify({'workflow': workflows})

'''
@routes.route('/api/workflow/<workflow_id>/jobs', methods=['GET'])
def get_jobs_of_workflow(workflow_id):
    # Do some stuff
    return jsonify({'tasks': tasks})


@routes.route('/api/workflow/<workflow_id>/<job_id>', methods=['GET'])
def get_job_of_workflow(workflow_id, job_id):
    # Do some stuff
    return jsonify({'tasks': tasks})
'''