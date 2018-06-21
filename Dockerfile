FROM debian:buster

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    openjdk-8-jdk \
    gradle


WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')" ]
