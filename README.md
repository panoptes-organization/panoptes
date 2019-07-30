# vzflow

Bioinformaticians and data scientists, rely on computational frameworks (e.g. [snakemake](https://snakemake.readthedocs.io/en/stable/), [nextflow](https://www.nextflow.io/), [CWL](https://www.commonwl.org/), [WDL](https://software.broadinstitute.org/wdl/)) to process, analyze and integrate data of various types. Such frameworks allow scientists to combine software and custom tools of different origin in a unified way, which lets them reproduce the results of others, or reuse the same pipeline on different datasets. One of the fundamental issues is that the majority of the users execute multiple pipelines at the same time, or execute a multistep pipeline for a big number of datasets, or both, making it hard to track the execution of the individual steps or monitor which of the processed datasets are complete. vzflow is a tool that monitors the execution of such workflows.

vzflow is a service that can be used by:
- Administrations that want to monitor their servers
- Data scientists, bioinformaticians, etc. that want to have a general overview of the progress of their pipelines
- Web developers that want to integrate the service in bigger web applications

**Note:** vzflow is in early development stage and the first proof of concept server will support only workflows written in [snakemake](https://snakemake.readthedocs.io/en/stable/).

# Contribute

Please see the [Contributing intructions](CONTRIBUTING.md).