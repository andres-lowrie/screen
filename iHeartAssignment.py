#!/usr/bin/env python

'''Script Name :           iHeartAssignment.py

   Objective:              To Count the Rows,Average Fields and Word Frequency across all .csv files in subdirectories a root directory

   User Inputs Required :  User is requested to input the Root Directory and the OutPut File Directory

   Program Output:         The program would display the Total Number of Rows and Average  Number of Fields in the Console and write a file in the Output directory
                           OutPutFileName is specified as  Output_File_Word_Count.txt

   Assumptions Made:       1)Script has been tested and validated to execute on Windows Env.The Input for directories may need to be altered
                             slightly in case the script is executed on Unix Shell.
                           2)The files to be considered  for this assignment are only the ".csv" files
                           3)Each file may or may not have equal number of fields for all rows inside that specific file
                           4)Requested Word Frequency calculation is Case Sensitive .Eg:python adn Python would be considered separate words


   Execution Instructions:Please execute the below command to execute the python script and provide the inputs at the prompt

  Command to be executed : python iHeartAssignment.py

'''


# Importing Modules required for the script

import os
import csv
from collections import Counter


__author__ = "Sudipta Sengupta"
__version__='1.0'
__email__='sudipta.sengupta87@gmail.com'


## -----Start of the Main Function ------##
def main():

    ## ----Initializing Variables and the counter---##
    global wordcount
    wordcount= Counter()
    countFields=0
    countRows=0
    file_list=[]

    ##--Setting up the name of the Output File to be created --#
    outFile="Output_File_Word_Count.txt"

    ##--Invoking the Funtion Request_User_input to obtain user input for the root directory and the target directory--##


    sPath,outputFileName=Request_User_Input(outFile)

    ##--Invoking the function Identify_List_of_Files to get a list of all the files present inside the root directory--##

    file_list=Identify_List_of_Files(sPath,file_list)

    ##--Below code logic will loop through the files and identify the Total number of fields and rows across all the csv files--##

    for filename in file_list:
        if os.stat(filename).st_size > 0:
            Calculate_Word_Frequency(filename)
            file=open(filename)
            reader=csv.reader(file)
            for row in reader:
                countFields+=len(row)
                countRows+=1

    ##-- If the total Number of rows across all the files are grater than zero it will print out the  Total number of rows and teh average number of fields--##

    if countRows >0:
        with open(outputFileName,"w") as outputFile:
            outputFile.write("Words" + ' \t '+ "Frequncy" + '\n')
        Write_Word_Count_to_File(outputFileName)
        averageNumFields=int(countFields/countRows)
        print("Total Number of Rows = {}".format(countRows))
        print("Average Number of Columns = {}".format(averageNumFields))
    else:
        print("No records present in the files in the root directory")

##End Of Main##

## --Start of Function Definitions --##

def Identify_List_of_Files(sPath,file_list):

    '''Recursively loop through the directories and append the fully qualified file names to the list and then return the list  containing the files'''

    for sChild in os.listdir(sPath):
        sChildPath=os.path.join(sPath,sChild)
        if os.path.isdir(sChildPath):
            Identify_List_of_Files(sChildPath,file_list)
        else:
            if sChildPath[-3:]=='csv':
                file_list.append(sChildPath)

    return file_list


def Calculate_Word_Frequency(filename):

    '''Calculate the word frequency and store it in the dictionary as key value pair'''

    value=" \n"
    with open(filename) as inputFile:
         for line in inputFile:

             for word in line.split(','):
                 wordcount[word.strip(value)] += 1



def Write_Word_Count_to_File(outputFileName):

    '''Write the Word counts from the dictionary to the Output Directory'''

    with open(outputFileName,"a") as outputFile:
         for k,v in wordcount.items():
             outputFile.write(str(k) + ' \t '+ str(v) + '\n')


def Request_User_Input(outFile):

    '''Request User input in the specific format'''

    checkFlag=1
    print("\n*****iHeart Assignment *****\n")
    print("Please provide the rquested inputs in the specified formates mentioned below : \n")
    print('Please use double slashes for the directory instead of single slahes to ensure we avoid issues due to escape characters --\n')
    print('Sample Input Pattern::  C:\\\\Users\\\\aviss\\\\Desktop\\\\iHeart\\\\ ')
    print('==============================================================================')

    while(checkFlag):
          print("Input the Root Directory which contains the csv files in the specified format below---")
          sPath=input()
          if os.path.isdir(sPath):
              checkFlag=0
          else:
             print("Please try again ..The input is not a directory")

    while(checkFlag==0):
         print("\nInput the Target Directory in which the output needs to be written in the specified format below---")
         tPath=input()
         if os.path.isdir(tPath):
             checkFlag=1
             outputFileName=tPath+outFile
         else:
             print("Please try again . The input is not a directory\n")


    return sPath,outputFileName




if __name__=='__main__':
    main()

