import threading
from time import sleep

class DetectYoloProc_Sample:

    __mLock = threading.Lock()

    __mStopFlag = False

    __mMyThread = None

    __Second = 1 # Default Wait Second is 1 Sec

    def Run(self): # Just Call This Function

        self.__mMyThread = threading.Thread(target=self.MyThread) # Change for Your Function
        self.__mMyThread.daemon = True
        self.__mMyThread.start()

    def MyThread(self):
        while True:
            self.__mLock.acquire()

            if(self.__mStopFlag == True):
                self.__mStopFlag = False
                return

            self.test() # This is Test Function, You Shoud Add your Function, then it will run periodically

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
     


## ------------------ How to Use -----------------#

test = DetectYoloProc_Sample()
test.Run()

## ------------------ How to Use -----------------#

