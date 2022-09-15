from FireDetect.DetectFiretProc import *
# from ObjectDetect.ObjectFiretProc import * # 설
class YoloContainer:
    
    __mDetectFireProc = DetectFireProc()
    #__mDetectObjectProc = DetectObjectProc() # 설
    def Run(self):

        self.__mDetectFireProc.Run()
        #self.__mDetectObjectProc.Run() # 설