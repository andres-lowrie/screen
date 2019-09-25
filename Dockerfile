FROM python:3.6.5-jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

WORKDIR /root

COPY parse_csv_files.py parse_csv_files.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN ["python", "parse_csv_files.py"]
