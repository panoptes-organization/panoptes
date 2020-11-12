from flask import jsonify
from panoptes.server_utilities.db_queries import get_db_workflows_by_id, get_db_workflows, get_db_jobs, get_db_job_by_id, delete_db_wf, get_db_workflows_by_status, delete_whole_db, get_db_table_is_empty
from . import routes

'''
/api/workflows
/api/workflow/<workflow_id>
/api/workflow/<workflow_id>/jobs
/api/workflow<workflow_id>/job/<job_id>
/api/delete/<workflow_id>
/api/clean-up-database
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


@routes.route('/api/delete/<workflow_id>', methods=['GET'])
def set_db_delete(workflow_id):
    if(get_db_workflows_by_id(workflow_id) is None):
        return jsonify({'error': 404, 'msg': 'Unable to delete Workflow ' + workflow_id + 
                        '. Please check if workflow ' + workflow_id + ' exists.'})
    elif(get_db_workflows_by_status(workflow_id)=='Running'):
        return jsonify({'error': 'Delete Rejected', 'msg': 'You cannot delete Running Workflow '})
    else:        
        delete=delete_db_wf(workflow_id)
        if delete:
          return jsonify({'msg': "Delete Complete Correctly ",'Workflow': workflow_id})
        else:
             return jsonify({'error': 404, 'msg': 'Database error'})


@routes.route('/api/clean-up-database', methods=['GET'])
def set_whole_db_delete():
    if get_db_table_is_empty('Workflows'):
        return jsonify({'error': 404, 'msg': 'Database is empty'})
    else:
        delete=delete_whole_db()
        if delete:
            return jsonify({'msg': 'Database clean up is complete'})
        else:
            return jsonify({'error': 404, 'msg': 'Database error'})