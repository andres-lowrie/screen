# Solution
 
 - Building docker image will execute the code
 - Two output files generated are :
 
	 1. ***/root/code/output*** - contains result for average total fields and total count
	 2. ***/root/code/word_count.csv*** -  contains result for word count
 - Command to see result
	 1. cat /root/code/output
	 2. cat /root/code/word_count.csv
	 
	### Assumptions
	- considered all the .csv files as valid and comma separated
	-	considerd all the csv file for processing ( csv files present both in archive directory and data directory). If we need some specific file the code can be very quickly and easily modified.
	-	For word count problem, was not clear on the meaning of every value ( so have counted frequency of each word in csv, except word in header row)
	-	Excluded header in while computing total count.
  
  
# Instructions

> Build this docker image
> Run `bash` as the command with an iteractive tty to get into the image:

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
