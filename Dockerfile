FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
	&& apt-get install python3 -y \
    && apt-get install python3-pip -y \
    && apt-get install python3-venv -y \
    && python3 -m venv venv
	
WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

COPY python_docker.py data/python_docker.py

CMD ["/usr/bin/python3", "data/python_docker.py"]