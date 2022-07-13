import json
import logging
from typing import List 
import socket
import numpy as np 
import math 
import pandas as pd 
from datetime import datetime 

def main():

    MIN_IN_A_DAY = 1440

# JobID|User|Account|Start|End|Submit|Partition|Timelimit|JobName|State|NNodes|ReqCPUS|NodeList

    userInput = input('Please enter the file name you would like to analyze: ')

# Generates a 2D list of the read in data for each line that is stored in a mainList 
    mainList = []
    readIn = open(userInput)
    #readIn = open('test_file.txt', 'r')
    next(readIn) # -> ignores the first line that has the description of what each data slot is 
    print('\nJob Dataset List: \nJobID|User|Account|Start|End|Submit|Partition|Timelimit|JobName|State|NNodes|ReqCPUS|NodeList\n')
    for line in readIn: # line is each line in the read in script
        temp = line.split('|') # parsing from the pipe 
        mainList.append(temp)
    rows = len(mainList)
    for x in mainList:
        for j in x:
            print(j, end = "|")    
        print()

# Access the Queue time of all the data and store it in a list 
    queueTimeList = [None]*len(mainList)
    generalStrtTimeList = [] # list of the start times that's appended from the .split list that is created -> holds [['2022-04-05', '15:32:09'], ['2022-04-03', '00:08:19'], ['2022-04-03', '00:09:51']]
    generalSubmitTimeList = []
    for i in range(len(mainList)):
        strt = mainList[i][3] # Both times are strings
        submit = mainList[i][5]


        strt_date = strt.split('T')
        submit_date = submit.split('T')

        generalStrtTimeList.append(strt_date) # Start time list:  [['2022-04-05', '15:32:09'], ['2022-04-03', '00:08:19'], ['2022-04-03', '00:09:51']]
        generalSubmitTimeList.append(submit_date)
    #print('\nGeneral Submit Time List: ', generalSubmitTimeList, '\nGeneral Start Time List: ', generalStrtTimeList)
    # General Submit Time List:  [['2022-01-19', '03:24:45'], ['2022-03-29', '21:34:12'], ['2022-03-29', '21:34:43']]
    # General Start Time List:  [['2022-04-05', '15:32:09'], ['2022-04-03', '00:08:19'], ['2022-04-03', '00:09:51']]
    '''

        NNodes = 0 # [10]
        ReqCPUS = 0 # [11]

        NNodes_tmp = mainList[i][10]
        ReqCPUS_tmp = mainList[i][11]

        NNodes = int(NNodes_tmp)
        ReqCPUS = int(ReqCPUS_tmp)
        print('\nNNodes = ', NNodes, ' <- type: ', type(NNodes))
        print('\nReqCPUS = ', ReqCPUS, ' <- type: ', type(ReqCPUS))

    '''

# Creates a 2D list that has the time of the inputted START TIME dataset 
    actualStartTime = []
    dateTime_STRT = []
    for i in range(len(generalStrtTimeList)): 
        temp_time = generalStrtTimeList[i][1]
        temp_date = generalStrtTimeList[i][0]
        start_time = temp_time.split(':')
        start_date = temp_date.split('-')
        actualStartTime.append([int(x) for x in start_time]) # coverts the string sequence of HR | MIN | SEC to their respective integer values  
        dateTime_STRT.append([int(y) for y in start_date])
    #print('\nAppended Start Date List: ', dateTime_STRT)

# Creates a 2D list that has the time of the inputted SUBMIT TIME dataset
    actualSubmitTime = []
    dateTime_SUBMIT = []
    for i in range(len(generalSubmitTimeList)):
        temp_time = generalSubmitTimeList[i][1]
        temp_date = generalSubmitTimeList[i][0]
        submit_time = temp_time.split(':')
        submit_date = temp_date.split('-')
        actualSubmitTime.append([int(x) for x in submit_time]) # coverts the string sequence of HR | MIN | SEC to their respective integer values
        dateTime_SUBMIT.append([int(y) for y in submit_date])
    #print('\nAppended Submit Date List: ', dateTime_SUBMIT)

# OVERALL QUEUE CALCS
# Checks to see if the job was in queue for more than a day -> if so, add that time to the total time of the submit/start time
# if it was submitted and started in a day, no need to add that difference 
    month_start = 0
    day_start = 0
    month_submit = 0
    day_submit = 0
    queueTime = 0.0  
# Calculates the Queue time 
# Convert the time to minutes 
    for i in range(len(actualSubmitTime)):     
        actualSubmitTime[i][0] = (actualSubmitTime[i][0] * 60)
        actualStartTime[i][0] = (actualStartTime[i][0] * 60)
    
    # Takes the user input for the job ID, will look up the 
    userJobID = input('\nPlease enter the job ID you would like to calculate the queue time for: ')
    
    for rows in range(0, len(mainList)):
        if userJobID.lower() in [str(x).lower() for x in mainList[rows]]:
            print('\nSuccess! Found valid Job ID!')
            IDrow = rows # -> this value will be used to call in the Submit/Start 2d Time lists the time corresponding to the row that is related to the job ID 
            
            month_start = dateTime_STRT[IDrow][1]
            day_start = dateTime_STRT[IDrow][2]

            month_submit = dateTime_SUBMIT[IDrow][1]
            day_submit = dateTime_SUBMIT[IDrow][2]
            year_submit = dateTime_SUBMIT[IDrow][0]

    total_submit_time = ((actualSubmitTime[IDrow][0]) + (actualSubmitTime[IDrow][1]) + (actualSubmitTime[IDrow][2] / 60))
    total_start_time = ((actualStartTime[IDrow][0]) + (actualStartTime[IDrow][1]) + (actualStartTime[IDrow][2] / 60))

    # Now go directly to the Start/Submit time and PULL the times and add them together

    for rows in range(0, len(mainList)):  
        if month_submit == month_start:
            print('\nSame month job was started as it was submitted! Continue ->')
            if day_submit == day_start: # works! 
                print('\nJob was started on the same day! Continue->')
                print('\nTotal Start Time: ', total_start_time)
                print('\nTotal Submit Time: ', total_submit_time)
                queueTime = total_start_time - total_submit_time
                print('\nQueue Time for job: ', queueTime)
                break 
            else: # This else statement if the job was in queue in the SAME month, didn't change months
                print('\nJob was in queue longer than a day')
                dlta_time_left_in_day_SUBMIT = (MIN_IN_A_DAY - total_submit_time) # delta time left in a day before the next day starts for submit time 
                print('\nDelta time left in Submit date: ', dlta_time_left_in_day_SUBMIT)
                dlta_days_into_time = ((day_start - day_submit) - 1) * MIN_IN_A_DAY
                print('\nDelta Days between start and submit time: ', dlta_days_into_time)
                print('\nTotal Start Time: ', total_start_time)
                queueTime = 0.0
                queueTime = dlta_days_into_time + dlta_time_left_in_day_SUBMIT + total_start_time
                print('\nQueue Time for job: ', queueTime)
                break
        
        else:
            if(month_submit == 1 or month_submit == 3 or month_submit == 5 or month_submit == 7 or month_submit == 8 or month_submit == 10 or month_submit == 12):
                
                print('\nThere are 31 Days in this month -> ', month_submit)
                days_left_in_month = 31 - day_submit
                
                dlta_time_left_in_day_SUBMIT = (MIN_IN_A_DAY - total_submit_time)
                
                dlta_time_left_in_month = (days_left_in_month) * MIN_IN_A_DAY
                
                rest_of_submit_month_time = dlta_time_left_in_month + dlta_time_left_in_day_SUBMIT 

                # Now for the new month
                adjusted_start_day_val = day_start - 1
                days_to_time_NM = (adjusted_start_day_val * MIN_IN_A_DAY) + total_start_time

                queueTime = rest_of_submit_month_time + days_to_time_NM
                print('\nQueue time for job that transfered over a new month that has 31 days in it: ', queueTime)
                break 
            if(month_submit == 2):
                if(year_submit % 4 == 0):
                    days_left_in_month = 29 - day_submit                
                    print('\nWow! It\'s a leap year!')
                else:
                    days_left_in_month = 28 - day_submit
                    print('\nIt\'s a normal Feburary!')
                dlta_time_left_in_day_SUBMIT = (MIN_IN_A_DAY - total_submit_time)

                dlta_time_left_in_month = (days_left_in_month) * MIN_IN_A_DAY

                rest_of_submit_month_time = dlta_time_left_in_month + dlta_time_left_in_day_SUBMIT

                # Now for the new month
                adjusted_start_day_val = day_start - 1
                days_to_time_NM = (adjusted_start_day_val * MIN_IN_A_DAY) + total_start_time

                queueTime = rest_of_submit_month_time + days_to_time_NM
                print('\nQueue time for job that transfered over Feburary: ', queueTime)
                break

            else:
                days_left_in_month = 30 - day_submit

                dlta_time_left_in_day_SUBMIT = (MIN_IN_A_DAY - total_submit_time)

                dlta_time_left_in_month = (days_left_in_month) * MIN_IN_A_DAY

                rest_of_submit_month_time = dlta_time_left_in_month + dlta_time_left_in_day_SUBMIT             

                # Now for the new month
                adjusted_start_day_val = day_start - 1
                days_to_time_NM = (adjusted_start_day_val * MIN_IN_A_DAY) + total_start_time

                queueTime = rest_of_submit_month_time + days_to_time_NM
                print('\nQueue time for job that transfered over a new month that has 30 days in it: ', queueTime)
                break
    #print('\nStored Queue Time value: ', queueTime)
    
    # Statistical Analysis 
    # The partition is the queue that was requested, e.g., "normal", "small", etc
    '''
    JobID|User|Account|Start|End|Submit|Partition|Timelimit|JobName|State|NNodes|ReqCPUS|NodeList
    4221134|tg840985|phy20012|2022-04-07T11:09:50|2022-04-08T07:50:34|2022-04-07T06:00:03|rtx|1-00:00:00|glidein|COMPLETED|1|16|c196-061
    '''  





if __name__ == '__main__':
    main()
