FROM python:alpine3.7

WORKDIR /app

ADD load.sh /app/load.sh
ADD process.py /app/process.py

RUN apk update --no-cache && \
	apk add --update --no-cache git curl jq && \
	chmod +x /app/load.sh && \
 	chmod +x /app/process.py

ENV LOG_LEVEL INFO

ENTRYPOINT /app/load.sh && python -m process