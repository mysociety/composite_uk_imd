FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt