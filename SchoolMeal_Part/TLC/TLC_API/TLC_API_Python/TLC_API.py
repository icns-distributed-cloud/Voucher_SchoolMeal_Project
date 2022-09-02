import enum
import json
import os
from enum import Enum
import random

#Version 1.01


class PixelType(Enum):
    TenByTen = 0
    FortyByForty = 1
    

class TLC_API:

    __FilePath = "FLC_Data/"

    __instance = None

    PixelData_10x10 = None
    PixelData_40x40 = None

    def __init__(self): # Initialization
        self.PixelData_10x10 = self.__CreatePixelData(640, 480, 10, 10, 4)
        self.PixelData_40x40 = self.__CreatePixelData(640, 480, 40, 40, 4)


    @classmethod
    def getInstance(self): # Singleton Pattern
        if self.__instance is None:
            self.__instance = super().__new__(self)
        return self.__instance


    def SetFilePath(self, path:str): # set W/R file path, Default path is "FLC_Data/", First argument value is Change FilePath
        self.__FilePath = path

    def __CreatePixelData(self, w:int, h:int, x:int, y:int, vertex:int): # Create Pixel Vertext Position Data
        PixelData = [[[0 for _ in range(vertex)] for _ in range(x)] for _ in range(y)]

        for i in range(x):
            for j in range(y):
                PixelData[i][j][0] = ([w/x * i, h/y * j])
                PixelData[i][j][1] = ([w/x * (i+1), h/y * j])
                PixelData[i][j][2] = ([w/x * i, h/y * (j+1)])
                PixelData[i][j][3] = ([w/x * (i+1), h/y * (j+1)])

        return PixelData


    def SaveAllJson(self, data, fileName:str): # Save JsonData, Fir argument value is Dictionary, Second value is FileName
        if not os.path.exists(self.__FilePath):
            os.makedirs(self.__FilePath)
        
        if(data != None):
            with open(self.__FilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData = data

                json.dump(inputData, outfile, indent=4)


    # def SaveOneJson(self, data, fileName:str):
    #     if(data == None):
    #         return None

    #     if not os.path.exists(self.__FilePath):
    #         os.makedirs(self.__FilePath)
        
    #     datas = self.LoadAllJsonData(fileName)

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


    def LoadAllJsonData(self, fileName:str): # Load All data of TLC Data (Temperature Data, Fire Data...), First argument value is FileNam. Return value is Dictionary about TLC Data
        if os.path.isfile(self.__FilePath + fileName + ".json") == False:
            return None

        with open(self.__FilePath + fileName + ".json", "r") as json_file:
            json_data = json.load(json_file)
            if(json_data != None):
                return json_data

    def GetTmperatureList(self, type:int ,fileName:str): # Get TCL->TemperatureList about 10x10 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array
        key =""
        if type == PixelType.TenByTen:
            key = "TemperatureList_100"
        elif type == PixelType.FortyByForty:
            key = "TemperatureList_1600"
        else:
            return None

        datas = self.LoadAllJsonData(fileName)

        if datas == None:
            return None
        else:
            if key in datas:
                return datas[key]
            else:
                return None
            
    def GetFireList(self, fileName): # Get TCL->Fire about 10x10 List, First argument is FileName. Return value is 2 Dimensional Array
        key ="FireList_100"

        datas = self.LoadAllJsonData(fileName)

        if datas == None:
            return None
        else:
            if key in datas:
                return datas[key]
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
    #     data = self.LoadAllJsonData(fileName)
    #     return self.GetValueOfKey_Data(data, key)


    def GetAllPixelData(self, type:int): # Get All Pixell Data, is X * Y Data, First argumenet value is PixelType. return value is 3 Dimensional Array
        if(type == PixelType.TenByTen):
            return self.PixelData_10x10 
        elif(type == PixelType.FortyByForty):
            return self.PixelData_40x40 
        else:
            return None


    def GetOnePixelData(self, x:int, y:int, type:int): # Get One Pixel(cell) in X * Y Data, First,Second argument value is x,y vertex, Third is PixelType, return 2 Dimensional Array, 
        if(type == PixelType.TenByTen):
            if x >= 10 or y >= 10:
                return None
            return self.PixelData_10x10[x][y]
        elif(type == PixelType.FortyByForty):
            if x >= 40 or y >= 40:
                return None
            return self.PixelData_40x40[x][y]
        else:
            return None




##### No Use, Test Code ######
'''
mTLC_API = TLC_API()

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

mTLC_API.SaveAllJson(dic,"DummyData")
'''

#print(GetOnePixelData(0))
#test_Tcl = TLC_API()

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