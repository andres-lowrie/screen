# Instructions

Here are step by step instructions on how to specifically run my code.

```
git clone https://github.com/csravelar/screen.git

cd screen

git checkout solution

sudo docker build -t iheart .

sudo docker run --rm -it iheart
```

Once you are in, navigate to the solutions directory.
The stdin output will be called stdout.txt and the occurence cvs file will be called result.csv


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
