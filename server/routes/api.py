from flask import Flask, jsonify
from server.server_utilities.db_queries import get_db_workflows_by_id, get_db_workflows
from . import routes

'''
/api/workflows
/api/workflow/<workflow_id>
/api/workflow/<workflow_id>/jobs
/api/workflow<workflow_id>/<job_id>
'''
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@routes.route('/api/workflows', methods=['GET'])
def get_workflows():
    workflows = get_db_workflows()

    return jsonify({'workflows': workflows})


@routes.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow_by_id(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)

    return jsonify({'workflow': workflows})


@routes.route('/api/workflow/<workflow_id>/jobs', methods=['GET'])
def get_jobs_of_workflow(workflow_id):
    # Do some stuff
    return jsonify({'tasks': tasks})


@routes.route('/api/workflow/<workflow_id>/<job_id>', methods=['GET'])
def get_job_of_workflow(workflow_id, job_id):
    # Do some stuff
    return jsonify({'tasks': tasks})
