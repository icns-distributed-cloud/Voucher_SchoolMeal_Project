import json
import os

# 5초 + 스레드 

'''
import time
# main
if __name__ == "__main__":
    while True:
        with futures.ThreadPoolExecutor() as executor: # Thread를 호출하고 executor 라고 부름
            results = executor.submit(read_detect, weights, source) # 함수이름 (read_detect) # 함수에게 전달할 인자 (weights, source)
        mPerson_Dic = {'person': True}

        # Thread의 return value을 출력
        print(results.result())
        TLC_API.getInstance().SaveAllJson(mPerson_Dic, "ResultDataPerson") 
        break # test 무한루프 탈출용
print('main exits')
'''
def controller(): 

    #path, dirs, files = next(os.walk("D:/controller/merge_model_04"))
    file_list = os.listdir("merge_model_04/") # 현재위치 기준

    #path = file_list

    open_list = [open("merge_model_04/" + json_path, 'r') for json_path in file_list]
    data_list = [json.load(json_open) for json_open in open_list]
    [json_open.close() for json_open in open_list]


    data_dict = {list(data.keys())[0]:list(data.values())[0] for data in data_list}
    print(data_dict)


    '''
    with open('ResultDataFire.json', 'r', encoding='UTF8') as file:
        Fire = json.load(file)
        print(Fire) # 1 불이 있다.

    with open('ResultDataObject.json', 'r', encoding='UTF8') as file:
        Object = json.load(file)
        print(Object) # 2 불주변에 물건이 있다.

    with open('ResultDataPerson.json', 'r', encoding='UTF8') as file:
        Person = json.load(file)
        print(Person) # 3 불주변에 사람이 없다.

    with open('ResultDataMouse.json', 'r', encoding='UTF8') as file:
        Mouse = json.load(file)
        print(Mouse) # 4 쥐가 있다.
    '''

    for num, key in enumerate(["IsFire", "IsObject", "IsPerson", "IsMouse"]): # enumerate 순서와 데이터를 함께 가져옴
        if data_dict[key]: 
            return (num + 1)
        
    return 0
    
    '''
    IsFire,IsObject,IsPerson,IsMouse = 0, 0, 0, 0

    if (Fire["IsFire"] == True ) :
        IsFire = 1
    if (Object["IsObject"] == True) :
        IsObject = 2
    if (Person["IsPerson"] == True) :
        IsPerson = 3
    if (Mouse["IsMouse"] == True) :
        IsMouse = 4

    # 어느것도 미해당시 0
    print(IsFire,IsObject,IsPerson,IsMouse)
    '''
controller()
