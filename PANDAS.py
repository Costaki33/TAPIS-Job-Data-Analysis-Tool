import json
import logging
from typing import List
import socket
import numpy as np
import math
import pandas as pd
from datetime import timedelta 
import datetime
import mysql.connector as msql
from mysql.connector import Error
import os 




def main():


    path = '/home/ubuntu/job-times'

    #for file in os.listdir():
     #   if file.endswith('.txt'):
     #       file_path = f'{path}\{file}'

# JobID|User|Account|Start|End|Submit|Partition|Timelimit|JobName|State|NNodes|ReqCPUS|NodeList

    #userInput = input('Please enter the file name you would like to analyze: ')

# Generates a 2D list of the read in data for each line that is stored in a mainList

    #readIn = open(userInput) # <- keep!
    readIn = open('test_file.txt', 'r')
    df = pd.read_csv(readIn, delimiter = '|') # Now in a DataFrame (table with rows and columns)


# Saves the dataframe to a .CSV file     
    df.to_csv('my_new_file.csv', index = None) # <- Saves the dateframe to a .CSV file 
    df_saved_file = pd.read_csv('my_new_file.csv')
        

    # Need to recreate dataframe where the START, END, and SUBMIT times are converted into datetime, then I can subtract 
    #['JobID', 'User', 'Account', 'Start', 'End', 'Submit', 'Partition', 'Timelimit', 'JobName', 'State', 'NNodes', 'ReqCPUS', 'NodeList']
    #"days-hours:minutes:seconds"
    df['Start'] = pd.to_datetime(df['Start'], format = '%Y-%m-%dT%H:%M:%S')
    df['Submit'] = pd.to_datetime(df['Submit'], format = '%Y-%m-%dT%H:%M:%S')
    df['End'] = pd.to_datetime(df['End'], format = '%Y-%m-%dT%H:%M:%S')
     
    #df['Timelimit'] = pd.to_datetime(df['Timelimit']).dt.strftime('%d-%H:%M:%S')
    #df['Timelimit'] = pd.to_datetime(df['Timelimit'], format = '%H:%M:%S', errors='ignore').astype('datetime64[D]')   
     
    #df['format'] = 1
    #df.loc[df.date.str.contains('-'), 'format'] = 2
    #df['new_date'] = pd.to_datetime(df.date)
    #df.loc[df.format == 1, 'new_date'] = pd.to_datetime(df.loc[df.format == 1, 'date'], format = '%d-%H:%M:%S').dt.strftime('%d-%H:%M:%S')
    #df.loc[df.format == 1, 'new_date'] = pd.to_datetime(df.loc[df.format == 1, 'date'], format = '%H:%M:%S').dt.strftime('%d-%H:%M:%S') 

    print(df)   
       
#    userJobID = input('\nPlease enter the job ID you would like to calculate the queue time for: ')
#    userJobID = np.int64(userJobID) # <- need to convert to match the other data types in the DataFrame
    
    
#    found_ID_location = df.loc[df['JobID'] == userJobID]  # <- finds the row that has the jobID from the user
#    userInput_index = found_ID_location.index.values
    #print(userInput_index)
    df.to_csv('my_new_file.csv', index = None)
    df_saved_file = pd.read_csv('my_new_file.csv')    
    

 # Need to implement the parsing of the data for the column and so on 
 
    # start = df.loc[userInput_index, 'AnyKey']
    #start = df.loc[userInput_index, 'Start']
    #submit = df.loc[userInput_index, 'Submit']
 
    #result = start - submit       
    
    #print('Delta queue time: ', result.total_seconds())
       


if __name__ == '__main__':
    main()
