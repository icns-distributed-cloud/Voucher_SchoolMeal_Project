import threading
from datetime import datetime
from time import sleep
from TIC.TIC_API.TIC_API_Python.TIC_API import *

import sys
sys.path.append('/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/')
from TIC_Data import *

import yolov5_master.DetectObject_Yolov5 as DetectObject_Yolov5

weights = "/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Object_best.pt" #  config를 수정하기 C:\dev\Meal\Voucher_SchoolMeal_Project\SchoolMeal_Part\DeepLearning\ObjectDetect\best.pt
source = "/home/icns/Desktop/TIC_Soft/TIC_Image.jpg" # 테스트할 이미지 "Voucher_SchoolMeal_Project/controller/DummyImage.png"

class DetectObjectProc:
    __mFilePath ="gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Detected_Data/"

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 5 # Default Wait Second is 1 Sec

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

            self.__DetectObject() # This is Test Function, You Shoud Add your Function, then it will run periodically

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
     
            
            
            
    def __DetectObject(self):
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
        ## DetectFireList.json {"DetectFireList": [[1,2], [2,3]]} ## 계속 늘어날수있음

        TIC_API.getInstance().SetFilePath("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/")
        GetDetectFireList = TIC_API.getInstance().GetAllJsonData("DetectFireList")
        fire_list = TIC_API.getInstance().GetFireFlagData(GetDetectFireList)
        
        fire_list_border = [[False for col in range(10)] for row in range(10)]
        for i in range(10):
            for j in range(10):
                fire_list_border[i][j] = False

        for i in range(10): # 0~9
            for j in range(10): # 0~9
                if fire_list[i][j] == True :
                    #fire_list_border[i][j] = True # 해당 불의 위치가 아닌 그 주변 픽셀에 한해서 Detect
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

        ObjectPresentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        if equalWithFireAndObject is True:
            dic = {"IsObject": True,"ObjectPresentTime":ObjectPresentTime}
        else :
            dic = {"IsObject": False,"ObjectPresentTime":ObjectPresentTime}
            
        
        data = dic
        fileName = "02_ResultDataObject"
        
        if not os.path.exists(self.__mFilePath):
            os.makedirs(self.__mFilePath)
        
        if(data != None):
            with open(self.__mFilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData = data

                json.dump(inputData, outfile, indent=4)

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

# print(NowFireIndexList)

if NowFireIndexList is None :
    start_detect = DetectObjectProc()
    start_detect.Run()