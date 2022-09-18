from FireDetect.DetectFiretProc import *
from ObjectDetect.DetectObjectProc import *
from PersonDetect.DetectPersonProc import *
class YoloContainer:
    
    __mDetectFireProc = DetectFireProc()
    __mDetectObjectProc = DetectObjectProc() 
    __mDetectPersonProc = DetectPersonProc()

    def Run(self):

        self.__mDetectFireProc.Run()
        self.__mDetectObjectProc.Run() 
        self.__mDetectPersonProc.Run()