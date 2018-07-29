# Run Instructions

##### Build the image
- `make build`

Docker command:
```bash
docker build . -t iheartmedia/screen
```

#### Run in the container
- `make run`
- The results will be put the directory `output`. The directory will be create if it does not exist.
- Average number of fields across all the `.csv` files:
    -  `./output/average_fields` 
- Word count of every value of every dataset (dataset being a `.csv` file):
    -   `./output/word_count.csv`
- Total number or rows for the all the `.csv` files:
    -   `./output/total_rows`

Docker command:
```bash
docker run --rm -ti -v ${PWD}/output:/app/output iheartmedia/screen
```
#### Interactive TTY
- `make tty`

Docker command:
```bash
docker run --rm -ti --entrypoint=/bin/sh iheartmedia/screen
```
