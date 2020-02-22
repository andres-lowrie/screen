FROM ubuntu:16.04

WORKDIR /root

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    python3 \
    python3-pip \
    vim
    

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ADD task1.py .
ADD task2.py .
ADD task3.py .
RUN mkdir output
CMD [ "python3", "task1.py"]
CMD [ "python3", "task2.py"]
CMD [ "python3", "task3.py"]
