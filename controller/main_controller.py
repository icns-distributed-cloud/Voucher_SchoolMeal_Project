import json
import os
import sys
import time
from TLC_API import *
from datetime import datetime
#import TapoP100.PyP100.Control_tapo as tapo
#from DetectFiretProc import *
from DetectObjectProc import *
from DetectPersonProc import *
from DetectMouseProc import *


def controller(): 
    
    file_list = os.listdir("controller/merge_model_04/") # 현재위치 기준


    # 만약 파일이 없다면?
    open_list = [open("controller/merge_model_04/" + json_path, 'r') for json_path in file_list]
    
    data_list = [json.load(json_open) for json_open in open_list]

    [json_open.close() for json_open in open_list]


    data_dict = {list(data.keys())[0]:list(data.values())[0] for data in data_list}
    time_dict = {list(data.keys())[1]:list(data.values())[1] for data in data_list}

    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    dic = {"result": 0}


    for num, key in enumerate(["MousePresentTime", "PersonPresentTime", "ObjectPresentTime"]): # enumerate 순서와 데이터를 함께 가져옴
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

    for num, key in enumerate(["IsMouse", "IsPerson", "IsObject"]):# enumerate 순서와 데이터를 함께 가져옴
        if key is 'IsPerson' : # 사람이 없을 때
            if data_dict[key] is False: 
                dic = {"lightType": num+1}
                break
        else : 
            if data_dict[key] is True: 
                dic = {"lightType": num+1}
                break
            
    
    TLC_API.getInstance().SaveAllJson(dic, "LightType") 
    
    return 0
    
        
mObjectcontrollerTest = DetectObjectProc() # 물체
mObjectcontrollerTest.Run()

mPersoncontrollerTest = DetectPersonProc() # 사람
mPersoncontrollerTest.Run()

mMousecontrollerTest = DetectMouseProc() # 쥐
mMousecontrollerTest.Run()

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