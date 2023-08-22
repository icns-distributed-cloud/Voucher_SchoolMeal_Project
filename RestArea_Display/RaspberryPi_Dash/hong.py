import serial
import time
import threading
import pymysql
import datetime as dt
from dateutil.tz import gettz


# Add function



if __name__ == "__main__":
    print('Running. Press CTRL-C to exit.')

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open

        if arduino.isOpen():
            print("{} connected!\n".format(arduino.port))
            arduino.reset_input_buffer()
    
            while True:
                if arduino.in_waiting != 0:
                    #time = dt.datetime.now(gettz('Asia/Seoul')).isoformat()
                    # str type
                    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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
                    print()