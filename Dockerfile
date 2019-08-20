FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    zlib1g-dev

# compile a modern version of python
RUN wget -c "https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz" && tar xzvf Python-3.6.7.tgz && \
    cd Python-3.6.7 && ./configure && make -j4 && make install && cd .. && rm -rf Python-3.6.7 Python-3.6.7.tgz

WORKDIR /root
RUN python3.6 -m venv .env

COPY data-aggregator src/

RUN ["/bin/bash", "-c", "source .env/bin/activate && python src/setup.py install"]

# run app to store results in image filesystem layer
RUN ["/bin/bash", "-c", "source .env/bin/activate && data-aggregator"]
