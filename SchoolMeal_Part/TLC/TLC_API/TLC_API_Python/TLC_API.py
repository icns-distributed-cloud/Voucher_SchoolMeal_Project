import enum
import json
import os
from pickle import NONE
from enum import Enum
import random

#Version 1.01


class PixelType(Enum):
    TenByTen = 0
    FortyByForty = 1

class TLC_API:

    __FilePath = "FLC_Data/"

    PixelData_10x10 = NONE
    PixelData_40x40 = NONE

    def __init__(self):
        #self.PixelData_10x10 = self.__CreatePixelData(640, 480, 10, 10, 4)
        self.PixelData_10x10 = self.__CreatePixelData(640, 480, 10, 10, 4)
        self.PixelData_40x40 = self.__CreatePixelData(640, 480, 40, 40, 4)

        # [w/x * i, h/y * j], [w/x * (i+1), h/y * j], [w/x * i, h/y * (j+1)], [w/x * (i+1), h/y * (j+1)]


    def __CreatePixelData(self, w,h,x,y,vertex):
        PixelData = [[[0 for _ in range(vertex)] for _ in range(x)] for _ in range(y)]

        for i in range(x):
            for j in range(y):
                PixelData[i][j][0] = ([w/x * i, h/y * j])
                PixelData[i][j][1] = ([w/x * (i+1), h/y * j])
                PixelData[i][j][2] = ([w/x * i, h/y * (j+1)])
                PixelData[i][j][3] = ([w/x * (i+1), h/y * (j+1)])

        return PixelData


    def SaveAllJson(self, fileName, data):
        if not os.path.exists(self.__FilePath):
            os.makedirs(self.__FilePath)
        
        if(data != NONE):
            with open(self.__FilePath + fileName + ".json", 'w') as outfile:

                inputData = {}
                inputData['Data'] = []
                inputData['Data'].append(data)

                json.dump(inputData, outfile, indent=4)


    def SaveOneJson(self, fileName, data):
        if(data == NONE):
            return NONE

        if not os.path.exists(self.__FilePath):
            os.makedirs(self.__FilePath)
        
        datas = self.LoadAllJson(fileName)

        if datas == NONE:
            self.SaveAllJson(fileName, data)
        else:
            try:
                for key, value in data.items():
                    datas['Data'][0][key] = value

                with open(self.__FilePath + fileName + ".json", 'w') as outfile:
                    json.dump(datas, outfile, indent=4)
            except KeyError:
                self.SaveAllJson(fileName, data)


    def LoadAllJson(self, fileName):
        if os.path.isfile(self.__FilePath + fileName + ".json") == False:
            return NONE

        with open(self.__FilePath + fileName + ".json", "r") as json_file:
            json_data = json.load(json_file)
            if(json_data != NONE):
                return json_data


    def GetValueOfKey_Data(self, data, key):
        try:
            datas = data['Data']

            if key in datas[0]:
                return datas[0][key]
            else:
                return NONE

        except KeyError:
            if key in datas:
                return data[key]
            else:
                return NONE


    def GetValueOfKey_File(self, fileName, key):
        data = self.LoadAllJson(fileName)
        return self.GetValueOfKey_Data(data, key)


    def GetAllPixelData(self, type):
        if(type == PixelType.TenByTen):
            return self.PixelData_10x10 
        elif(type == PixelType.FortyByForty):
            return self.PixelData_40x40 


    def GetOnePixelData(self, x, y, type):
        if(type == PixelType.TenByTen):
            if x >= 10 or y >= 10:
                return None
            return self.PixelData_10x10[x][y]
        elif(type == PixelType.FortyByForty):
            if x >= 40 or y >= 40:
                return None
            return self.PixelData_40x40[x][y]



#---------------------- How to Use --------------------------#    
   
mTLC_API = TLC_API()
#print(mTLC_API.PixelData_10x10)

print(mTLC_API.GetOnePixelData(7,7, PixelType.TenByTen))

#---------------------- How to Use --------------------------#



'''
datas = [[0 for col in range(10)] for row in range(10)]
for i in range(10):
    for j in range(10):
        datas[i][j] = random.randrange(10, 50)

print(datas)

datasT = [[0 for col in range(40)] for row in range(40)]
for i in range(40):
    for j in range(40):
        datasT[i][j] = random.randrange(10, 50)

datasFire = [0 for col in range(10)]

for i in range(10):
    if random.randrange(1, 7) == 5:
        datasFire[i] = True
    else:
        datasFire[i] = False

dic = {}
dic["TemperatureList_100"] = datas
dic["TemperatureList_1600"] = datasT
dic["FireList_100"] = datasFire

mTLC_API.SaveAllJson("test",dic)
'''

#print(GetOnePixelData(0))

#dic = {'abcvs':'kadis'}
#WriteJson("test", dic)
#WriteJson_All("test",dic)
#dd = GetJson("test")
#print(dd)
#print(GetKey_Data(dd,"name"))

#test_data = GetJson("test")

#print(test_data["name"])

#for key, value in dic.items():
#    print(key + "  " + value)