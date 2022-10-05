import json
import os
import time
from TIC_API import *

from datetime import datetime

from DetectObjectProc import *

from SchoolMeal_Part.DeepLearning.PersonDetect.DetectPersonProc import *
from SchoolMeal_Part.DeepLearning.MouseDetect.DetectMouseProc import *
from SchoolMeal_Part.DeepLearning.MouseDetect.DetectMouse_TIC import *

import RestArea_Part.TapoP100.PyP100.Control_tapo as tapo

from sensor import *


def controller(): 
    TIC_API.SetFilePath("SchoolMeal_Part/TIC_Data/")

    file_list = os.listdir("SchoolMeal_Part/TIC_Data/") # 현재위치 기준


    # 만약 파일이 없다면?
    open_list = [open(file_list + json_path, 'r') for json_path in file_list]
    
    data_list = [json.load(json_open) for json_open in open_list]

    [json_open.close() for json_open in open_list]


    data_dict = {list(data.keys())[0]:list(data.values())[0] for data in data_list}
    time_dict = {list(data.keys())[1]:list(data.values())[1] for data in data_list}

    
    for num, key in enumerate(["MousePresentTime", "PersonPresentTime", "ObjectPresentTime", "SmartConsentPresentTime"]): # enumerate 순서와 데이터를 함께 가져옴
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        datetime_result = datetime.strptime(time_dict[key], datetime_format)
        timeDifference = datetime.now() - datetime_result
        
        # detection 4가지 문제 생겼을 시 재 실행 각각 5초가 지났을때 실행해야함
        if int(timeDifference.seconds) > 5 : 
            print("5초 경과했습니다. 강제 종료 후 해당파일 재실행합니다.")
            if key is 'MousePresentTime' : 
                DetectMouseProc.StopThread()
                DetectMouseProc.RestartThread()

            elif key is 'PersonPresentTime':
                DetectPersonProc.StopThread()
                DetectPersonProc.RestartThread()

            elif key is 'ObjectPresentTime':
                DetectObjectProc.StopThread()
                DetectObjectProc.RestartThread()

            elif key is 'SmartConsentPresentTime' :
                print()

    isMouse, isPerson,isObject,smartConsent = 0, 1, 0, 0
    
    
    for num, key in enumerate(["IsMouse", "IsPerson", "IsObject", "SmartConsent"]):# enumerate 순서와 데이터를 함께 가져옴
        if key is 'IsMouse' : # 사람이 없을 때
            isMouse = data_dict[key]
            
        elif key is 'IsPerson' :
            isPerson = data_dict[key]
        
        elif key is 'IsObject' :
            isObject = data_dict[key]
            
        elif key is 'SmartConsent' : 
            smartConsent = data_dict[key]
            if data_dict[key] is 1:
                plug = tapo.Plug("IP2")
                plug.turn_on()
                dic = {"lightType": 2}
            else :
                plug.turn_off()

    isFire = TIC_API.getInstance().GetNowFireCellList("FireResult") 

    dic = {"lightType": 0}

    if (len(isFire) > 0) and (isPerson is 0):
        dic = {"lightType": 1}
    elif (len(isFire) > 0) and (isObject is 1) :
        dic = {"lightType": 2}
    elif (smartConsent is 1) :
        dic = {"lightType": 2}
    elif isMouse is 1:
        dic = {"lightType": 3}
             
        
    TIC_API.getInstance().SaveAllJson(dic, "LightType") 
    
    return 0
    
        
mObjectcontroller = DetectObjectProc() # 물체
mObjectcontroller.Run()

mPersoncontroller = DetectPersonProc() # 사람
mPersoncontroller.Run()

mMousecontroller = DetectMouseProc() # 쥐 야간
mMousecontroller.Run()

mDetectMouse_TIC = DetectMouse_TIC()  # 쥐 야간
mDetectMouse_TIC.Run()

while(True):
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