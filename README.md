# ![alt text](server/static/src/img/brand/panoptes.png "panoptes")


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
- [sqlite3](https://www.sqlite.org/download.html)
- virtualenv

### Install and run server

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
python setup.py npm_install
```

Run server
```bash
python panoptes.py
```
Server should run on: http://127.0.0.1:5000/'

## Developer installation

### Requirements

- Python>=3.6
- [sqlite3](https://www.sqlite.org/download.html)
- npm (tested with version >=6)
- virtualenv

### Install and run server

Clone repo
```bash
git clone -b develop https://github.com/panoptes-organization/panoptes.git
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

Install pip requirements
```bash
pip install -r requirements.txt
```

Enter coreui directory and install javascipt dependencies
```bash
cd server/static
npm install
```

Go to the root directory
```bash
cd ../../
```

Run server
```bash
python panoptes.py
```
Server should run on: http://127.0.0.1:5000/'

## Docker

### Requirements

- docker
- docker-compose


### Build and run

Build
```bash
docker-compose build
```

Run
```bash
docker-compose up -d
```

Server should run on: http://127.0.0.1:8000/'

### Run an example workflow

In order to run an example workflow please follow the instructions [here](https://github.com/panoptes-organization/snakemake_example_workflow)

#### panoptes in action

[![Watch the video](https://img.youtube.com/vi/de-YSJmq_5s/hqdefault.jpg)](https://www.youtube.com/watch?v=de-YSJmq_5s)

#### CI server

Changes in develop or master trigger a [Travis](https://travis-ci.com/panoptes-organization/panoptes) build (and soon tests)

# Contribute

Please see the [Contributing instructions](CONTRIBUTING.md).

**panoptes** is one of the [selected projects](https://github.com/elixir-europe/BioHackathon-projects-2019/tree/master/projects/14) for the [2019 Paris Biohackthon](https://www.biohackathon-europe.org/). 

# Contact

In case the [issues section](https://github.com/panoptes-organization/panoptes/issues) is not enough for you, you can also contact us via [gitter](https://gitter.im/panoptes-organization/)