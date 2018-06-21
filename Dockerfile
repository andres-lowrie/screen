FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3 \
    gcc \
    libc-dev \
    build-essential \
    python3-dev \
    python3-pip \
    jq

WORKDIR /root

COPY csv_analyzer.py /root/csv_analyzer.py

RUN ["/bin/bash","-c","python3 -m pip install pandas;mkdir output;mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]
