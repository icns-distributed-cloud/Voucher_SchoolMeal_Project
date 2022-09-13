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

        self.__DetectFire()
        threading.Timer(5, self.Run).start()
        
        self.__mLock.release()
        

    def __DetectFire(self):
        print("Start Detect Fire")
        DetectResultBox = DetectFire_Yolov5.run()

        BoxOverLabList = []

        if(len(DetectResultBox) >= 1):
            for i in DetectResultBox:
                for j in range(10):
                    for k in range(10):
                        FireImageBox = []
                        FireImageBox.append(TLC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.x.value]) # x
                        FireImageBox.append(TLC_API.getInstance().GetOneCellData(j, k, PixelType.TenByTen.value)[0][Rect.y.value]) # y
                        FireImageBox.append(64) # w
                        FireImageBox.append(48) # h

                        DetectFireBox = []

                        DetectFireBox.append(i[0].item())
                        DetectFireBox.append(i[1].item())
                        DetectFireBox.append(i[2].item())
                        DetectFireBox.append(i[3].item())

                        if(self.__CheckBoxOverlab(DetectFireBox, FireImageBox) == True):
                            BoxOverLabList.append([j, k])
                            #break
        
        JsonResultData = {}
        IsFireList_10x10 =  [[0 for col in range(10)] for row in range(10)]

        for i in range(10):
            for j in range(10):
                IsFireList_10x10[i][j] = False


        if(len(BoxOverLabList) >= 1):
            for i in BoxOverLabList:
                for j in range(10):
                    for k in range(10):
                        if (i[0] == j and i[1] == k):
                            IsFireList_10x10[j][k] = True
                        #else:
                            #IsFireList_10x10[j][k] = False

        JsonResultData["FireList_100"] = IsFireList_10x10


        print(JsonResultData)

        TLC_API.getInstance().SaveAllJson(JsonResultData, "FireResult")

            
    def __CheckBoxOverlab(self, box1, box2): # 추가

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


#test = DetectFireProc()
#test.Run()

