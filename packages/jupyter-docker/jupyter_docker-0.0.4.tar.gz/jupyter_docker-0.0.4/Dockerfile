# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

FROM python:3.11

RUN mkdir /opt/jupyter-docker

WORKDIR /opt/jupyter-docker

RUN pip install kazoo

COPY jupyter_docker /opt/jupyter_docker
RUN pip install -e ./jupyter_docker

# COPY frontplane/dist.html /opt/jupyter-docker/index.html

WORKDIR /opt/jupyter-docker/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_docker"]
