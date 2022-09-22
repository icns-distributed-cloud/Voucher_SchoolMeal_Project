import threading
from datetime import datetime
from time import sleep
from enum import Enum

from SchoolMeal_Part.TIC.TIC_API.TIC_API_Python.TIC_API import *

class Rect(Enum):
    x = 0
    y = 1
    w = 2
    h = 3
    

class DetectFireProc:

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 5 # Default Wait Second is 1 Sec

    def Run(self): # Just Call This Function

        self.__mMyThread = threading.Thread(target=self.__MyThread)
        #self.__mMyThread.daemon = True
        self.__mMyThread.start()

    def __MyThread(self):
        while True:
            self.__mLock.acquire()

            if(self.__mStopFlag == True):
                self.__mStopFlag = False
                self.__mLock.release()
                return

            #Add Detect Oill Code

            sleep(self.__Second)

            self.__mLock.release()


    def RestartThread(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True

            threading.Timer(self.__Second + 2, self.Run).start()


    def StopThread(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
        
'''
    def __Detect(self):
        print("Start Detect Fire")
        DetectBoxList = DetectFire_Yolov5.run()

        BoxOverlabList = []

        if(len(DetectBoxList) >= 1):
            for i in DetectBoxList:
                for j in range(10):
                    for k in range(10):
                        CurrentCellBox = []
                        CurrentCellBox.append(TIC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.x.value]) # x
                        CurrentCellBox.append(TIC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.y.value]) # y
                        CurrentCellBox.append(64) # w
                        CurrentCellBox.append(48) # h

                        CurrentDetectBox = []
                        CurrentDetectBox.append(i[0].item())
                        CurrentDetectBox.append(i[1].item())
                        CurrentDetectBox.append(i[2].item())
                        CurrentDetectBox.append(i[3].item())

                        if(self.__CheckBoxOverlab(CurrentDetectBox, CurrentCellBox) == True):
                            BoxOverlabList.append([j, k])

        
        JsonResultData = {}
        
        IsDetectList_10x10 =  [[0 for col in range(10)] for row in range(10)]

        for i in range(10):
            for j in range(10):
                IsDetectList_10x10[i][j] = False


        if(len(BoxOverlabList) >= 1):
            for i in BoxOverlabList:
                for j in range(10):
                    for k in range(10):
                        if (i[Rect.x.value] == j and i[Rect.y.value] == k):
                            TmperatureList_10x10 = TIC_API.getInstance().GetTmperatureList(PixelType.TenByTen.value, "DummyData")
                            if (TmperatureList_10x10 is not None):
                                if (TmperatureList_10x10[j][k] >= 80):
                                    IsDetectList_10x10[j][k] = True


        now = datetime.now()

        JsonResultData["FireList_100"] = IsDetectList_10x10
        JsonResultData["CurrentTime"] = now.strftime('%Y-%m-%d %H:%M:%S')

        #print(JsonResultData)

        TIC_API.getInstance().SaveAllJson(JsonResultData, "01_ResultDataFire")


    def __CheckBoxOverlab(self, box1, box2): # Check is Detect box overlab with 10x10 cell

        if(box1[Rect.x.value] > box2[Rect.x.value] + box2[Rect.w.value]):
            return False
        if(box1[Rect.x.value] > box1[Rect.w.value] < box2[Rect.x.value]):
            return False
        if(box1[Rect.y.value] > box2[Rect.y.value] + box2[Rect.h.value]):
            return False
        if(box1[Rect.y.value] + box1[Rect.h.value] < box2[Rect.y.value]):
            return False

        #rect = [0, 0, 0, 0]

        #rect[0] = max(box1[Rect.x.value], box2[Rect.x.value])
        #rect[1] = max(box1[Rect.y.value], box2[Rect.y.value])
        #rect[2] = min(box1[Rect.x.value] + box1[Rect.w.value], box2[Rect.x.value] + box2[Rect.w.value]) - rect[Rect.x.value]
        #rect[3] = min(box1[Rect.y.value] + box1[Rect.h.value], box2[Rect.y.value] + box2[Rect.h.value]) - rect[Rect.y.value]

        return True
'''

## ------------------ How to Use -----------------#

#test = DetectFireProc()
#test.Run()

## ------------------ How to Use -----------------#

