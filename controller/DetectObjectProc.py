import threading
import DetectObject_Yolov5
from datetime import datetime
from time import sleep

weights = "C:/Users/nosul/ObjectDetection/yolov5/best.pt" #  config를 수정하기
source = "C:/Users/nosul/ObjectDetection/yolov5/test_image.jpg" # 테스트할 이미지

from TIC_API import *

class DetectObjectProc:

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 1 # Default Wait Second is 1 Sec

    def Run(self): # Just Call This Function

        self.__mMyThread = threading.Thread(target=self.MyThread) # Change for Your Function
        #self.__mMyThread.daemon = True
        self.__mMyThread.start()

    def MyThread(self):
        while True:
            self.__mLock.acquire()

            if(self.__mStopFlag == True):
                self.__mStopFlag = False
                self.__mLock.release()
                return

            self.__DetectFire() # This is Test Function, You Shoud Add your Function, then it will run periodically

            sleep(self.__Second)

            self.__mLock.release()

    def test(self):
        print("This is Test Funcion")
        
    def RestartThread(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True

            threading.Timer(self.__Second + 2, self.Run).start()


    def StopThread(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
     
            
            
            
    def __DetectFire(self):
        print("Start Detect Object")
        result = DetectObject_Yolov5.run(weights = weights, source = source)

        output = []
        datasObject = [[False for col in range(10)] for row in range(10)]
        resultObject = [[False for col in range(10)] for row in range(10)]


        for i in range(10):
            for j in range(10):
                datasObject[i][j] = False
                
        for i in range(10):
            for j in range(10):
                resultObject[i][j] = False

        if(len(result) >= 1):
            for i in result: # 마스크 개수
                for j in range(10):
                    for k in range(10):
                        list_ = []
                        # 픽셀 위치
                        list_.append(TIC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][0]) # x
                        list_.append(TIC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][1]) # y
                        list_.append(64) # w
                        list_.append(48) # h

                        result_list = []
                        # 
                        result_list.append(i[0].item()) # 해당 마스크의 위치 i마다 바뀜
                        result_list.append(i[1].item())
                        result_list.append(i[2].item())
                        result_list.append(i[3].item())

                        if(self.__GetPixelData(result_list, list_) == True):
                            output.append([j, k]) # 비교한 값에 대한 true false 집합
                            #break
        
        dic = {}
        
        equalWithFireAndObject = False
        fire_list = TIC_API.getInstance().GetAllFireList("FireResult") 

        fire_list_border = [[False for col in range(10)] for row in range(10)]
        for i in range(10):
            for j in range(10):
                fire_list_border[i][j] = False

        for i in range(10): # 0~9
            for j in range(10): # 0~9
                if fire_list[i][j] == True :
                    fire_list_border[i][j] = True
                    if i == 0 and j == 0:
                        fire_list_border[i+1][j] = True
                        fire_list_border[i][j+1] = True
                        fire_list_border[i+1][j+1] = True
                    elif i == 9 and j == 9:
                        fire_list_border[i-1][j] = True
                        fire_list_border[i-1][j-1] = True
                        fire_list_border[i][j-1] = True
                    elif i == 0 and j == 9:
                        fire_list_border[i][j-1] = True
                        fire_list_border[i+1][j-1] = True
                        fire_list_border[i+1][j] = True
                    elif i == 9 and j == 0:
                        fire_list_border[i-1][j] = True
                        fire_list_border[i-1][j+1] = True
                        fire_list_border[i][j+1] = True
                    elif i == 0:
                        fire_list_border[i][j-1] = True
                        fire_list_border[i][j+1] = True
                        fire_list_border[i+1][j-1] = True
                        fire_list_border[i+1][j] = True
                        fire_list_border[i+1][j+1] = True
                    elif j == 0:
                        fire_list_border[i-1][j] = True
                        fire_list_border[i-1][j+1] = True
                        fire_list_border[i][j+1] = True
                        fire_list_border[i+1][j] = True
                        fire_list_border[i+1][j+1] = True
                    elif i == 9:
                        fire_list_border[i-1][j-1] = True
                        fire_list_border[i-1][j] = True
                        fire_list_border[i-1][j+1] = True
                        fire_list_border[i][j-1] = True
                        fire_list_border[i][j+1] = True
                    elif j == 9:
                        fire_list_border[i-1][j] = True
                        fire_list_border[i+1][j] = True
                        fire_list_border[i-1][j-1] = True
                        fire_list_border[i][j-1] = True
                        fire_list_border[i+1][j-1] = True
                    else:
                        fire_list_border[i-1][j-1] = True
                        fire_list_border[i-1][j] = True
                        fire_list_border[i-1][j+1] = True
                        fire_list_border[i][j-1] = True
                        fire_list_border[i][j+1] = True
                        fire_list_border[i+1][j-1] = True
                        fire_list_border[i+1][j] = True
                        fire_list_border[i+1][j+1] = True
   
        if(len(output) >= 1):
            for i in output:
                for j in range(10):
                    for k in range(10):
                        if (i[0] == j and i[1] == k):
                            datasObject[j][k] = True

        for i in range(10): # 0~9
            for j in range(10): # 0~9
                if fire_list_border[i][j] == True and datasObject[i][j] == True :
                    resultObject[i][j] = True
                    
                    equalWithFireAndObject = True

        ObjectPresentTime = datetime.now()
        
        if equalWithFireAndObject is True:
            dic = {"IsObject": 1,"ObjectPresentTime":ObjectPresentTime}
        else :
            dic = {"IsObject": 0,"ObjectPresentTime":ObjectPresentTime}
            
        TIC_API.getInstance().SaveAllJson(dic, "02_ResultDataObject")
        
    def __GetPixelData(self, r1, r2): # 추가
        x = 0
        y = 1
        w = 2
        h = 3

        if(r1[x] > r2[x] + r2[w]):
            return False
        if(r1[x] > r1[w] < r2[x]):
            return False
        if(r1[y] > r2[y] + r2[h]):
            return False
        if(r1[y] + r1[h] < r2[y]):
            return False

        rect = [0, 0, 0, 0]

        rect[0] = max(r1[x], r2[x])
        rect[1] = max(r1[y], r2[y])
        rect[2] = min(r1[x] + r1[w], r2[x] + r2[w]) - rect[x]
        rect[3] = min(r1[y] + r1[h], r2[y] + r2[h]) - rect[y]

        return True

NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")

print(NowFireIndexList)

if NowFireIndexList is not None :
    test = DetectObjectProc()
    test.Run()