1) Create a folder and put files into the created folder.
2) Open a terminal session and move to the created folder.
3) Build an image via docker (e.g. `docker build --tag=iheartmedia .`).
4) Run image (e.g. `docker run -i -t iheartmedia /bin/bash`).
5) In the terminal execute a command `python screen.py` and wait for results. (brute-force solution, only for utf-8)

Extra.
6) In the terminal execute a command `python screen_2.py` and wait for results. (slow solution, for any encoding)
