# Instructions

- Build this docker image
- Run `bash` as the command with an iteractive tty to get into the image:

```
docker run --rm -it ${whatever-you-named-the-image} /bin/bash
```

- The data is in the directory `/root/data` on said image
- Create a Pull Request with your code for review

> **You're free to use whatever language you want just as long as you include the instructions on how to run your code. (Bonus points if you modify the `Dockerfile` instead)**
>
> Note that you **do not** have to use a _Big Data_ stack like Hadoop or Spark. If you do use those, provide either a [docker-swarm](https://docs.docker.com/compose/) or [kubernetes](https://kubernetes.io/) configuration file(s) in your Pull Request that will setup the cluster or else we won't be able to run the code


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

# Answers

## Q1

During building the docker image using `docker build -t <DOCKER_IMAGE_NAME> .` the answer of this question would be printed.

## Q2

During building the docker image, the name of the CSV file in which all the values and their counts are stored, would be displayed.
In order to get access to the output file, you can get access to a running container and find the output file using:

- `docker run --rm -it <DOCKER_IMAGE_NAME> /bin/bash`

Also, if you would like to pull the output file from your running container, you can run:

- `docker cp <CONTAINER_ID>:/root/<OUTPUT_FILE>.csv /path/to/store/locally`

## Q3

During building the docker image, the answer of this question would be printed.
