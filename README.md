# ![alt text](panoptes/static/src/img/brand/panoptes.png "panoptes")


Bioinformaticians and data scientists, rely on computational frameworks (e.g. [snakemake](https://snakemake.readthedocs.io/en/stable/), [nextflow](https://www.nextflow.io/), [CWL](https://www.commonwl.org/), [WDL](https://software.broadinstitute.org/wdl/)) to process, analyze and integrate data of various types. Such frameworks allow scientists to combine software and custom tools of different origin in a unified way, which lets them reproduce the results of others, or reuse the same pipeline on different datasets. One of the fundamental issues is that the majority of the users execute multiple pipelines at the same time, or execute a multistep pipeline for a big number of datasets, or both, making it hard to track the execution of the individual steps or monitor which of the processed datasets are complete. panoptes is a tool that monitors the execution of such workflows.

panoptes is a service that can be used by:
- Data scientists, bioinformaticians, etc. that want to have a general overview of the progress of their pipelines and the status of their jobs
- Administrations that want to monitor their servers
- Web developers that want to integrate the service in bigger web applications

**Note:** panoptes currently supports workflows written in [snakemake](https://snakemake.readthedocs.io/en/stable/).

> **Snakemake 9 users:** the legacy `--wms-monitor` flag was removed upstream.
> Monitoring is now delivered via a logger plugin — see
> [Snakemake 9 support](#snakemake-9-support) below.

# Installation

Requirements:
- Python>=3.11
- virtualenv
- [sqlite3](https://www.sqlite.org/download.html)

## Local
### pypi

Create virtual environment
```bash
python3 -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install via pypi
```bash
pip install panoptes-ui
```

### conda

Create conda environment
```bash
conda create --name panoptes -c conda-forge -c bioconda panoptes-ui
```

Activate conda environment
```bash
conda activate panoptes
```

### Source code

Clone repo
```bash
git clone https://github.com/panoptes-organization/panoptes.git
```

Enter repo
```bash
cd panoptes
```

Create virtual environment
```bash
python3 -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install all requirements
```bash
pip install .
```

### Run the server
By default, server should run on `127.0.0.1:5000`, and generate the sqlite database `.panoptes.db`.

The running version is shown in the web UI under **About** (and is available programmatically as `panoptes.__version__`).

#### Using the development server
```bash
panoptes
```

#### Using a WSGI server
Install all necessary packages (see above), plus a WSGI server (e.g. [gunicorn](https://gunicorn.org/) or [waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/)), and run the server:
```bash
gunicorn --access-logfile logs/access.log --error-logfile logs/error.log --timeout 120 --bind :5000 panoptes.app:app
```

## Containers
### Docker

Requirements:
- docker

Pull image that is automatically built from bioconda. You can find the latest tag in the following url: https://quay.io/repository/biocontainers/panoptes-ui?tab=tags. For example:
```
docker pull quay.io/biocontainers/panoptes-ui:1.0.0--pyhdfd78af_0
```

Then run the container with:

```bash
docker run -p 5000:5000 -it <image-id> panoptes
```

> Note: In this case the database is stored within the docker image, so every time you restart the server the database will be empty. You would need to mount the volumes to make the database persistent.

### Docker compose

Requirements:
- docker
- docker-compose

Build
```bash
docker-compose build
```

Run
```bash
docker-compose up -d
```

Server should run on: http://127.0.0.1:8000

Stop
```bash
docker-compose down
```

### Singularity

You can also deploy the server with singularity. To do so pull the image with singularity. For example:

```bash
singularity pull docker://quay.io/biocontainers/panoptes-ui:1.0.0--pyhdfd78af_0
```

And then we can start the server by running:
```bash
singularity exec panoptes-ui:1.0.0--pyhdfd78af_0
```

# Run an example workflow

A small reference pipeline (samtools sort/index → htseq-count → merge across
four samples) that already wires up `--logger panoptes` lives at
[snakemake_example_workflow](https://github.com/panoptes-organization/snakemake_example_workflow).
Follow the instructions there to exercise this server end-to-end.

# Snakemake 9 support

Starting with Snakemake 9, the `--wms-monitor` flag that older panoptes versions
relied on has been removed. Monitoring is instead delivered through
[logger plugins](https://snakemake.readthedocs.io/en/stable/executing/monitoring.html).

To stream events from a Snakemake 9 workflow to panoptes, install the companion
logger plugin with either pip or conda:

```bash
pip install snakemake-logger-plugin-panoptes
# or
conda install -c conda-forge -c bioconda snakemake-logger-plugin-panoptes
```

Then pass `--logger panoptes` to Snakemake:

```bash
snakemake \
    --cores 1 \
    --logger panoptes \
    --logger-panoptes-address http://127.0.0.1:5000
```

The plugin lives in its own repository:
[panoptes-organization/snakemake-logger-plugin-panoptes](https://github.com/panoptes-organization/snakemake-logger-plugin-panoptes).
It registers a workflow with panoptes via `GET /create_workflow` on the first
event and then translates Snakemake's `LogEvent` records (`JOB_INFO`,
`JOB_STARTED`, `JOB_FINISHED`, `JOB_ERROR`, `SHELLCMD`, `PROGRESS`, `ERROR`,
`RUN_INFO`) into the JSON payloads that panoptes' `/update_workflow_status`
endpoint already understands.

Workflows orchestrated by Snakemake &lt; 9 continue to work unchanged via the
legacy `--wms-monitor http://<host>:<port>` flag.

## panoptes in action

[![Watch the video](https://img.youtube.com/vi/de-YSJmq_5s/hqdefault.jpg)](https://www.youtube.com/watch?v=de-YSJmq_5s)

## panoptes API

Panoptes provides the following API endpoints:

Endpoint | Method | Description 
-- | -- | --
`/api/service-info` | `GET` | Server status
`/api/workflows` | `GET` | Get all workflows
`/api/workflow/<workflow-id>` | `GET` | Get workflow status
`/api/workflow/<workflow-id>/jobs` | `GET` | Get all jobs of a workflow
`/api/workflow/<workflow-id>/job/<job-id>` | `GET` | Get job status
`/api/workflow/<workflow-id>` | `PUT` | Rename a workflow  <br>  Expects a dictionary with new name <br> (e.g. `{'name': 'my new workflow name'}`)
`/api/workflow/<workflow-id>/cancel` | `POST` | Cancel a workflow (sets its status to `Cancelled`). Use this to move a workflow that is stuck as `Running` (e.g. a dry run, or a process killed with `kill -9`) into a deletable state.
`/api/workflow/<workflow-id>` | `DELETE` | Delete a workflow. A workflow that is still `Running` is protected and returns `403`; cancel it first via the endpoint above.
`/api/workflows/all` | `DELETE` | Clean up database (deletes all workflows, including running ones)

To communicate with panoptes the following endpoints are used by snakemake:

Endpoint | Method | Description 
-- | -- | --
`/api/service-info` | `GET` | Server status (same as above)
`/create_workflow` | `GET` | Get a unique id/name str(uuid.uuid4()) for each workflow
`/update_workflow_status` | `POST` | Panoptes receives a dictionary from snakemake that contains: <br> - A log message dictionary (JSON-encoded) <br> - The current timestamp <br> - The unique id/name of the workflow. <br> (e.g. `{'msg': json.dumps(message), 'timestamp': time.asctime(), 'id': id}`)

# Contribute

Please see the [Contributing instructions](CONTRIBUTING.md).

## CI server

Changes on master (and pull requests against it) trigger a [GitHub Actions](https://github.com/panoptes-organization/panoptes/actions) build that runs the test suite and a live end-to-end run of the example workflow.

# Contact

In case the [issues section](https://github.com/panoptes-organization/panoptes/issues) is not enough for you, you can also contact us via [discord](https://discord.gg/vMcZCVZ)
