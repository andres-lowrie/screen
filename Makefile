.PHONY: build run tty

build:
	docker build . -t iheartmedia/screen

run:
	docker run --rm -ti -v ${PWD}/output:/app/output iheartmedia/screen

tty:
	docker run --rm -ti --entrypoint=/bin/sh iheartmedia/screen
