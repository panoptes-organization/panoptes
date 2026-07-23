##### BASE IMAGE #####
FROM python:3.12-slim

##### METADATA #####
ARG PANOPTES_VERSION="development"
LABEL base.image="python:3.12-slim"
LABEL version="2"
LABEL software="panoptes"
LABEL software.version="${PANOPTES_VERSION}"
LABEL software.description="Monitor computational workflows in real time"
LABEL software.website="https://github.com/panoptes-organization/panoptes"
LABEL software.documentation="https://github.com/panoptes-organization/panoptes/blob/master/README.md"
LABEL software.license="https://github.com/panoptes-organization/panoptes/blob/master/LICENSE.md"
LABEL software.tags="workflows,monitor,track,snakemake"
LABEL maintainer="fgypas@gmail.com"
LABEL maintainer.organisation=""
LABEL maintainer.location=""
LABEL maintainer.license="MIT"

WORKDIR /panoptes
COPY . /panoptes

RUN pip install --no-cache-dir '.[postgres]'

EXPOSE 5000

CMD ["panoptes"]
