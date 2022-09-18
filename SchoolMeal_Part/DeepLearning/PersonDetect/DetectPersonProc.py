import threading
import DetectPerson_Yolov5
from datetime import datetime
from time import sleep

from TLC_API import *

# 테스트용 Weights, Source
weights = "D:/person_detection/Pascal_yolov5pytorch/yolov5/runs/train/result_hyper3/weights/best.pt" # config를 수정하기
source = "C:/Users/yuri/Desktop/test_img_640_480.png"
    
class DetectPersonProc:
    
    __mLock = threading.Lock()
    
    __mStopFlag = False
    
    __mMyThread = None
    
    __Second = 5 # Default Wait Second is 1 Sec


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
        

    # Detect code
    def __Read_Detect(self): 
        person_count = DetectPerson_Yolov5.run(weights = weights, source = source)
        is_fire = False
        fire_list = TLC_API.getInstance().GetAllFireList("FireResult")   

        for row in range(10): # row(행) 10
            for column in range(10): # column(열) 10
                if fire_list[row][column]: # fire_list true (true = if fire exist)
                    TLC_API.getInstance().GetOnePixelData(row, column, PixelType.TenByTen)
                    is_fire = True
                    break
                
        now = datetime.now()
        
        print(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
            
        # value handling (fire o person x = True), (remainder value = False) 
        if is_fire and not person_count:
            print("danger")
            is_person = True
        else:
            print("not danger")
            is_person = False
            
        
        mPerson_Dic = { 
                       "IsPerson": is_person,
                       "PersonPresentTime":now.strftime('%Y-%m-%d %H:%M:%S.%f')
                       }
        
        # Json으로 저장
        TLC_API.getInstance().SaveAllJson(mPerson_Dic, "03_ResultDataPerson")


test = DetectPersonProc()
test.Run()