import serial
import time
import threading
import pymysql
import datetime as dt
from dateutil.tz import gettz
from dotenv import load_dotenv
import os
from enum import Enum


class Sensor_Type(Enum):
    Gas = 0
    Light = 1
    Humidity = 2
    Temperature = 3


# Add function
if __name__ == "__main__":
    print('Running. Press CTRL-C to exit.')

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open

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

                    print(time)
                    # print("Gas: ", sensor_list[0], "ppm", sep="")
                    # print("Light: ", sensor_list[1], "lx", sep="")
                    # print("Humidity: ", sensor_list[2], "%", sep="")
                    # print("Temperature: ", sensor_list[3], "ºC", sep="")
                   
                    DB_server = os.environ.get('DB_server')
                    User = os.environ.get('User')
                    Password = os.environ.get('Password')
                    Table_name = os.environ.get('Table_name')

      
                    conn = pymysql.connect(
                    host=DB_server,
                    port=3306,
                    user=User,
                    passwd=Password,
                    db=Table_name)

                    with conn.cursor() as cur:
                        sql = "insert into sensor_data(time, gas, light, humidity, temperature) values(%s, %s, %s, %s, %s)"

                        for i in sensor_list:
                            if(i == None or time == None):
                                print("Failed to get reading.")
                                break

                        cur.execute(sql, (
                                time, sensor_list[Sensor_Type.Gas.value], sensor_list[Sensor_Type.Light.value], sensor_list[Sensor_Type.Humidity.value], sensor_list[Sensor_Type.Temperature.value]
                            ))
                        conn.commit()
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
