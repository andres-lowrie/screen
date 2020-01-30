FROM python:3.7.3-slim

RUN apt-get update && apt-get install -y git curl jq

WORKDIR /root

COPY ./ /root/

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN ["python", "main.py"]