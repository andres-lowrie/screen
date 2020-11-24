FROM debian

RUN apt-get update && apt -y upgrade && apt-get install -y \
    git \
    curl \
    jq \
    mariadb-server

RUN apt install -y python3
RUN apt install nano
RUN apt install -y python3-pip
RUN pip3 install pandas
RUN pip3 install sqlalchemy
RUN pip3 install mysql-connector








WORKDIR /root

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]



COPY Load_CSV_to_DB.py ./
COPY exercise_answer.py ./

