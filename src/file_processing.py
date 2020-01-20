from functools import reduce
import csv


class CSV_Proc:

    def __init__(self,wdCntDict,total):
        self.total = total
        self.wdCntDict = wdCntDict

    def col_count(self,col_list):
        #get an average of column numbers over all files
        answer = 0
        count = 0
        total = 0
        for x in col_list:
        
            try:
                #open the file and read first line
                with open(x,'r',errors='ignore') as csvfile:
                    count +=1
                    total += len(csvfile.readline().split(','))
        
            except Exception as e:
                print(e)
        
            try:
                answer = total/count
            except Exception as e:
                print(e)
        
        return answer


    def process_file(self,col_list):
        #iterate through file name list
        for x in col_list:
            try:
                #use generator so that we don't have to load the whole csv into memory, yield one row at a time
                with open(x, "r",errors='ignore') as email_records:
                    for email_record in csv.reader(email_records):
                        yield email_record       
        
            except Exception as e:
                print(e)
        
  

    def write_dict(self,wdDict,file_out):
        #write outputs to a file
        csv_columns = 'value,count'
        
        try:
            with open(file_out, 'w') as f:
                f.write(csv_columns+'\n')
                for key in wdDict.keys():
                    f.write("%s, %s\n" % (key, wdDict[key]))

        except IOError:
            print("I/O error")
