from flask import jsonify, request, Response
from panoptes.server_utilities.db_queries import get_db_workflows_by_id, get_db_workflows, get_db_jobs, get_db_job_by_id, delete_db_wf, get_db_workflows_by_status, delete_whole_db, get_db_table_is_empty, rename_db_wf, rename_db_job
from . import routes

'''
/api/workflows
/api/workflow/<workflow_id>
/api/workflow/<workflow_id>/jobs
/api/workflow<workflow_id>/job/<job_id>
/api/workflows/all
'''


@routes.route('/api/service-info', methods=['GET'])
def get_service_info():
    return jsonify({'status': "running"}), 200


@routes.route('/api/workflows', methods=['GET'])
def get_workflows():
    workflows = [wf.get_workflow() for wf in get_db_workflows()]
    return jsonify({'workflows': workflows,
                    'count': len(workflows)}), 200


@routes.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow_by_id(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        return jsonify({'workflow': workflows.get_workflow()}), 200
    else:
        response = Response(status=404)
        return response


@routes.route('/api/workflow/<workflow_id>/jobs', methods=['GET'])
def get_jobs_of_workflow(workflow_id):
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        jobs = [j.get_job_json() for j in get_db_jobs(workflows.id)]
        return jsonify({'jobs': jobs,
                        'count': len(jobs)}), 200
    else:
        response = Response(status=404)
        return response


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
            return jsonify({'jobs': job.get_job_json()}), 200
        else:
            response = Response(status=404)
            return response
    else:
        response = Response(status=404)
        return response


@routes.route('/api/workflow/<workflow_id>', methods=['PUT'])
def rename_workflow_by_id(workflow_id):
    data = request.json
    if data is None or 'name' not in data or len(data['name']) < 1 or data['name'].isspace():
        response = Response(status=400)
        return response
    workflows = get_db_workflows_by_id(workflow_id)
    if workflows:
        if rename_db_wf(workflow_id, data['name']):
            return jsonify({'workflow': workflows.get_workflow()}), 200
        else:
            return jsonify({'msg': 'Database error'}), 500
    else:
        response = Response(status=404)
        return response


@routes.route('/api/workflow/<workflow_id>', methods=['DELETE'])
def set_db_delete(workflow_id):
    if(get_db_workflows_by_id(workflow_id) is None):
        response = Response(status=404)
        return response
    elif(get_db_workflows_by_status(workflow_id) == 'Running'):
        return jsonify({'msg': 'You cannot delete Running Workflow '}), 403
    else:
        delete = delete_db_wf(workflow_id)
        if delete:
            response = Response(status=204)
            return response
        else:
            return jsonify({'msg': 'The server is unable to store the '
                            'representation needed to complete the delete request.'}), 507


@routes.route('/api/workflows/all', methods=['DELETE'])
def set_whole_db_delete():
    if get_db_table_is_empty('Workflows'):
        response = Response(status=410)
        return response
    else:
        delete = delete_whole_db()
        if delete:
            return jsonify({'msg': 'Database clean up is complete'}), 200
        else:
            return jsonify({'msg': 'The server is unable to store the '
                            'representation needed to complete the delete request.'}), 507
