
- Added a python script to solve the Questions mentioned in the Instructions README file.
- Edited the DockerFile to copy the python script python_docker.py to docker container on build.
- To build the container execute the following;
	$docker build -t <image-name> .
- It will install the relevant python packages
- To run execute the following;
docker run -it --rm <image-name>
- You can see the output displayed in the following format;
---------------------------------
Average number of columns:
---------------------------------
10
---------------------------------
Writing value-count pairs to words.csv file..
Done writing to words.csv
---------------------------------
Total number of rows:
---------------------------------
1654156
---------------------------------

-Below is my interpretation of the Questions and the logic I have applied to get the answers;

## what's the average number of fields across all the `.csv` files?
>> Wrote a python method to recursively search for .csv files inside sub-directories and count the number of fields in each file and calcuate the average.

## create a csv file that shows the word count of every value of every dataset (dataset being a `.csv` file)
>> Writing to a .csv file on the container. The file is called "words.csv" which contains key value pairs of "value-count".
The python code for this question does counts the column names as well.

## what's the total number or rows for the all the `.csv` files?
>> Recursively reading and counting the number of lines in each .csv file. I am executing this script before creating the words.csv file in 
Question 2, just to avoid counting the lines from this output file in my total.
