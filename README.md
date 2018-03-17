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
_command to generate the average number of fields_
```
file_cnt=`find . -name '*.csv'|wc -l`;for file in `find . -name '*.csv'`;do cat $file|perl -pe 's/\r(?!\n)/\r\n/g'|head -n 1;done|perl -wnlp -e 's/\t/,/g;'|perl -pe 's/,/\n/g' |sort |uniq -c |awk '{$1=$1};1'|sed 's/ /|/1'|awk -F $'|' ' { t = $1; $1 = $2; $2 = t; print; } ' OFS=$','|sed 's/^M//g'|awk -F "\"*,\"*" '{print $2}'|awk '{s+=$1} END {print s}'|{ bc | tr -d '\n' ; echo ",$file_cnt"; }|awk -F $',' ' { printf("%.0f\n", $1/$2) } '
```
Note: Above command needs to be executed in root/data directory

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

_command to generate word count of CSV files excluding header_
```
echo "value,count" > wordcount.dat ; for file in `find . -name '*.csv'`;do cat $file|perl -pe 's/\r(?!\n)/\r\n/g'|tail -n +2;done|perl -wnlp -e 's/\t/,/g;'|perl -pe 's/,/\n/g' |sort |uniq -c |awk '{$1=$1};1'|sed 's/ /|/1'|awk -F $'|' ' { t = $1; $1 = $2; $2 = t; print; } ' OFS=$',' >> wordcount.dat
```

Note: Output is stored in wordcount.dat in root/data directory; Perform vi wordcount.dat or cat wordcount.dat in the command line to view the output

## what's the total number or rows for the all the `.csv` files?

output should be a simple number

_sample output_

```
1000000000
```

_command to generate total number rows in all CSV files excluding header_

```
for file in `find . -name '*.csv'`;do cat $file|perl -pe 's/\r(?!\n)/\r\n/g'|tail -n +2;done|wc -l
```
