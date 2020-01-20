FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    python3 \
    python3-dev

RUN mkdir /root/src
COPY ./src/* /root/src/
RUN /bin/bash -c 'chmod +x /root/src/run.sh'


WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]


