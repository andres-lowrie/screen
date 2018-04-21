#!/bin/bash

filecounter=0
headercounter=0
linecounter=0
for subdirectory in /root/data/**/data/*.csv
do
        num_of_lines=$(wc -l "$subdirectory" | head -n1 | cut -d " " -f1)
        linecounter=$((num_of_lines+$linecounter))
        count=$(sed -n 1p $subdirectory | tr ',' '\n' | wc -l)
        headercounter=$(($headercounter+$count))
        ((filecounter++))
done
avg_num_fields=$(($headercounter/$filecounter))
echo Average number of fields across all the csv
echo $avg_num_fields
echo Total Number of row for the all csv files
echo $linecounter
