# Instructions

- Build this docker image
- You can run `bash` as the command with an interactive tty to get into the image:

```
docker run --rm -it ${whatever-you-named-the-image}
```

- Setup a local database within the docker image.
- Load the csv files from the `data` directory into the database you created.
- Answer the questions [below](README.md#Questions) and output the answers into an answer table(s).
- Lastly, create a Pull Request with your code for review

# Questions

## What's the average number of fields across all the tables you loaded?

Output should be a simple number

_sample output_

```
|Question|Answer|
|--------|------|
| 1      | 5    |
```

## What is the word count of every value of every table

Output should have fields `value` and `count` and one entry for every value found:

_sample output_

```
|     value     | count  |
|---------------|--------|
|   some value  | 435    |
| another value | 234    |
|     word      | 45     |
```

## What's the total number or rows for the all the tables?

Output should be a simple number

_sample output_

```
|Question|Answer|
|--------|------|
| 3      | 1000 |
```
