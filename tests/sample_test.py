import requests

url = 'http://127.0.0.1:5000'
docker_url = 'http://127.0.0.1:8000'


def test_docker_api_work_flows():
    r = requests.get(docker_url + '/api/workflows')  # Assumes that it has a path of "/"
    assert r.status_code == 200  # Assumes that it will return a 200 response
