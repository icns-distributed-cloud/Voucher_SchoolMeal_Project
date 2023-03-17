import json
from math import fabs
from multiprocessing.sharedctypes import Value
import os
from enum import Enum

#Version 1.03


class PixelType(Enum):
    TenByTen = 0
    FortyByForty = 1
    


class TIC_API:

    __mFilePath = "TIC_Data/"

    __mInstance = None

    __mPixelData_10x10 = None
    __mPixelData_40x40 = None

    __mIsInit = False

    def __init__(self): # Initialization
        if self.__mIsInit == True:
            return

        self.__mPixelData_10x10 = self.__CreatePixelData(1440, 1080, 10, 10, 4)
        self.__mPixelData_40x40 = self.__CreatePixelData(1440, 1080, 40, 40, 4)
        
        self.__mIsInit = True

    @classmethod
    def getInstance(self):
        """Singleton Pattern, Get TIC_API Instance"""
        if self.__mInstance is None:
            self.__mInstance = super().__new__(self)
            self.__mInstance.__init__()
        return self.__mInstance


    def SetFilePath(self, path:str): 
        """If You want use other FilePath, You can set W/R file path, Default path is "FLC_Data/", First argument value is Change FilePath"""
        self.__mFilePath = path


    def __CreatePixelData(self, w:int, h:int, x:int, y:int, vertex:int): # Create Pixel Vertext Position Data
        PixelData = [[[0 for _ in range(vertex)] for _ in range(x)] for _ in range(y)]

        for i in range(x):
            for j in range(y):
                PixelData[i][j][0] = ([w/x * i, h/y * j])
                PixelData[i][j][1] = ([w/x * (i+1), h/y * j])
                PixelData[i][j][2] = ([w/x * i, h/y * (j+1)])
                PixelData[i][j][3] = ([w/x * (i+1), h/y * (j+1)])

        return PixelData


    def SaveAllJson(self, data:dict, fileName:str):
        """ Save JsonData, First argument value is Dictionary, Second value is FileName"""
        if not os.path.exists(self.__mFilePath):
            os.makedirs(self.__mFilePath)
        
        if(data != None):
            with open(self.__mFilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData = data

                json.dump(inputData, outfile, indent=4)


    def GetFireFlagData(self, data:list[list]):
        """Get is Fire True or False Data, First argument value is 2 Dimensional Array, Return Vlaue is 2 Dimensional Array"""

        if data == None:
            return None

        data_list = [[0 for col in range(10)] for row in range(10)]
        
        for i in range(10):
            for j in range(10):
                data_list[i][j] = False
        
        for i in range(len(data["DetectFireList"])):
            data_list[data["DetectFireList"][i][0]][data["DetectFireList"][i][1]] = True

        return data_list

    # def SaveOneJson(self, data, fileName:str):
    #     if(data == None):
    #         return None

    #     if not os.path.exists(self.__FilePath):
    #         os.makedirs(self.__FilePath)
        
    #     datas = self.GetAllJsonData(fileName)

    #     if datas == None:
    #         self.SaveAllJson(fileName, data)
    #     else:
    #         try:
    #             for key, value in data.items():
    #                 datas[key] = value
                

    #             with open(self.__FilePath + fileName + ".json", 'w') as outfile:
    #                 json.dump(datas, outfile, indent=4)
    #         except KeyError:
    #             self.SaveAllJson(fileName, data)


    def GetAllJsonData(self, fileName:str): 
        """ Load All data of TIC Data (Temperature Data, Fire Data...), First argument value is FileNam. Return value is Dictionary about TIC Data"""
        if os.path.isfile(self.__mFilePath + fileName + ".json") == False:
            return None

        with open(self.__mFilePath + fileName + ".json", "r") as json_file:
            json_data = json.load(json_file)
            if(json_data != None):
                return json_data

    def GetDetectFireList(self, fileName:str):
        """Get Detect Fire Cell in 10x10 List. Return value is 2 Dimensional Array"""
        if os.path.isfile(self.__mFilePath + fileName + ".json") == False:
            return None

        datas = self.GetAllJsonData(fileName)

        key ="DetectFireList"

        if datas == None:
            return None
        else:
            if key in datas:
                return datas[key]
            else:
                return None

    def GetTemperatureList(self, type:int ,fileName:str): 
        """Get TIC->TemperatureList about 10x10 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array"""
        key =""
        if type == PixelType.TenByTen.value:
            key = "TemperatureList_100"
        elif type == PixelType.FortyByForty.value:
            key = "TemperatureList_1600"
        else:
            return None

        datas = self.GetAllJsonData(fileName)

        if datas == None:
            return None
        else:
            if key in datas:
                return datas[key]
            else:
                return None
            
    def GetAllFireList(self, fileName:str): 
        """Get TCL->Fire about 10x10 List, First argument is FileName. Return value is 2 Dimensional Array"""
        key ="FireList_100"

        datas = self.GetAllJsonData(fileName)

        if datas == None:
            return None
        else:
            if key in datas:
                return datas[key]
            else:
                return None


    def GetNowFireCellList(self, fileName:str):
        """Get Now Fire Cell in X * Y All Fire List. return 2 Dimensional Array"""

        key ="FireList_100"

        datas = self.GetAllJsonData(fileName)

        if datas == None:
            return None
        else:
            if key in datas:

                isFireList = []

               # isFireList = []
                index = 0

                for i in range(len(datas[key])):
                    for j in range(len(datas[key][i])):
                        if datas[key][i][j] == True:
                            isFireList.append([i, j])
                            index += 1

                return isFireList
            else:
                return None

    # def GetValueOfKey_Data(self, key:str, data):
    #     try:
    #         datas = data
    #         if key in datas:
    #             return datas[key]
    #         else:
    #             return None

    #     except KeyError:
    #         if key in datas:
    #             return data[key]
    #         else:
    #             return None


    # def GetValueOfKey_File(self, key:str, fileName:str):
    #     data = self.GetAllJsonData(fileName)
    #     return self.GetValueOfKey_Data(data, key)


    def GetAllCellData(self, type:int): 
        """Get All Pixell Data, is X * Y Data, First argumenet value is PixelType. return value is 3 Dimensional Array"""
        if(type == PixelType.TenByTen.value):
            return self.__mPixelData_10x10 
        elif(type == PixelType.FortyByForty.value):
            return self.__mPixelData_40x40 
        else:
            return None


    def GetOneCellData(self, x:int, y:int, type:int): 
        """Get One Pixel(cell) in X * Y Data, First,Second argument value is x,y vertex, Third is PixelType, return 2 Dimensional Array"""
        if(type == PixelType.TenByTen.value):
            if x >= 10 or y >= 10:
                return None
            return self.__mPixelData_10x10[x][y]
        elif(type == PixelType.FortyByForty.value):
            if x >= 40 or y >= 40:
                return None
            return self.__mPixelData_40x40[x][y]
        else:
            return None


    def GetConfigData(self, fileName:str):
        """Get induction position in 10 x 100 cell. Second argument value is file name. Return value is 2 Dimensional Array"""

        key ="InductionPosition"

        datas = self.GetAllJsonData(fileName)

        data_list = []

        if datas == None:
            return None
        else:
            if key in datas:

                for i in range(len(datas[key])):
                    data_list.append(datas[key][i])
                return data_list
            else:
                return None



##### Not Use, Test Code ######
'''
mTIC_API = TIC_API()

datas = [[0 for col in range(10)] for row in range(10)]
for i in range(10):
    for j in range(10):
        datas[i][j] = random.randrange(10, 50)

print(datas)

datasT = [[0 for col in range(40)] for row in range(40)]
for i in range(40):
    for j in range(40):
        datasT[i][j] = random.randrange(10, 50)

datasFire =  [[0 for col in range(10)] for row in range(10)]

for i in range(10):
    for j in range(10):
        if random.randrange(1, 7) == 5:
            datasFire[i][j] = True
        else:
            datasFire[i][j] = False

dic = {}
dic["TemperatureList_100"] = datas
dic["TemperatureList_1600"] = datasT
dic["FireList_100"] = datasFire

mTIC_API.SaveAllJson(dic,"DummyData")
'''

#print(GetOnePixelData(0))
#test_Tcl = TIC_API()

#dic = {'abcvs':50}
#test_Tcl.WriteJson("test", dic)
#test_Tcl.SaveAllJson(dic,"test")
#dd = GetJson("test")
#print(dd)
#print(GetKey_Data(dd,"name"))

#test_data = GetJson("test")

#print(test_data["name"])

#for key, value in dic.items():
#    print(key + "  " + value)