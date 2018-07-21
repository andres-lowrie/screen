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

> **In case you'd like to read what exactly my code does, I provided a copy of my answer.py file with docstrings called "answer_with_docstrings.py". Feel free to take a look.
