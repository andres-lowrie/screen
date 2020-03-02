import os
import re
import logging
from collections import Counter

import pandas as pd
from tqdm import tqdm

class i_heart_media:
    """
    This class defines all the methods used in this assignment
    """
    def __init__(self):
        self.csv_files_list=[]
        self.total_fields_count=0
        self.total_row_count=0
        self.count_bad_files=0
        self.combined_word_count={}
    
    def get_csv_files(self, path):
        """
        :param: directory where all the csv files are saved
        :return: number of csv files found in the passed parameter
        """
        for root, dirs, files in os.walk(path):
            [self.csv_files_list.append(os.path.join(root, file_name)) for file_name in files if file_name.endswith('.csv')]
        csv_files_count=len(self.csv_files_list)
        return csv_files_count

    def combine_columns_into_one(self, file_data):
        """
        :param: dataframe
        :return: new dataframe with only one column having data from all the columns
        """
        file_data['New'] = file_data[file_data.columns[:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis = 1)
        return file_data[['New']]
    
    def convert_column_to_list(self, file_data):
        """
        :param: dataframe
        :return: list of same size as number of rows in dataframe passed in the parameter
        """
        single_file_combined_column=[]
        for i in range(file_data.shape[0]):
            single_file_combined_column.append(file_data.loc[i][0])
        return single_file_combined_column
    
    def split_each_element_in_list(self, single_file_combined_column):
        """
        :param: list
        :return: new list with each word separate into one element of the list
        """
        return ' '.join(single_file_combined_column).split()
    
    def create_word_dict(self, single_file_combined_list):
        """
        :param: list
        :return: dictonary of only those list elements which contain a letter
        """
        single_file_word_count={}
        for i in single_file_combined_list:
            if i in single_file_word_count.keys() and re.search('[a-zA-Z]', i):
                single_file_word_count[i]+=1
            elif i not in single_file_word_count.keys() and re.search('[a-zA-Z]', i):
                single_file_word_count[i]=1
        return single_file_word_count
    
    def read_csv_files(self):
        """
        :param: class instance only
        :return: none
        """
        for file_name in tqdm(self.csv_files_list): 
            try:
                file_data = pd.read_csv(file_name)
            except UnicodeDecodeError as e:
                file_data = pd.read_csv(file_name, encoding='latin-1')
            except (pd.errors.ParserError) as e:
                logging.warning(f'{file_name} skipped because of parsing error')
                self.count_bad_files+=1
            except (pd.errors.EmptyDataError) as e:
                logging.warning(f'{file_name} skipped because it is empty')
            num_fields = len(file_data.columns.values)
            self.total_fields_count+=num_fields
            file_row_count = file_data.shape[0]
            self.total_row_count+=file_row_count
            file_data = self.combine_columns_into_one(file_data)
            single_file_combined_column = self.convert_column_to_list(file_data)
            single_file_combined_list = self.split_each_element_in_list(single_file_combined_column)
            single_file_word_count = self.create_word_dict(single_file_combined_list)
            self.combined_word_count = Counter(self.combined_word_count) + Counter(single_file_word_count)
    
    def answer_question_1(self, csv_files_count):
        """
        :param: total csv files
        :return: none
        """
        print(f'Average number of fields across all the .csv files: {self.total_fields_count//(csv_files_count-self.count_bad_files)}')
    
    def answer_question_2(self, file_path, file_name):
        """
        :param: file path and name to save the file
        :return: none
        """
        combined_word_count_dict = dict(self.combined_word_count)
        word_count_df = pd.DataFrame.from_dict(combined_word_count_dict, orient='index').reset_index().rename(columns={'index': 'value', 0: 'count'})
        word_count_df.to_csv(os.path.join(file_path, file_name), index=False)
    
    def answer_question_3(self):
        """
        :param: class instance only
        :return: none
        """
        print(f'Total number of rows for all the .csv files: {self.total_row_count}')

ihm = i_heart_media()
csv_files_count = ihm.get_csv_files(r'/root/data')
ihm.read_csv_files()
 
ihm.answer_question_1(csv_files_count)
ihm.answer_question_2(r'/root', 'word_count_dataset.csv')
ihm.answer_question_3()
