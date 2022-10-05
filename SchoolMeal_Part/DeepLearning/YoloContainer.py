from ObjectDetect.DetectObjectProc import *
from PersonDetect.DetectPersonProc import *
from MouseDetect.DetectMouseProc import *

class YoloContainer:
    
    __mDetectObjectProc = DetectObjectProc() 
    __mDetectPersonProc = DetectPersonProc()
    __mDetectMouseProc = DetectMouseProc()

    def Run(self):

        self.__mDetectObjectProc.Run() 
        self.__mDetectPersonProc.Run()
        self.__mDetectMouseProc.Run()