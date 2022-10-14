import threading
from collections import deque
from datetime import datetime
from time import sleep
from TIC.TIC_API.TIC_API_Python.TIC_API import *

class DetectMouse_TIC:
    __mFilePath = "rolo/"

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 5 # Default Wait Second is 5 Sec

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
            
            

            self.main() # This is Test Function, You Shoud Add your Function, then it will run periodically
            TCL_Data = TIC_API.getInstance().GetAllJsonData("ResultData") # Load All data of TLC Data (Temperature Data, Fire Data...), First argument value is FileNam. Return value is Dictionary about TLC Data
            print(TCL_Data)
            
            
            sleep(self.__Second)

            self.__mLock.release()


    def __test(self):
        print("This is Test Funcion")


    def RestartThread(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True

            threading.Timer(self.__Second + 2, self.Run).start()


    def StopThread(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
            
    
    def SaveAllJson(self,data:dict, fileName:str):
        """ Save JsonData, Fir argument value is Dictionary, Second value is FileName"""
        if not os.path.exists(self.__mFilePath):
            os.makedirs(self.__mFilePath)
        
        if(data != None):
            with open(self.__mFilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData = data

                json.dump(inputData, outfile, indent=4)

    def main(self):

        #if(현재시간):
        #    return

            ## FilePath
        TIC_API.getInstance().SetFilePath("Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/") # If You want use other FilePath, You can set W/R file path, Default path is "FLC_Data/", First argument value is Change FilePath
        
        ## Save Json File Data
        MousePresentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        mMouse_Dic = {'IsMouse': False,
                     'MousePresentTime':MousePresentTime} # You Have Use Dictionary when save Data, It's Test Dictionary
        self.SaveAllJson(mMouse_Dic, "04_ResultDataMouse") # Save JsonData, Fir argument value is Dictionary, Second value is FileName
        
        first = []
        for i in range(10):
            line = []
            for j in range(10):
                line.append(0)
            first.append(line)
        
        queue = deque([first])
        
        for i in range(30):
            TmperatureList_10x10 = TIC_API.getInstance().GetTemperatureList(PixelType.TenByTen.value, "DummyData") # Get TCL->TemperatureList about 10x10 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array
            queue.append(TmperatureList_10x10)
            sleep(2)
        
        checkList = queue.popleft()
        have2Check = [[i,j] for i in range(10) for j in range(10) if checkList[i][j]>34 and checkList[i][j]<40]
        
        for i in range(28):
            CheckList = queue.popleft()
            for element in have2Check:
                tmp = CheckList[element[0]][element[1]]
                if tmp<35 or tmp>40:
                    # 결과값 True로 변경
                    ## Save Json File Data
                    mMouse_Dic = {'IsMouse': True,
                     'MousePresentTime':MousePresentTime} # You Have Use Dictionary when save Data, It's Test Dictionary
                    self.SaveAllJson(mMouse_Dic, "04_ResultDataMouse") # Save JsonData, Fir argument value is Dictionary, Second value is FileName
                    print("Mouse: True")
            have2Check = [[i,j] for i in range(10) for j in range(10) if checkList[i][j]>34 and checkList[i][j]<40]
        
        CheckList = queue.popleft()
        for element in have2Check:
            tmp = CheckList[element[0]][element[1]]
            if tmp<35 or tmp>40:
                # 결과값 True로 변경
                ## Save Json File Data
                mMouse_Dic = {'IsMouse': True,
                     'MousePresentTime':MousePresentTime} # You Have Use Dictionary when save Data, It's Test Dictionary
                self.SaveAllJson(mMouse_Dic, "04_ResultDataMouse") # Save JsonData, Fir argument value is Dictionary, Second value is FileName
                print("Mouse: True")
                
        sleep(5)
        ## Save Json File Data
        mMouse_Dic = {'IsMouse': False,
                     'MousePresentTime':MousePresentTime} # You Have Use Dictionary when save Data, It's Test Dictionary
        self.SaveAllJson(mMouse_Dic, "04_ResultDataMouse") # Save JsonData, Fir argument value is Dictionary, Second value is FileName    
        print("Mouse: False")
        
        return


## ------------------ How to Use -----------------#

# test = DetectMouse_TIC()
# test.Run()

## ------------------ How to Use -----------------#

