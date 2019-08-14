# Instructions

- Build this docker image

```
docker build -t ${whatever-you-named-the-image} .
```

- Run `bash` as the command with an iteractive tty to get into the image:

```
docker run --rm -it ${whatever-you-named-the-image} /bin/bash
```

- The data is in the directory `/root/data` on said image

- To run tests on your local machene

```
python3.7 -m venv venv
```

```
. ./venv/bin/activate
```

```
pip install --upgrade pip
```

```
pip install -r requirements-dev.txt
```

```
python -m pytest tests --cov=app --cov-config=.coveragerc
```

# Questions

## what's the average number of fields across all the `.csv` files?

output should be a simple number

_sample output_

```
5
```

## create a csv file that shows the word count of every value of every dataset (dataset being a `.csv` file)

output should be a csv file that has a header row with fields `value` and
`count` and one entry for every value found:

_sample output_

```
value,count
some value,435
another value,234
word,45
...
```

## what's the total number or rows for the all the `.csv` files?

output should be a simple number

_sample output_

```
1000000000
```


