FROM ghcr.io/mysociety/data_common:sha-e3ee4f4

# Make an empty project directory so the 'self' setup doesn't fail and scripts can be setup
# Override the .pth created at previous stages to point to where the working directory will land
COPY pyproject.toml poetry.loc[k] /setup/ 
COPY src/data_common/pyproject.toml src/data_common/poetry.loc[k] /setup/src/data_common/
ENV WORKSPACE_NAME composite_uk_imd
RUN mkdir /setup/src/$WORKSPACE_NAME \
    && touch /setup/src/$WORKSPACE_NAME/__init__.py \
    && mkdir --parents /setup/src/data_common/src/data_common \
    && touch /setup/src/data_common/src/data_common/__init__.py \
    && export PATH="/root/.local/bin:$PATH" \
    && cd /setup/ && poetry install \
    && echo "/workspaces/$WORKSPACE_NAME/src/" > /usr/local/lib/python3.10/site-packages/$WORKSPACE_NAME.pth \
    && echo "/workspaces/$WORKSPACE_NAME/src/data_common/src" > /usr/local/lib/python3.10/site-packages/data_common.pth

# special binder instructions

RUN pip install --no-cache-dir notebook

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}