FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \ 
    llvm\
    libncurses5-dev\
    libncursesw5-dev\
    xz-utils\
    tk-dev \
    nano

WORKDIR /root

RUN ["/bin/bash", "-c", "wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz && tar xvf Python-3.6.4.tgz && cd Python-3.6.4 && ./configure --enable-optimizations && make && make install && cd /root"]

RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

RUN apt-get install -y python3-pip && pip3 install pandas==0.24.2 && pip3 install tqdm

ENV PYTHONIOENCODING=utf8

