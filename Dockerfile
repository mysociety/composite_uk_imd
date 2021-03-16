FROM python:3.8

RUN curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
      && echo 'deb https://deb.nodesource.com/node_14.x buster main' > /etc/apt/sources.list.d/nodesource.list

RUN curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
      && echo 'deb https://deb.nodesource.com/node_14.x buster main' > /etc/apt/sources.list.d/nodesource.list

RUN curl -s https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
      && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list

RUN apt-get -qq update \
      && apt-get -qq install \
            google-chrome-stable \
      && rm -rf /var/lib/apt/lists/*

COPY notebook_helper/chrome_setup.bash /
RUN /chrome_setup.bash

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt

