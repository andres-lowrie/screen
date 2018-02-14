FROM debian:jessie

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq

WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]


RUN apt-get install -y \
	default-jre \ 
	default-jdk
	
RUN ["/bin/bash", "-c", "mkdir maven && cd maven && curl http://www.trieuvan.com/apache/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz > apache-maven-3.5.2-bin.tar.gz && tar -xvf apache-maven-3.5.2-bin.tar.gz"]

ENV MVN_HOME /root/maven/apache-maven-3.5.2
ENV PATH $PATH:$MVN_HOME/bin

COPY code code

RUN cd code && \
    mvn clean compile package && \
	java -cp target/screen-0.0.1-SNAPSHOT.jar com.screen.Application /root/data