import threading
import yolov5_master.DetectPerson_Yolov5 as DetectPerson_Yolov5
from datetime import datetime
from time import sleep
from TIC.TIC_API.TIC_API_Python.TIC_API import *

import sys
sys.path.append('/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/')
from TIC_Data import *  

# 테스트용 Weights, Source
# weights = "D:/person_detection/Pascal_yolov5pytorch/yolov5/runs/train/result_hyper3/weights/best.pt" # config를 수정하기
# source = "C:/Users/yuri/Desktop/test_img_640_480.png"
weights = "/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Person_best.pt" #  config를 수정하기 C:\dev\Meal\Voucher_SchoolMeal_Project\SchoolMeal_Part\DeepLearning\ObjectDetect\best.pt
source = "/home/icns/Desktop/TIC_Soft/TIC_Image.jpg" # 테스트할 이미지 "Voucher_SchoolMeal_Project/controller/DummyImage.png"
   
class DetectPersonProc:
    __mFilePath ="gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Detected_Data/"

    __mLock = threading.Lock()
    
    __mStopFlag = False
    
    __mMyThread = None
    
    __Second = 5 # Default Wait Second is 1 Sec
    
    #fire_list = []
    
    #def __init__(self, NowFireIndexList): # __init__ 초기화
    #    self.fire_list = NowFireIndexList


    def Run(self): # Just Call This Function
        
        self.__mMyThread = threading.Thread(target=self.MyThread) # Change for Your Function
        #self.__mMyThread.daemon = True
        self.__mMyThread.start()
    

        # Thread가 자원을 사용하기위해 요청, 사용할 수 있다면 들어가서 Lock, 이미 사용중이라면 대기
    def MyThread(self):
        while True:
            self.__mLock.acquire()
            
            if(self.__mStopFlag == True):
                self.__mStopFlag = False
                self.__mLock.release()
                return
            
            self.__Read_Detect() # This is Test Function, You Shoud Add your Function, then it will run periodically

            sleep(self.__Second)

            self.__mLock.release()
        
        
    def RestartThread(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True

            threading.Timer(self.__Second + 2, self.Run).start()


    def StopThread(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
        
    def Origin_to_ten (coor, W=1440, H=1080): # coor 좌표
        w = W//10
        h = H//10
        return [coor[0]//w, coor[1]//h, coor[2]//w, coor[3]//h] # box를 그릴 때, 왼쪽 위 꼭지점이랑 오른쪽 아래 꼭지점을 찍어 사각형을 그림 # x1 # y1 # x2 # y2  
        
    def range_check(self, x, range_pixel):
        x += range_pixel
        x = 0 if x<0 else x
        x = 9 if x>9 else x
        return x
    
    def Check_Danger(self, fire_list, ten_ten_arr):
        for x in range(len(fire_list)):
            for y in range(len(fire_list[x])):
                if fire_list[x][y]:
                    startx = self.range_check(x, -2)
                    endx = self.range_check(x, 2)
                    starty = self.range_check(y, -2)
                    endy = self.range_check(y, 2)

                    for i in range(startx, endx+1):
                        for j in range(starty, endy+1):
                            if not ten_ten_arr[i][j]:
                                return True # fire_list가 없으면 탈출 # 상태가 danger 감지 후 탈출 # True 위험
        return False

    # Detect code
    def __Read_Detect(self): 
        is_fire_danger = False
        
        # 사람을 Detection해서 사람 좌표 가져옴
        print("Start Detect Person")
        person_boxes = DetectPerson_Yolov5.run(weights = weights, source = source)
        
        # 현재 불이 있는 좌표만 가져옴
        TIC_API.getInstance().SetFilePath("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/")
        GetDetectFireList = TIC_API.getInstance().GetAllJsonData("DetectFireList")
        fire_list = TIC_API.getInstance().GetFireFlagData(GetDetectFireList)


        # False로 10*10행렬 생성
        ten_ten_arr = [[False]*10]*10
        
        # 사람 좌표로 10*10행렬에서 사람이 있는 면적을 표시
        while person_boxes:
            origin_coor = [val.item() for val in person_boxes.pop()]
            x1, y1, x2, y2 = self.origin_to_ten(origin_coor)
            
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    ten_ten_arr[i][j] = True
                
        # 현재 불이 인식되어서 fire_list에 값이 있다면
        #if fire_list:
            # fire_list가 빌때까지 불이 있는 좌표에서 1칸씩의 범위로 사람이 있는지 비교
        
        
#        while(fire_list and not is_fire_danger):
        is_fire_danger = self.Check_Danger(fire_list, ten_ten_arr)
                

        # 시간 불러오기
        now = datetime.now()
        #print(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
        
        if is_fire_danger: # 불 있고 + 사람 없을 때 = 위험 (경보음 발생)
            print("danger")
            is_person = False
        else:
            print("not danger") # 불 있고 + 사람 있을 때 = 이상 없음
            is_person = True
        
        # 저장할 내용 dict로 만들기
        mPerson_Dic = { 
                       "IsPerson": is_person,
                       "PersonPresentTime":now.strftime('%Y-%m-%d %H:%M:%S.%f')
                       }
        # Json으로 저장
        #TIC_API.getInstance().SaveAllJson(mPerson_Dic, "03_ResultDataPerson")
        data = mPerson_Dic
        fileName = "03_ResultDataPerson"
        
        if not os.path.exists(self.__mFilePath):
            os.makedirs(self.__mFilePath)
        
        if(data != None):
            with open(self.__mFilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData = data

                json.dump(inputData, outfile, indent=4)

NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")

# print(NowFireIndexList)

if NowFireIndexList is None :
   start_detect = DetectPersonProc()
   start_detect.Run()