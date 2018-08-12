FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

RUN set -ex && \
    echo 'deb http://deb.debian.org/debian jessie-backports main' \
      > /etc/apt/sources.list.d/jessie-backports.list && \
    apt update -y && \
    apt install -t \
      jessie-backports \
      openjdk-8-jdk-headless \
      ca-certificates-java -y

ENV PATH=${PATH}:/usr/lib/jvm/java-1.8.0-openjdk-amd64/bin
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
RUN update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64

WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

ADD Main.java /usr/local/bin/Main.java
ADD commons-csv-1.5.jar /usr/local/bin/commons-csv-1.5.jar
ADD docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh
CMD /usr/local/bin/docker-entrypoint.sh
