import requests
import panoptes.tests.api_test_helper as helper

local_url = 'http://127.0.0.1:5000'
docker_url = 'http://127.0.0.1:8000'

# CI server uses docker, to run locally use local_url
url_to_use = docker_url
# Workflow and job entries to check. We don't check the date related entries
workflow_entries = ['id', 'jobs_done', 'jobs_total']
job_entries = ['input', 'is_checkpoint', 'jobid', 'log', 'msg', 'name', 'output', 'shell_command', 'status',
               'wildcards', 'workflow_id']
jobs_entries = ['is_checkpoint', 'msg', 'name', 'shell_command', 'status',
                'workflow_id']


#   Get all workflows
def test_workflows():
    response = requests.request(
        "GET", url_to_use + '/api/workflows', headers=helper.headers)
    assert response.status_code == 200
    assert response.json()["count"] == 2
    for entry in workflow_entries:
        assert response.json()[
            "workflows"][0][entry] == helper.workflows[0][entry]
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Non existent workflow
def test_specific_work_flow_not_found():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/100', headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Valid workflow
def test_specific_work_flow_valid():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/1', headers=helper.headers)
    assert response.status_code == 200
    for entry in workflow_entries:
        assert response.json()["workflow"][entry] == helper.workflows[0][entry]
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   All jobs for a valid workflow
def test_specific_work_flow_all_jobs_valid():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/1/jobs', headers=helper.headers)
    assert response.status_code == 200
    assert response.json()["count"] == 14
    for entry in jobs_entries:
        assert response.json()["jobs"][0][entry] == helper.jobs[entry]
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Jobs for non existent workflow
def test_specific_work_flow_jobs_not_found():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/100/jobs', headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Specific job for a specific workflow
def test_specific_work_flow_and_job_valid():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/1/job/3', headers=helper.headers)
    assert response.status_code == 200
    for entry in job_entries:
        assert response.json()["jobs"][entry] == helper.jobs[entry]
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Non existent job for a specific workflow
def test_specific_work_flow_and_job_non_existent():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/1/job/100', headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Non existent workflow and job for a specific workflow
def test_specific_work_flow_job_non_existent():
    response = requests.request(
        "GET", url_to_use + '/api/workflow/100/job/1', headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Specific rename a specific workflow
def test_specific_work_flow_re_name_existent():
    data = {'name': 'test name'}
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/1', json=data, headers=helper.headers)
    assert response.status_code == 200
    for entry in workflow_entries:
        assert response.json()["workflow"][entry] == helper.workflows[0][entry]
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)

#   Specific rename a specific workflow with empty json
def test_specific_work_flow_re_name_json_non_existent():
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/1', headers=helper.headers)
    assert response.status_code == 400
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)

#   Specific rename a specific workflow with wrong key
def test_specific_work_flow_re_name_json_wrong_key():
    data = {'wrong_name':'test name'}
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/1', json=data, headers=helper.headers)
    assert response.status_code == 400
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Specific rename a specific workflow with white space data
def test_specific_work_flow_re_name_json_wrong_data():
    data = {'name':'    '}
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/1', json=data, headers=helper.headers)
    assert response.status_code == 400
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)

#   Specific rename a specific workflow with white no data
def test_specific_work_flow_re_name_json_wrong_non_data():
    data = {'name':''}
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/1', json=data, headers=helper.headers)
    assert response.status_code == 400
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)

#   Non existent specific rename a specific workflow
def test_specific_work_flow_re_name_non_existent():
    data = {'name': 'test name'}
    response = requests.request(
        "PUT", url_to_use + '/api/workflow/100', json=data, headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Specific workflow delete existent
def test_specific_work_flow_delete_existent():
    response = requests.request(
        "DELETE", url_to_use + '/api/workflow/1', headers=helper.headers)
    assert response.status_code == 204
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   Specific workflow delete non existent
def test_specific_work_flow_delete_non_existent():
    response = requests.request(
        "DELETE", url_to_use + '/api/workflow/100', headers=helper.headers)
    assert response.status_code == 404
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   clean up the whole database
def test_clean_up_database_existent():
    response = requests.request(
        "DELETE", url_to_use + '/api/workflows/all', headers=helper.headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Database clean up is complete"
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)


#   clean up the whole database non existent
def test_clean_up_database_non_existent():
    response = requests.request(
        "DELETE", url_to_use + '/api/workflows/all', headers=helper.headers)
    assert response.status_code == 410
    helper.pretty_print_request(response.request)
    helper.pretty_print_response(response)
