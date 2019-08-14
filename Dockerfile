FROM debian:jessie
FROM python:3.7

ENV APP /root

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    vim

COPY app $APP/app

WORKDIR $APP 
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]
