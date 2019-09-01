# vzflow

Bioinformaticians and data scientists, rely on computational frameworks (e.g. [snakemake](https://snakemake.readthedocs.io/en/stable/), [nextflow](https://www.nextflow.io/), [CWL](https://www.commonwl.org/), [WDL](https://software.broadinstitute.org/wdl/)) to process, analyze and integrate data of various types. Such frameworks allow scientists to combine software and custom tools of different origin in a unified way, which lets them reproduce the results of others, or reuse the same pipeline on different datasets. One of the fundamental issues is that the majority of the users execute multiple pipelines at the same time, or execute a multistep pipeline for a big number of datasets, or both, making it hard to track the execution of the individual steps or monitor which of the processed datasets are complete. vzflow is a tool that monitors the execution of such workflows.

vzflow is a service that can be used by:
- Administrations that want to monitor their servers
- Data scientists, bioinformaticians, etc. that want to have a general overview of the progress of their pipelines
- Web developers that want to integrate the service in bigger web applications

**Note:** vzflow is in early development stage and the first proof of concept server will support only workflows written in [snakemake](https://snakemake.readthedocs.io/en/stable/).

# Installation

## Development installation

### Install Mongo DB

Install [Mongo DB](https://docs.mongodb.com/manual/installation/)

- [Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
- [Linux](https://docs.mongodb.com/manual/administration/install-on-linux/)

Server should run on: http://127.0.0.1:27017/

### Install Postman

Install [Postman](https://www.getpostman.com/) to send mock json requests to the server.

### Install Flask server

Create virtual environment
```bash
virtualenv -p `which python3` venv
```

Create virtual environment
```bash
source venv/bin/activate
```

Create virtual environment
```bash
pip install -r requirements.txt
```

Install requirements
```bash
pip install -r requirements.txt
```

EXPORT FLASK_APP
```bash
export FLASK_APP=server/app.py
export FLASK_ENV=development
```

Run server
```bash
python -m flask run
```

Server should run on: http://127.0.0.1:5000/

# Contribute

Please see the [Contributing instructions](CONTRIBUTING.md).
