import json
import os
import time
from SchoolMeal_Part.TIC.TIC_API.TIC_API_Python.TIC_API import *

from datetime import datetime

import sys
sys.path.append('/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part')
# from SchoolMeal_Part.YoloContainer import *
from SchoolMeal_Part.TIC_Data import *
#from SchoolMeal_Part.DetectObjectProc import *
#from SchoolMeal_Part.DetectMouse_TIC import *
from SchoolMeal_Part.DetectPersonProc import *
# from SchoolMeal_Part.DetectMouseProc import *

############################# NEED Smart outlet #############################
#import RestArea_Part.TapoP100.PyP100.Control_tapo as tapo 

#from sensor import *

def controller():
    
    
    file_list = os.listdir("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Detected_Data") # 현재위치 기준 Voucher_SchoolMeal_Project\SchoolMeal_Part\TIC_Data


    # 만약 파일이 없다면?
    open_list = [open("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/Detected_Data/" + json_path, 'r') for json_path in file_list]
    
    data_list = [json.load(json_open) for json_open in open_list]

    [json_open.close() for json_open in open_list]


    data_dict = {list(data.keys())[0]:list(data.values())[0] for data in data_list}
    time_dict = {list(data.keys())[1]:list(data.values())[1] for data in data_list}
    
    dic = {"lightType": 0}
    TIC_API.getInstance().SetFilePath("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/")    
    TIC_API.getInstance().SaveAllJson(dic, "LightType")
    
    
    for num, key in enumerate(["MousePresentTime", "PersonPresentTime", "ObjectPresentTime", "SmartConsentPresentTime"]): # enumerate 순서와 데이터를 함께 가져옴
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        datetime_result = datetime.strptime(time_dict[key], datetime_format)
        timeDifference = datetime.now() - datetime_result

        now = datetime.now() #.strftime('%Y-%m-%d %H:%M:%S.%f')
        mMornning = now.replace(hour=6, minute=0, second=0, microsecond=0)
        mNight= now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # detection 4가지 문제 생겼을 시 재 실행 각각 5초가 지났을때 실행해야함
        if int(timeDifference.seconds) > 30 : 
            # if key == 'MousePresentTime' : 
            #     print("Mouse, 5 seconds delayed . stop and restart.")
            #     mMousecontroller.StopThread()
            #     mDetectMouse_TIC.StopThread()
            #     if (now < mNight) and (now >= mMornning) :
            #         mMousecontroller.RestartThread()
            #     else :
            #         mDetectMouse_TIC.RestartThread()
            if key == 'PersonPresentTime': 
                print("Person, 5 seconds delayed . stop and restart.")
                mPersoncontroller.StopThread()
                mPersoncontroller.RestartThread()

            # elif key == 'ObjectPresentTime':
            #     print("Object, 5 seconds delayed . stop and restart.")
            #     mObjectcontroller.StopThread()
            #     mObjectcontroller.RestartThread()
            ############################# NEED Smart outlet #############################
            # elif key == 'SmartConsentPresentTime' :
            #     print()

    isMouse, isPerson,isObject,smartConsent = 0, 1, 0, 0
    
    
    for num, key in enumerate(["IsMouse", "IsPerson", "IsObject", "SmartConsent"]):# enumerate 순서와 데이터를 함께 가져옴
        if key == 'IsMouse' : # 사람이 없을 때
            isMouse = data_dict[key]
            
        elif key == 'IsPerson' :
            isPerson = data_dict[key]
        
        elif key == 'IsObject' :
            isObject = data_dict[key]
            
        elif key == 'SmartConsent' : 
            smartConsent = data_dict[key]
            if data_dict[key] == 1:
                ############################# NEED Smart outlet #############################
                #plug = tapo.Plug("IP2")
                #plug.turn_on()
                dic = {"lightType": 2}
            else :
                print()
                ############################# NEED Smart outlet #############################
                #plug.turn_off()

    # 화구 내 기름의 온도를 가져옴
    detected_oil_temperature = 0
    
    TIC_API.getInstance().SetFilePath("/mnt/share/")
    #TIC_API.getInstance().SetFilePath("/home/icns/gitMeal/Voucher_SchoolMeal_Project/")
    
    GetDetectFireList = TIC_API.getInstance().GetConfigData("config")

    GetTemperature = TIC_API.getInstance().GetAllJsonData("TIC_Data")
    GetTemperatureList = GetTemperature["TemperatureList_100"]

    # detected_oil_temperature : 화구에 있는 위치 데이터의 온도 중 가장 큰 온도
    for i in range (0, len(GetDetectFireList)) :
        x = GetDetectFireList[i][0]
        y = GetDetectFireList[i][1]
        if(detected_oil_temperature <= GetTemperatureList[x][y]):
            detected_oil_temperature = GetTemperatureList[x][y]
        

    required_oil_temperature = 50.0 #50.0
    #detected_oil_temperature = 100 # for test, should remove
    


    if (detected_oil_temperature >=required_oil_temperature) and (isPerson == 0):
        dic = {"lightType": 1}
    elif (detected_oil_temperature >= required_oil_temperature) and (isPerson == 1):
        dic = {"lightType": 2}
    else :
        dic = {"lightType": 0}
        print("else lightType: 0")
        print()
    # elif (smartConsent == 1) :
    #     dic = {"lightType": 2}
    # elif isMouse == 1:
    #     dic = {"lightType": 3}
             
             
            
    TIC_API.getInstance().SetFilePath("/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part/TIC_Data/")    
    TIC_API.getInstance().SaveAllJson(dic, "LightType") 
    
    return
    
#### prototype test 이후 삭제 예정 ####
#mObjectcontroller = DetectObjectProc() #  Flammable Object Detection function call
# mObjectcontroller.Run()


#NowFireIndexList = TIC_API.getInstance().GetNowFireCellList("FireResult")
#mPersoncontroller = DetectPersonProc(NowFireIndexList) # Person Detection function call
mPersoncontroller = DetectPersonProc()
# mPersoncontroller.Run()

# 쥐의 경우 낮 / 밤의 경우 특정 시간을 정해서 시간대로 실행 시켜야 함. (현재 오후 23:59:59.999999 ~ 오전 06:00:00.000000)
# mMousecontroller = DetectMouseProc() # 쥐 주간
# mMousecontroller.Run()

#mDetectMouse_TIC = DetectMouse_TIC()  # 쥐 야간
# mDetectMouse_TIC.Run()

while(True):
    if (os.path.isdir("/mnt/share/") is True) and (os.path.isfile("/mnt/share/TIC_Image.jpg") is True):
        function_result = controller()
        time.sleep(3)

# 스마트 콘센트,로고젝트 켤때, 환풍기,주파수
# if __name__ == "__main__":
#     #plug = tapo.Plug("IP1")
#     plug = tapo.Plug("IP2")
#     flag = True

#     while True:
#         if flag:
#             plug.turn_on()
#             flag = False
#         else:
#             plug.turn_off()
#             flag = True

#         time.sleep(3)