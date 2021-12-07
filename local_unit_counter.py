# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:41:51 2021
Author: Adam Coxson, PhD, The University of Liverpool
Department of Chemistry, Materials Innovation Factory, Levershulme Research Centre
Project: 
Module: 
Dependancies: 
"""

import numpy as np
import csv

########## FUNCTIONS #########

def time_to_sec(t):
   h, m, s = map(int, t.split(':'))
   return h * 3600 + m * 60 + s

def file_reader(filename, n_header_rows=1, delimiter=','):

    filename = "rpt_cleaned.csv"
    with open(filename, 'r') as f:
        data = list(csv.reader(f, delimiter=delimiter))
    data = np.array(data[n_header_rows:]) # slice data from 1:end to get rid of header
    return data

def write_to_csv(filename, data, header=None):
    """
    Writes data to csv with option for header.
    Note use terminator=os.linesep for linux systems, '\n' is windows excel csv default

    Parameters
    ----------
    filename : str
        filename or filepath.
    data : ndarray
        list of data in row/col format.
    header : list of str
        a single string for each column headr.

    Returns
    -------
    None.

    """
    writer = csv.writer(open(filename,'w'),lineterminator ='\n')
    if header != None:
        writer.writerow(header)
    writer.writerows(data)
    print("Written to",filename,"successfully.")
    return None


############ MAIN ############

filename = "rpt_cleaned.csv"
raw_data = file_reader(filename=filename,n_header_rows=1)

# Removing player timestamps
player_stamp_idx = [] 
for i in range(1,len(raw_data)):
    #print(data[i][1])
    val = raw_data[i][1]
    if val != 'Server' and val != 'HC1' and val != 'HC2':
        player_stamp_idx.append(i)


data = np.delete(raw_data,player_stamp_idx,axis=0)
time_s = np.copy(data[:,0])
for i in range(len(time_s)): time_s[i]=time_to_sec(time_s[i])

# Grouping indexes of timestamps within desired time_gap tolerance
i=0
j=0
group_list =[]
group_line = [i]
end_of_file = False
time_gap = 30

while end_of_file == False: # This while loop is the complicated bit

    if j+1 == len(time_s): # End of data condition
        end_of_file = True
        group_list.append(group_line) # making sure to add the last group on
    elif int(time_s[j+1])-int(time_s[i]) <= time_gap: # If next point at j+1 is within timegap, add to group, where j= i+1 or i+2 or i+3.. 
        group_line.append(j+1)
        j=j+1
    elif int(time_s[j+1])-int(time_s[i]) > time_gap: # If next point is not within time gap of first timestamp, reset and start from that point
        group_list.append(group_line) 
        i=j+1 # Resetting the counter to start from new datapoint that is not within the timegap of the old group
        j=j+1
        group_line = [i] # reset group with current point as first element, the rest will be appended on next iteration 
    else:
        print("Something fucked up man")
        
# Using groupings to assign formatted data
formatted_data = np.zeros(shape=(len(group_list),5)).astype(str) # N rows 4 cols for time, HC1, HC2, Server, total
for i in range(len(group_list)):
    idx = group_list[i]
    formatted_data[i][0] = data[idx[0],0]
    total =0
    for j in range(0,len(idx)):
        total=total+int(data[idx[j],3])
        if data[idx[j],1] == "HC1":
            formatted_data[i][1] = data[idx[j],3]
        elif data[idx[j],1] == "HC2":
            formatted_data[i][2] = data[idx[j],3]
        elif data[idx[j],1] == "Server":
            formatted_data[i][3] = data[idx[j],3]
        else:
            print("bzz bzz, I'm a bug")
    formatted_data[i][4] = total
        
        
write_to_csv(filename="local_unit_data.csv",data=formatted_data,header=["Server Time","HC1","HC2","Server","Total"])
        
    
    