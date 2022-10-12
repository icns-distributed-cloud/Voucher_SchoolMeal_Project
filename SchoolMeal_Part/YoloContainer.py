from pickle import NONE
from DetectObjectProc import *
from DetectPersonProc import *
from DetectMouseProc import *
from DetectMouse_TIC import *

from datetime import datetime

class YoloContainer:
    __now = datetime.now() #.strftime('%Y-%m-%d %H:%M:%S.%f')
    __mMornning = __now.replace(hour=6, minute=0, second=0, microsecond=0)
    __mNight= __now.replace(hour=23, minute=59, second=59, microsecond=999999)

    ## 계속 detect만되는 상황 ## 수정필요
    __mDetectObjectProc = DetectObjectProc() 
    __mDetectPersonProc = NONE
    __mDetectMouseProc = DetectMouseProc()
    __mDetectMouse_TIC = DetectMouse_TIC()

    def Run(self):
        NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")
        self.__mDetectPersonProc = DetectPersonProc(NowFireIndexList)

        self.__mDetectObjectProc.Run() 
        self.__mDetectPersonProc.Run()

        if (self.__now < self.__mNight) and (self.__now >= self.__mMornning) :
            self.__mDetectMouseProc.Run()
        else :
            self.__mDetectMouse_TIC.Run()