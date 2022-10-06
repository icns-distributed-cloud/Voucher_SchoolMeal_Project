from pickle import NONE
from ObjectDetect.DetectObjectProc import *
from PersonDetect.DetectPersonProc import *
from MouseDetect.DetectMouseProc import *

class YoloContainer:
    
    __mDetectObjectProc = DetectObjectProc() 
    __mDetectPersonProc = NONE
    __mDetectMouseProc = DetectMouseProc()

    def Run(self):
        NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")
        self.__mDetectPersonProc = DetectPersonProc(NowFireIndexList)

        self.__mDetectObjectProc.Run() 
        self.__mDetectPersonProc.Run()
        self.__mDetectMouseProc.Run()