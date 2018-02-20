#!/bin/ksh
basedir=$HOME
name=$(basename $0)
day=$(date +%d%m%y%H%M%S)
logname=$name.$day.log
cat >> $logname < /dev/null
summary=$basedir/assign/summary.txt

#############################################
###Repo which contains all of your CSV files
repo=$basedir/data/
#############################################
echo "basedir is $basedir"
cd $basedir/assign

if [ -e $summary ]
then
    rm -f $basedir/assign/summary.txt
    rm -f $basedir/assign/summary_out.csv
    echo "Files removed successfully" >> $logname
else
    echo "Cleanup unnecessary"
fi

if [ -e $basedir/assign/summary_out.csv ]
then
   rm -f $basedir/assign/summary_out.csv
fi

echo "Finding all *.csv files from repo"

echo "Repo path is $repo"
find $repo -iname '*.csv' > $summary
#find /home/ec2-user/data/investor-flow-of-funds-us/data/ -iname 'weekly.csv' > $summary
if [ $? -eq 0 ]
then
    echo "Find completed successfully"
else
    echo "Couldn't find any *.csv files"
fi

echo "FileName, TotalRecords, TotalFields, WordCount" >> summary_out.csv
while read filename
do
  #echo "Filename is $filename"
  #word_count=$(wc -w < $filename)
  awk '
       BEGIN{FS=",";OFS=",";w_c=0}
        {
         line=$0;
         gsub("," ," ", line);
         gsub("[:%?<>&@!=+.()]", "", line_wo_comma);
         w_c+=split(line, array, " ");
        }
       END{print FILENAME, FNR, NF, w_c >> "summary_out.csv" ;}
      ' $filename ;
 # echo $filename
done < $summary

  awk '
      BEGIN{
            print "Started Caculating stats";
			            FS=",";ACC_SUM=0;ACC_FIELDS=0
           }
           {if(NR>1)
                {
                  ACC_SUM+=$2;
                  ACC_FIELDS+=$3
                }
            }
      END{
          print "Total Files processed            : " NR-1 "\n",
                "Sum of records in all files      : " ACC_SUM "\n",
                "Average of no. of fields in files: " ACC_FIELDS/(NR-1)
         };' summary_out.csv


echo " Print all Contents of file "
cat summary_out.csv
