FROM python:3.8

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt