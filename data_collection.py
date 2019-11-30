import requests
import json
import random
import serial
import RPi.GPIO as gp
import time
from datetime import datetime
import pandas as pd
import sys

def random_generator():
    data = {
    "temp": round(random.uniform(0,40),2),
    "pres": round(random.uniform(90000,100000),2),
    "co": int(random.uniform(0,10)),
    "lpg": int(random.uniform(0,10)),
    "smoke": int(random.uniform(0,10))
    }
    return data

def log_generator():
    smell_classes = ["Air", "Lime", "Vodka", "Beer", "Vinegar", "Wine", "Acetone", "Ethanol", "Isopropanol"]
    smell_class = random.choice(smell_classes)
    return smell_class

try:
    ser=serial.Serial("/dev/ttyACM1",9600)
except:
    ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

gp.setmode(gp.BOARD)
try:
    rows = list()
    x = 1
    for i in range(1,101):
        if x>60:
            x = 1
        read_ser=ser.readline()
        temp_string = read_ser.decode('utf-8')
        temp_data = eval(temp_string[:-2])
        # temp_data = random_generator()
        temp_data["time"] = x
        print(temp_data)
        row = [temp_data["time"], temp_data["temp"], temp_data["pres"], temp_data["co"], temp_data["lpg"], temp_data["smoke"]]
        rows.append(row)
        x += 1

        time.sleep(1)
    df = pd.DataFrame(rows, columns = ["Time",'Temperature', 'Pressure', 'CO', 'LPG', 'Smoke'])
    df.to_csv("Air.csv", index = False)
    data={
        "device_id": "testdev3",
        "avg_pres": round(df["Pressure"].mean(),2),
        "avg_temp": round(df["Temperature"].mean(),2),
        "avg_co": int(df["CO"].mean()),
        "avg_lpg": int(df["LPG"].mean()),
        "avg_smoke": int(df["Smoke"].mean())
        }
    data["smell_class"] = log_generator()
    print(data)
except KeyboardInterrupt:
    sys.exit(0)
except:
    print("Try Again")
