FROM python:3

WORKDIR /root

RUN mkdir -p /app

COPY ./app /app

RUN pip install -r /app/requirements.txt

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

RUN apt-get -yq install sqlite3 libsqlite3-dev

RUN apt-get -y install vim

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN python /app/load_db.py
RUN python /app/questions.py

CMD ["/bin/bash", "/app/get_tables.sh"]
