import json
import os
while(True):

    # 5초 + 스레드 

    path, dirs, files = next(os.walk("C:/Users/nosul/cont"))
    file_list = os.listdir("./")

    print(path)
    print(dirs)
    print(files)

    path = file_list
    print(path)


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

    #스마트 플러그 와 동시에 켜주세요
    #경광등
    #로보젝트
    #소리