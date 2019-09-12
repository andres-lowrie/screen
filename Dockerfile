FROM python:3

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

WORKDIR /usr/iheartmedia

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY screen.py screen.py
COPY screen_2.py screen_2.py