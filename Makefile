.PHONY: build run tty load process

build:
	docker build . -t iheartmedia/screen

run:
	docker run --rm -ti -v ${PWD}/output:/app/output iheartmedia/screen

tty:
	docker run --rm -ti --entrypoint=/bin/sh iheartmedia/screen

load:
	sh load.sh

process:
	python3 -m process
