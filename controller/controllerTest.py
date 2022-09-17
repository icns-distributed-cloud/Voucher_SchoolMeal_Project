import os
import time
import sys 
import threading
from tracemalloc import start

class controllTest:
    
    __isExit = False
    __TestThread = None
    
    def program_exit() :
        sys.exit("test controller program sys.exit()")
        
    def Run_Therad(self):
        time.sleep(1)
        self.__TestThread = threading.Thread(target=self.__Run, daemon=True)
        self.__TestThread.start()
        
    def __Run(self):
        while(True):
            
            if(self.__isExit == True):
                break
            
            #time.sleep(1)
            print("Testing.....")
            
        self.__isExit = False
        print("쓰레드 진짜 종료!!")
        sys.exit()
            
            
    def Exit(self):
        if(self.__isExit  == False):
            print("쓰레드 종료함수 호출!!")
            self.__isExit = True
        