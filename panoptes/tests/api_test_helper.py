headers = {
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "4bf65e52-fc39-425b-a7c5-b472c0b45b90,569052b9-1b47-4155-b30b-7d6d84c6cfa3",
    'Host': "127.0.0.1:8000",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

workflows = [{
    'id': 1,
    'jobs_done': 14,
    'jobs_total': 14,
    'status': "Done"
}]

jobs = {
    "input": [
        "samples/control_rep1.bam"
    ],
    "is_checkpoint": False,
    "jobid": 3,
    "log": [
        "logs/local_log/samtools_sort_control_rep1.log"
    ],
    "msg": None,
    "name": "samtools_sort",
    "output": [
        "results/control_rep1.sorted.bam"
    ],
    "shell_command": None,
    "status": "Done",
    "wildcards": {
        "sample": "control_rep1"
    },
    "workflow_id": 1
}


def pretty_print_request(request):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text)
    )
