import serial
import time
import threading
# import pymysql
import datetime as dt
from dateutil.tz import gettz
from dotenv import load_dotenv
import os
from enum import Enum
from TLC_API import *
from datetime import datetime

class Sensor_Type(Enum):
    Gas = 0
    Light = 1
    Humidity = 2
    Temperature = 3


# Add function
if __name__ == "__main__":
    print('Running. Press CTRL-C to exit.')

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(3) #wait for serial to open

        if arduino.isOpen():
            print("{} connected!\n".format(arduino.port))
            arduino.reset_input_buffer()
            load_dotenv()
            while True:
                if arduino.in_waiting != 0:
                    #time = dt.datetime.now(gettz('Asia/Seoul')).isoformat()
                    # str type
                    time = dt.datetime.today().now(gettz('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")
                    sensor_value = arduino.readline().decode('utf-8').rstrip()
                    # # # # # # # # # # # # # # # # # # # # # 
                    # ALL float type
                    # index 0: Gas
                    # index 1: Light
                    # index 2: Humidity
                    # index 3: Temperature
                    # # # # # # # # # # # # # # # # # # # # #
                    sensor_list = list(map(float, sensor_value.split(",")))
                    if sensor_list[0] >= 1000 : 
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        JsonResultData = {}
                        JsonResultData["SmartConsent"] = True
                        JsonResultData["SmartConsentPresentTime"] = now
                        TLC_API.getInstance().SaveAllJson(JsonResultData, "SmartConsent")
                    
                    print("success")
                        

"""
            try:
                while True:
                    cmd=input("Enter command : ")
                    arduino.write(cmd.encode())
                    #time.sleep(0.1) #wait for arduino to answer

                    while arduino.inWaiting()==0: 
                        pass

                    if  arduino.inWaiting()>0: 
                        answer=arduino.readline()
                        print(answer)
                        arduino.flushInput() #remove data after reading
                        
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
"""
