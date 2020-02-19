
FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq	\
    python3 \
    vim \
    && apt-get install python3 -y \
    && apt-get install python3-pip -y \
    && apt-get install python3-pandas -y 

WORKDIR /root

ADD prog.py .
ADD prog2.py .
ADD prog3.py . 

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]
