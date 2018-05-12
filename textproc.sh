#!/bin/bash

tempFile="stage.tmp"
outTemp="output.tmp"
finalOut1="output-method1.txt"
finalOut2="output-method2.txt"

rm -f $tempFile $outTemp

find /root/data -type f -name '*.csv' -exec sed -i 's||\n|g' {} +

find /root/data -type f -name '*.csv' -exec head -n 1 {} + | 
	grep -v '==>' | grep  -v '^$'| 
	awk -F ',' '{fc+=NF}END{avg=fc/NR; avg = avg%1 ? int(avg)+1:avg;printf("Total Fields %d \n Total Number of Files %d \n Average Number of fileds %d\n",fc, NR,avg);}'

totalLines=$(find /root/data -type f -name '*.csv' -exec cat {} + | wc -l)

echo " Total Lines "${totalLines}

tot_lines=0;

for line in $(find /root/data -type f -name '*.csv'); do
#find . -type f -name '*.csv' -print0 | while IFS= read -r -d $'\0' line; do
#	echo $line
	curr_lines=$(wc -l < $line)
#	echo $line "==> "$curr_lines
	tot_lines=$((curr_lines + tot_lines))
	awk -F ',' -v tempFile=${tempFile} '{for(w=1;w<=NF;w++) {gsub(/[ ,\t]*/,"",$w);arr[$w]+=1;}}END{for (key in arr) {print key"|"arr[key] >> tempFile}}' $line
done

echo " Total Lines from Loop ==> "$tot_lines

awk -F '|' -v outTemp=${outTemp} '{ arr[$1]+=$2;}END{for (key in arr) {print key","arr[key] >> outTemp }}' $tempFile 

echo "Value,Count" > $finalOut1
sort -t "," -k 2,2nr $outTemp >> $finalOut1

rm -f $outTemp

head -10 $finalOut1 | cat -n

echo "Method 2"

#find . -name '*.csv' -exec awk -F ',' -v outTemp=${outTemp} '{for(w=1;w<=NF;w++) {gsub(/ */,"",$w);arr[$w]+=1;}}END{for(key in arr){printf("%s|%s",key,arr[key])>>outTemp;}}' {} +

find /root/data -name '*.csv' -exec awk -F ',' -v outTemp=${outTemp} '{for(w=1;w<=NF;w++) {gsub(/[ ,\t]*/,"",$w);arr[$w]+=1;}}END{for(key in arr){printf("%s,%s\n",key,arr[key])>>outTemp;}}' {} +

echo "Value,Count" > $finalOut2
sort -t "," -k 2,2nr $outTemp >> $finalOut2

head -10 $finalOut2 | cat -n
