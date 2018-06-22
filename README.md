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

# Executing Solution

- Build this docker image
- Run `bash` as the command with an iteractive tty to get into the image:

```
docker run --rm -it ${whatever-you-named-the-image} /bin/bash
```

Execute jar

```
java -jar screen-1.0-SNAPSHOT.jar data/
```

Solution 1 and 3 will be printed to the console. Solution 2 is written to file `solution2.csv`. The argument `data/` can be another data directory. 

Notes: 

I was unsure at the time I started working on this if I had a choice of language and made the executive decision to write it in Kotlin. Unfortunately 
when I started I was working off of an assumption of JDK 8 being available which wasn't readily available without adding other apt-get sources in the Debian jessie 
docker image so I upgraded it to the buster version. I'm hoping for correctness as I wrote the bare minimum amount of testing which if this was an application
would be much more in depth. The Dockerfile currently clones the repo from my fork path which if it were to be an accepted merge it should be pointing to `andres-lowrie/screen
`.
