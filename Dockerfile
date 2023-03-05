ARG BUILD_IMAGE=python:3.10
ARG BASE_IMAGE=python:3.10-slim

FROM $BUILD_IMAGE AS build

# Create a virtual environment in which package will be installed
RUN python3 -m pip install -U pip setuptools wheel \
    && python3 -m pip install virtualenv \
    && python3 -m virtualenv /opt/genid --download \
    && mkdir -p /build

# Copy only requirements
COPY requirements.txt /build/requirements.txt

# Install and cache dependencies (relies on host pip config)
RUN --mount=type=secret,id=pip-config \
    mkdir -p $HOME/.config/pip \
    && cp /run/secrets/pip-config $HOME/.config/pip/pip.conf \
    && /opt/genid/bin/python -m pip install -r /build/requirements.txt

# Copy only required files to perform build
COPY README.md /build/README.md
COPY pyproject.toml /build/pyproject.toml
COPY src /build/src

RUN /opt/genid/bin/python -m pip install /build

FROM $BASE_IMAGE

ARG USER_ID="1000"
ARG GROUP_ID="1000"
ARG USER_NAME="genid"

ENV PROJECT_NAME="genid"

RUN groupadd --gid $GROUP_ID $USER_NAME \
    && useradd \
    --create-home \
    --home-dir /$USER_NAME \
    --shell /bin/bash \
    --uid $USER_ID \
    --gid $GROUP_ID \
    $USER_NAME

USER $USER_NAME

COPY --from=build /opt/genid /opt/genid

ENV PATH="/opt/genid/bin:$PATH"
