import numpy as np
import glob
import argparse
import collections
import time
import datetime
import sys

def every_count(count_dict, count_list):

    temp_dict = collections.Counter(count_list)
    temp_keys = temp_dict.keys()
    for key in temp_keys:
        if key in count_dict:
            count_dict[key] = count_dict[key] + temp_dict[key]
        else:
            count_dict[key] = temp_dict[key]

def confirm_date(date, start, end):

    d = datetime.datetime.strptime(date, "%d/%b/%Y")
    sub_start = d - start
    sub_end = end - d


    if sub_end.days >= 0 and sub_start.days >= 0:
        return False
    else:
        return True
    
    


parser = argparse.ArgumentParser()
parser.add_argument("--start_date", default="", type=str, help="write [year_month_day]")
parser.add_argument("--end_date", default="", type=str, help="write [year_month_day]")
args = parser.parse_args()

t1 = time.time()
access_log_list = glob.glob("./*access_log*.txt")
host_count_dict = {}
host_count_list = []
time_count_dict = {}
time_count_list = []

date_flag = False

if len(args.start_date) > 0 or len(args.end_date):
    try:
        start = datetime.datetime.strptime(args.start_date, "%Y_%m_%d")
        end = datetime.datetime.strptime(args.end_date, "%Y_%m_%d")
        date_flag = True
        print("search {}/{}/{} ~ {}/{}/{} accesses".format(start.year, start.month, start.day, end.year, end.month, end.day))
    except ValueError as Ve:
        print("catch ValueError::Your input is incorrect [year_month_day]. Search all accesses.",Ve)

else:
    print("search all accesses")

t1 = time.time()
append = host_count_list.append
for i in range(5):
    for access_log in access_log_list:

        with open(access_log, mode="r") as f:
                        
            for line in f:
                line_split = line.split(" ")
                date_split = line_split[3][1:].split(":")
                
                if date_flag and confirm_date(date_split[0], start, end):
                    continue
                
                append((date_split[0],date_split[1],line_split[0]))
                
                    

                if sys.getsizeof(host_count_list) > 500000000:
                    if not host_count_dict:
                        host_count_dict = collections.Counter(host_count_list)
                    else:
                        every_count(host_count_dict, host_count_list)
                    host_count_list.clear()

every_count(host_count_dict, host_count_list)

t2 = time.time()
print("processing time",t2-t1)

for host, count in sorted(host_count_dict.items(), key=lambda x:(x[0][0], x[0][1], -x[1])):
    print(host,count)
