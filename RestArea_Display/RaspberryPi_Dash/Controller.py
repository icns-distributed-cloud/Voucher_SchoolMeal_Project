from TapoP100.PyP100.Control_tapo import Plug
import requests
import socket
import urllib3
import pymysql
import time
import logging


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s - %(message)s]')

file_handler = logging.FileHandler('Error.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

'''
plug_list = []
plug_list.append(Plug("192.168.5.19", "kidae92@khu.ac.kr", "icns0000", "Gasup"))
plug_list.append(Plug("192.168.5.20", "kidae92@khu.ac.kr", "icns0000", "whanpung"))
plug_list.append(Plug("192.168.5.21", "kidae92@khu.ac.kr", "icns0000", "jomung"))
plug_list.append(Plug("192.168.5.22", "kidae92@khu.ac.kr", "icns0000", "sunpung"))'''

# con = pymysql.connect(host="localhost", port=3306, user="root", password=PW, db ="sensor_data")
# cur = con.cursor()

while True:
    try:
        time.sleep(0.5)
        
        plug_list = []
        plug_list.append(Plug("192.168.4.12", "jyng2227@khu.ac.kr", "icns0000", "Gasup"))
        plug_list.append(Plug("192.168.4.15", "jyng2227@khu.ac.kr", "icns0000", "whanpung"))
        plug_list.append(Plug("192.168.4.13", "jyng2227@khu.ac.kr", "icns0000", "jomung"))
        plug_list.append(Plug("192.168.4.14", "jyng2227@khu.ac.kr", "icns0000", "sunpung"))
        
        print("DB CONNECT")
        con = pymysql.connect(host="localhost", port=3306, user="root", password=PW, db ="sensor_data")
        cur = con.cursor()
        sql = "select * from sensor_data order by time desc limit 1"
        cur.execute(sql)
        print("DB SUCCESS!")

        rows = list(cur.fetchall())
        print(rows, type(rows))

        Time, Gas, Light, Humid, Temp = rows[0]
        ''' 
        tmp = []
        for i in rows:
            tmp.append(i)
        # print(tmp)
        '''
        # Read Value
        '''
        Gas = rows[1]
        Light = rows[2]
        Humid = rows[3]
        Temp = rows[4]
        '''
        if (Gas > 500):
            plug_list[1].turn_on()
        elif (Gas < 300):
            plug_list[1].turn_off()

        if (Humid < 20):
            plug_list[0].turn_on()
        elif (Humid > 60):
            plug_list[0].turn_off()

        if (Light < 100):
            plug_list[2].turn_on()
        elif (Light > 200):
            plug_list[2].turn_off()

        if (Temp > 26):
            plug_list[3].turn_on()
        elif (Temp < 20):
            plug_list[3].turn_off()
    except requests.exceptions.ReadTimeout as E:
        print(f'{E}\nTimeout 오류 발생!')
        logger.error(E)
    except requests.exceptions.ConnectTimeout as E:
        print(f'{E}\nTimeout 오류 발생!')
        logger.error(E)
    except requests.exceptions.ConnectionError as E:
        print(f'{E}\nTimeout 오류 발생!')
        logger.error(E)
    except socket.timeout as E:
        print(f'{E}\nTimeout Error')
        logger.error(E)
    except urllib3.exceptions.ReadTimeoutError as E:
        print(f'{E}\nTimeout')
        logger.error(E)
    except KeyError as E:
        print(f'{E}\nKeyError')
        logger.error(E)
    except IndexError as E:
        print(f'{E}\n인덱스 에러!')
        logger.error(E)
