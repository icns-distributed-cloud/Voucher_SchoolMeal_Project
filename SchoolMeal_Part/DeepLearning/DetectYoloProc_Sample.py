import threading
from datetime import datetime

class DetectYoloProc_Sample:

    __mLock = threading.Lock()

    __mStopFlag = False

    def Run(self): # Just Call This Function

        if(self.__mStopFlag == True):
            self.__mStopFlag = False
            return

        self.__mLock.acquire()
        
        #Add Your Function
        self.Test() # This is Test Function, You Shoud Add your Function, then it will run periodically

        threading.Timer(5, self.Run).start() # You Can Change The Thread Time, Now is 5 Second
        
        self.__mLock.release()


    def Test(self):
        print("This is Test Function, You Can Input This Function")

    def RestartThread(self): # RestartThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True

            threading.Timer(10, self.Run).start()


    def StopThread(self): # StopThread Function
        if(self.__mStopFlag == False):
            self.__mStopFlag = True
     


## ------------------ How to Use -----------------#

test = DetectYoloProc_Sample()
test.Run()

## ------------------ How to Use -----------------#

