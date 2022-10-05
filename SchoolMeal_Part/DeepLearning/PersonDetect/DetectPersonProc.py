import threading

import yolov5_master.DetectPerson_Yolov5 as DetectPerson_Yolov5

from datetime import datetime
from time import sleep

from SchoolMeal_Part.TIC.TIC_API.TIC_API_Python.TIC_API import *

# 테스트용 Weights, Source
weights = "D:/person_detection/Pascal_yolov5pytorch/yolov5/runs/train/result_hyper3/weights/best.pt" # config를 수정하기
source = "C:/Users/yuri/Desktop/test_img_640_480.png"
    
class DetectPersonProc:
    
    __mLock = threading.Lock()
    
    __mStopFlag = False
    
    __mMyThread = None
    
    __Second = 5 # Default Wait Second is 1 Sec
    
    fire_list = []
    
    def __init__(self, NowFireIndexList): # __init__ 초기화
        self.fire_list = NowFireIndexList


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
        
    def range_check(x, range_pixel):
        x += range_pixel
        x = 0 if x<0 else x
        x = 9 if x>9 else x
        return x
    
    # Detect code
    def __Read_Detect(self): 
        is_fire_danger = False
        
        # 사람을 Detection해서 사람 좌표 가져옴
        person_boxes = DetectPerson_Yolov5.run(weights = weights, source = source)
        
        # 현재 불이 있는 좌표만 가져옴
        fire_list = self.fire_list # 수정 필요 (어떻게 쓰는지)  
        
        # False로 10*10행렬 생성
        ten_ten_arr = [[False]*10]*10
        
        # 사람 좌표로 10*10행렬에서 사람이 있는 면적을 표시
        while person_boxes:
            origin_coor = [val.item() for val in person_boxes.pop()]
            x1, y1, x2, y2 = origin_to_ten(origin_coor)
            
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    ten_ten_arr[i][j] = True
                
        # 현재 불이 인식되어서 fire_list에 값이 있다면
        #if fire_list:
            # fire_list가 빌때까지 불이 있는 좌표에서 1칸씩의 범위로 사람이 있는지 비교
        while(fire_list and not is_fire_danger):
            # i(x), j(y)좌표로 뒤에서부터 하나씩 꺼냄
            x, y = fire_list.pop() # 가장 뒤에 있는 것을 꺼내기 pop
            startx = range_check(x, 2)
            endx = range_check(x, -2)
            starty = range_check(y, 2)
            endy = range_check(y, -2)
            
            for i in range(startx, endx+1):
                for j in range(starty, endy+1):
                    if not ten_ten_arr[i][j]:
                        is_fire_danger=True # fire_list가 없으면 탈출 # 상태가 danger 감지 후 탈출 # True 위험
                

        # 시간 불러오기
        now = datetime.now()
        #print(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
        
        if is_fire_danger: # 불 있고 + 사람 없을 때 = 위험 (경보음 발생)
            print("danger")
            is_person = 0
        else:
            print("not danger") # 불 있고 + 사람 있을 때 = 이상 없음
            is_person = 1
        
        # 저장할 내용 dict로 만들기
        mPerson_Dic = { 
                       "IsPerson": is_person,
                       "PersonPresentTime":now.strftime('%Y-%m-%d %H:%M:%S.%f')
                       }
        # Json으로 저장
        TIC_API.getInstance().SaveAllJson(mPerson_Dic, "03_ResultDataPerson")


NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")

print(NowFireIndexList)

if NowFireIndexList is not None :
    test = DetectPersonProc(NowFireIndexList)
    test.Run()
