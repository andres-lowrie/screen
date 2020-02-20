FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    python3 \
    vim

WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

ADD https://raw.githubusercontent.com/virajgite/screen/master/solution.py /root/

RUN /bin/bash -c 'python3 /root/solution.py'