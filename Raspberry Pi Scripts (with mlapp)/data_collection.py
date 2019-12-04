import requests
import json
import random
import serial
import RPi.GPIO as gp
import time
from datetime import datetime
import sys
import csv

# def random_generator():
#     data = {
#     "temp": round(random.uniform(0,40),2),
#     "pres": round(random.uniform(90000,100000),2),
#     "co": int(random.uniform(0,10)),
#     "lpg": int(random.uniform(0,10)),
#     "smoke": int(random.uniform(0,10))
#     }
#     return data

try:
    ser=serial.Serial("/dev/ttyACM1",9600)
except:
    ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

gp.setmode(gp.BOARD)
smell_class = input("Enter Smell Class: ")
rows = list()
x = 1
for i in range(1,101):
    if x>60:
        x = 1
    try:
        read_ser=ser.readline()
        temp_string = read_ser.decode('utf-8')
        temp_data = eval(temp_string[:-2])
        # temp_data = random_generator()
        temp_data["time"] = x
        data = {
        "time":temp_data["time"],
        "temp":temp_data["temp"],
        "pres":temp_data["pres"],
        "co":temp_data["co"],
        "lpg": temp_data["lpg"],
        "smoke": temp_data["smoke"]
        }
        print(data)
        rows.append(data)
        x += 1
        time.sleep(1)
    except:
        print("Try Again")
now = int(datetime.timestamp(datetime.now()))
keys = rows[0].keys()
with open(str(smell_class)+'_'+str(now)+'.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(rows)
    print(str(smell_class)+'_'+str(now)+'.csv')
