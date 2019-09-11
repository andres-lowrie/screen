1) Create a folder a put files into the created folder.
2) Open terminal session and move to the created folder.
3) Build image via docker (e.g. `docker build --tag=iheartmedia .`)
4) Run image (e.g. `docker run -t iheartmedia`) <-- probably it's not a right syntax
5) Check container (e.g. `docker ps`)
6) Connect to container session (e.g. `docker exec -it <container_name> /bin/bash`)
7) In CLI execute a command `python session.py` and wait results 
