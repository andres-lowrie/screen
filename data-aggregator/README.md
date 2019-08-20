# Code challenge: Aggregations over csv data

*by Alfredo Valles - email: alfredo.valles@gmail.com - github: alfre2v*


## What is this?

This package attempt to solve the code challenge described [here](https://github.com/andres-lowrie/screen/blob/master/README.md)


## Running the code

To build the image and execute the application (results saved in the image disk):

```
$ docker build -t iheart-screen-alfredo:1.0 .
```

When the build is finished you can access the app results by running the container:

```
docker run --rm -it iheart-screen-alfredo:1.0 /bin/bash
```


## Accessing the Results

After the app is finished the execution (or the docker image is built if that's how you are running tha app),
you will find an output dir **/root/output** with the following content:

```
app-logfile.log                      # the application logs 
csv_files_parse_failure.txt          # a list of csv files we failed to parse
csv_files_parse_success.txt          # a list of the cvs files we could parse successfully
question1_avg_fields.txt             # the answer to question 1
question2_aggregated_counts.csv      # the answer to question 2
question3_total_rows.txt             # the answer to question 3
```


## Python Package use

If you don't build the docker image but instead want to install the python app yourself


### Manual installation

Like almost any python distributable packages these days, you just have to:

```
# Optional: Probably you want to setup a virtualenv and activate it
$ virtualenv .env
$ source .env/bin/activate
$
# build and install the setuptools package
$ cd data-aggregator
$ python setup.py install
$
# the installer creates a bunch of build related folders, if you want to clean them:
$ python setup.py clean --all
```


### Invocation

Execute the app by calling the command:

```
$ data-aggregator
```


### Running tests

App tests can be run from to installer script:

```
$ python setup.py test
```



## App design considerations

1. Decided not to use Pandas or any other data science package because the task is simple and I wanted to keep\ 
   the memory usage of the app at a minimum as this is runing in a docker container.

2. Decided that at the moment there is no need for using threads to read several csv files in parallel, althought\ 
   it may be an interesting avenue to explore given that most Python IO calls release the GIL.

3. Decided not to concentrate on eliminating parse errors for individual csv files, instead I tried to\
   provide robust logging of the errors, with details that would make it easy to chase the errors later.\
   There are several causes to these parsing failures: lacking headers, non-utf8 encodings,\
   improperly escaped separator characters... The code could be improved to deal with some of these issues but\
   time is a constrain.
   




 