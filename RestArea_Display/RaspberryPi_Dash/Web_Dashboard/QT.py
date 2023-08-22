import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from threading import Thread
import pymysql
import time
import threading
from time import sleep
import json

class DB():
    def __init__(self):
        self.con = pymysql.connect(host="localhost", port=3306, user="root", password=PW, db ="sensor_data")
        self.cur = self.con.cursor()
        self.sql = "select * from sensor_data order by time desc limit 1"

        self.GetDB()
    
    def GetDB(self):
        con = pymysql.connect(host="localhost", port=3306, user="root", password=PW, db ="sensor_data")
        cur = con.cursor()
        sql = "select * from sensor_data order by time desc limit 1"
        cur.execute(sql)

        rows = list(cur.fetchall())
        print(rows, type(rows))

        Time, Gas, Light, Humid, Temp = rows[0]

        return [Gas, Light, Humid, Temp]

class SensorScreenWindow(QMainWindow):

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 0.1 # Default Wait Second is 1 Sec

    senSorA = None
    senSorB = None
    senSorC = None
    senSorD = None

    def __init__(self):
        super().__init__()

        self.db = DB()

        # label
        self.gas = self.CreateLabel("Gas",100,60)
        self.light = self.CreateLabel("Light",340,60)
        self.humid = self.CreateLabel("Humid",100,200)
        self.temp = self.CreateLabel("Temp",340,200)
       
    def SetLabelText(self, label,str):
        label.setText(str)

    def CreateLabel(self, str, x, y):
        label = QLabel(str, self)
        label.move(x, y)
        return label
    
    def Run(self): # Just Call This Function

        self.__mMyThread = threading.Thread(target=self.__MyThread)
        self.__mMyThread.daemon = True
        self.__mMyThread.start()

    def __MyThread(self):
        while True:
            self.__mLock.acquire()

            if(self.__mStopFlag == True):
                self.__mStopFlag = False
                self.__mLock.release()
                return

            self.__ShowScreen()

            sleep(self.__Second)

            self.__mLock.release()


    def Restart(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
            threading.Timer(self.__Second + 2, self.Run).start()

    def Stop(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
        
    def __ShowScreen(self):

        sensor = self.db.GetDB()

        self.SetLabelText(self.gas, str(sensor[0]))
        self.SetLabelText(self.light, str(sensor[1]))
        self.SetLabelText(self.humid, str(sensor[2]))
        self.SetLabelText(self.temp, str(sensor[3]))

app = QApplication(sys.argv)
mywindow = SensorScreenWindow()
mywindow.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
mywindow.resize(480, 320) 
mywindow.show()
mywindow.Run()
app.exec_()