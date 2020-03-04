FROM python:3.7

RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    vim


WORKDIR /root
RUN ["/bin/bash", "-c", "mkdir data && cd data && while read i; do git clone $i; done < <(curl -s https://api.github.com/orgs/datasets/repos?per_page=100 | jq -r '.[].clone_url')"]

#RUN git clone https://github.com/joys021/python-code.git

copy /code /root

#RUN apt-get update -y -qqq
RUN apt-get -y -qqq install python-pip
RUN pip install -r requirements.txt
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev



EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]



