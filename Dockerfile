##### BASE IMAGE #####
FROM python:3.6.12-slim

##### METADATA #####
LABEL base.image="python:3.6.12-slim"
LABEL version="1"
LABEL software="panoptes"
LABEL software.version="development"
LABEL software.description="Monitor computational workflows in real time"
LABEL software.website="https://github.com/panoptes-organization/panoptes"
LABEL software.documentation="https://github.com/panoptes-organization/panoptes/blob/develop/README.md"
LABEL software.license="https://github.com/panoptes-organization/panoptes/blob/develop/LICENSE.md"
LABEL software.tags="workflows,monitor,track"
LABEL maintainer="fgypas@gmail.com"
LABEL maintainer.organisation=""
LABEL maintainer.location=""
LABEL maintainer.license="MIT"

COPY . /panoptes

RUN cd panoptes && pip install .

CMD ["panoptes"]
