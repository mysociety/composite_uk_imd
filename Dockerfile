FROM python:3.8-buster

ENV DEBIAN_FRONTEND noninteractive

COPY notebook_helper/chrome_setup.bash /
RUN /chrome_setup.bash

COPY notebook_helper/base_requirements.txt /
RUN pip install -r /base_requirements.txt