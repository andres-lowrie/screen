FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    python3 \
    vim

WORKDIR /root

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN ["/bin/bash", "-c", "mkdir solution && cd solution"]
COPY answer.py solution/
RUN ["/bin/bash", "-c", "cd solution && python3 answer.py > stdout.txt"]
