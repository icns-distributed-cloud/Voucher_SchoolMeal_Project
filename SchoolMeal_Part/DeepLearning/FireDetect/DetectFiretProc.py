import threading
import DetectFire_Yolov5

from TLC_API import *

class Rect(Enum):
    x = 0
    y = 1
    w = 2
    h = 3
    

class DetectFireProc:

    __mLock = threading.Lock()

    __mStopFlag = False

    def Run(self):

        if(self.__mStopFlag == True):
            self.__mStopFlag = False
            return

        self.__mLock.acquire()

        self.__Detect()
        threading.Timer(5, self.Run).start()
        
        self.__mLock.release()
        

    def __Detect(self):
        print("Start Detect Fire")
        DetectBoxList = DetectFire_Yolov5.run()

        BoxOverlabList = []

        if(len(DetectBoxList) >= 1):
            for i in DetectBoxList:
                for j in range(10):
                    for k in range(10):
                        CurrentCellBox = []
                        CurrentCellBox.append(TLC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.x.value]) # x
                        CurrentCellBox.append(TLC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.y.value]) # y
                        CurrentCellBox.append(64) # w
                        CurrentCellBox.append(48) # h

                        CurrentDetectBox = []
                        CurrentDetectBox.append(i[0].item())
                        CurrentDetectBox.append(i[1].item())
                        CurrentDetectBox.append(i[2].item())
                        CurrentDetectBox.append(i[3].item())

                        if(self.__CheckBoxOverlab(CurrentDetectBox, CurrentCellBox) == True):
                            BoxOverlabList.append([j, k])

        
        JsonResultData = {}
        
        IsDetectList_10x10 =  [[0 for col in range(10)] for row in range(10)]

        for i in range(10):
            for j in range(10):
                IsDetectList_10x10[i][j] = False


        if(len(BoxOverlabList) >= 1):
            for i in BoxOverlabList:
                for j in range(10):
                    for k in range(10):
                        if (i[Rect.x.value] == j and i[Rect.y.value] == k):
                            TmperatureList_10x10 = TLC_API.getInstance().GetTmperatureList(PixelType.TenByTen.value, "DummyData")
                            if (TmperatureList_10x10 is not None):
                                if (TmperatureList_10x10[j][k] >= 80):
                                    IsDetectList_10x10[j][k] = True

        JsonResultData["FireList_100"] = IsDetectList_10x10

        #print(JsonResultData)

        TLC_API.getInstance().SaveAllJson(JsonResultData, "FireResult")

            
    def __CheckBoxOverlab(self, box1, box2): # Check is Detect box overlab with 10x10 cell

        if(box1[Rect.x.value] > box2[Rect.x.value] + box2[Rect.w.value]):
            return False
        if(box1[Rect.x.value] > box1[Rect.w.value] < box2[Rect.x.value]):
            return False
        if(box1[Rect.y.value] > box2[Rect.y.value] + box2[Rect.h.value]):
            return False
        if(box1[Rect.y.value] + box1[Rect.h.value] < box2[Rect.y.value]):
            return False

        #rect = [0, 0, 0, 0]

        #rect[0] = max(box1[Rect.x.value], box2[Rect.x.value])
        #rect[1] = max(box1[Rect.y.value], box2[Rect.y.value])
        #rect[2] = min(box1[Rect.x.value] + box1[Rect.w.value], box2[Rect.x.value] + box2[Rect.w.value]) - rect[Rect.x.value]
        #rect[3] = min(box1[Rect.y.value] + box1[Rect.h.value], box2[Rect.y.value] + box2[Rect.h.value]) - rect[Rect.y.value]

        return True


## ------------------ How to Use -----------------#

#test = DetectFireProc()
#test.Run()

## ------------------ How to Use -----------------#

