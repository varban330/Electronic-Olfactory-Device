import requests
import json
import random
import serial
import RPi.GPIO as gp
import time
from datetime import datetime
import sys

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
while True:
    y = datetime.now()
    try:
        rows = list()
        for i in range(1,61):
            read_ser=ser.readline()
            temp_string = read_ser.decode('utf-8')
            temp_data = eval(temp_string[:-2])
            # temp_data = random_generator()
            temp_data["time"] = i
            print(temp_data)
            rows.append(temp_data)
            time.sleep(1)
        data={
        "device_id": "testdev3",
        "rows": rows
        }
        headers = {"content-type": 'application/json',"Ocp-Apim-Subscription-Key": "94cea4adae3c452ebd3c2ff10dd54d7c"}
        r = requests.post(url = 'https://eod-backend.herokuapp.com/ml/predict-class/',
                      data = json.dumps(data),
                      headers = headers)
        if r.status_code != requests.codes.ok:
               print(data)
               print(r.json())
        else:
               print("--------------------------------------------------------")
               print("Request Successful")
               print(r.json())
               x = r.json()
               if "category" in x.keys() and x["category"] == "Dangerous":
                   print("Buzzer Bjaao")
               elif "category" in x.keys() and x["category"] == "Normal":
                   print("Sab theek h")
               else:
                   print("Kuch gdbd h... Key nhi aayi")
               print("Total Time Taken (in Seconds)")
               print((datetime.now() - y).seconds)
               print("--------------------------------------------------------")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Try Again")
