# ![alt text](panoptes/static/src/img/brand/panoptes.png "panoptes")


Bioinformaticians and data scientists, rely on computational frameworks (e.g. [snakemake](https://snakemake.readthedocs.io/en/stable/), [nextflow](https://www.nextflow.io/), [CWL](https://www.commonwl.org/), [WDL](https://software.broadinstitute.org/wdl/)) to process, analyze and integrate data of various types. Such frameworks allow scientists to combine software and custom tools of different origin in a unified way, which lets them reproduce the results of others, or reuse the same pipeline on different datasets. One of the fundamental issues is that the majority of the users execute multiple pipelines at the same time, or execute a multistep pipeline for a big number of datasets, or both, making it hard to track the execution of the individual steps or monitor which of the processed datasets are complete. panoptes is a tool that monitors the execution of such workflows.

panoptes is a service that can be used by:
- Data scientists, bioinformaticians, etc. that want to have a general overview of the progress of their pipelines and the status of their jobs
- Administrations that want to monitor their servers
- Web developers that want to integrate the service in bigger web applications

**Note:** panoptes is in early development stage and the first proof of concept server will support only workflows written in [snakemake](https://snakemake.readthedocs.io/en/stable/).

# Installation

## Basic installation process

### Requirements

- Python>=3.6
- virtualenv
- [sqlite3](https://www.sqlite.org/download.html)

### Option 1: Install via pypi and run server

Create virtual environment
```bash
virtualenv -p `which python3` venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install via pypi
```bash
pip install panoptes-ui
```
Run server
```bash
panoptes
```
Server should run on: 127.0.0.1:5000

By default it should generate an sqlite database: .panoptes.db

### Option 2: Install via conda and run server

Create conda environment
```bash
conda create --name panoptes
```

Activate conda environment
```bash
conda activate panoptes
```

Install via pypi OR conda
```bash
conda install -c panoptes-organization panoptes-ui
```
Run server
```bash
panoptes
```
Server should run on: 127.0.0.1:5000

By default it should generate an sqlite database: .panoptes.db

### Option 3: Install from source code and run server

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
virtualenv -p `which python3` venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install all requirements
```bash
pip install .
```

Run server
```bash
panoptes
```
Server should run on: 127.0.0.1:5000

By default it should generate an sqlite database: .panoptes.db 

## Docker installation

### Requirements

- docker
- docker-compose

### Build and run with docker-compose

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

### Run an example workflow

In order to run an example workflow please follow the instructions [here](https://github.com/panoptes-organization/snakemake_example_workflow)

### panoptes in action

[![Watch the video](https://img.youtube.com/vi/de-YSJmq_5s/hqdefault.jpg)](https://www.youtube.com/watch?v=de-YSJmq_5s)

### panoptes API

Panoptes provides the following API endpoints:

Endpoint | Method | Description 
-- | -- | --
`/api/service-info` | `GET` | Server status
`/api/workflows` | `GET` | Get all workflows
`/api/workflow/<workflow-id>` | `GET` | Get workflow status
`/api/workflow/<workflow-id>/jobs` | `GET` | Get all jobs of a workflow
`/api/workflow/<workflow-id>/job/<job-id>` | `GET` | Get job status
`/api/workflow/<workflow-id>` | `PUT` | Rename a workflow  <br>  Expects a dictionary with new name <br> (e.g. `{'name': 'my new workflow name'}`)
`/api/workflow/<workflow-id>` | `DELETE` | Delete a workflow
`/api/workflows/all` | `DELETE` | Clean up database

To communicate with panoptes the following endpoints are used by snakemake:

Endpoint | Method | Description 
-- | -- | --
`/api/service-info` | `GET` | Server status (same as above)
`/create_workflow` | `GET` | Get a unique id/name str(uuid.uuid4()) for each workflow
`/update_workflow_status` | `POST` | Panoptes receives a dictionary from snakemake that contains: <br> - A log message dictionary <br> - The current timestamp <br> - The unique id/name of the workflow. <br> (e.g. `{'msg': repr(msg), 'timestamp': time.asctime(), 'id': id}`)

# Contribute

Please see the [Contributing instructions](CONTRIBUTING.md).

## CI server

Changes in develop or master trigger a [Travis](https://travis-ci.com/panoptes-organization/panoptes) build (and runs tests)

# Contact

In case the [issues section](https://github.com/panoptes-organization/panoptes/issues) is not enough for you, you can also contact us via [discord](https://discord.gg/vMcZCVZ)
