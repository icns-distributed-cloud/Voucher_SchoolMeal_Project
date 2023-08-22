import serial
import time
import threading
import pymysql
import datetime as dt
from dateutil.tz import gettz
from dotenv import load_dotenv
import os




# Add function



if __name__ == "__main__":
    print('Running. Press CTRL-C to exit.')

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open

        if arduino.isOpen():
            print("{} connected!\n".format(arduino.port))
            arduino.reset_input_buffer()
            load_dotenv()
            
            print('env connect') 
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
                    #print()

                    gas, light, humidity, temperature = sensor_list[0], sensor_list[1], sensor_list[2], sensor_list[3]
                    User = os.environ.get('User')
                    Password = os.environ.get('Password')
                    Table_name = os.environ.get('Table_name')

"""          
                    conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='User',
                    passwd='Password',
                    db='Table_name')

                    with conn.cursor() as cur:
                        sql = "insert into sensor_data(time, gas, light, humidity, temperature) values(%s, %s, %s, %s, %s)"
                        

                    
                        if time is not None and light is not None and humidity is not None and temperature is not None:  # insert data

                            cur.execute(sql, (
                                time, gas, light, humidity, temperature
                            ))
                            conn.commit()
                            print("success")
                        else:
                            print("Failed to get reading.")
                            """


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
