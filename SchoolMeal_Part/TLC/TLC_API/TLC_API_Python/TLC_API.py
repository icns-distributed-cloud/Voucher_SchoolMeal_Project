from asyncio.windows_events import NULL
import json
import os

#Version 1.01

FilePath = "FLC_Data/"

def WriteJson_All(fileName, data):
    if not os.path.exists(FilePath):
        os.makedirs(FilePath)
    
    if(data != NULL):
        with open(FilePath + fileName + ".json", 'w') as outfile:

            inputData = {}
            inputData['Data'] = []
            inputData['Data'].append(data)

            json.dump(inputData, outfile, indent=4)



def WriteJson(fileName, data):

    if not os.path.exists(FilePath):
        os.makedirs(FilePath)
    
    if(data != NULL):

        with open(FilePath + fileName + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)


def GetJson(fileName):
    with open(FilePath + fileName + ".json", "r") as json_file:
        json_data = json.load(json_file)
        if(json_data != NULL):
            return json_data


#def GetKey(key, data):
#    if key in data:
#        if "Data" in data:
#            print('aa')
#            return data['Data'][key]
#        else:
#            return data[key]

#    else:
#        return NULL



dic = {'name':'pey', 'phone':'0119993323', 'birth': '1118'}
#WriteJson_All("test",dic)
dd = GetJson("test")
print(dd)
print(GetKey("name", dd))

#test_data = GetJson("test")

#print(test_data["name"])

#for key, value in dic.items():
#    print(key + "  " + value)



'''
file_path = "./sample.json"

data = {}
data['posts'] = []
data['posts'].append({
    "title": "How to get stroage size",
    "url": "https://codechacha.com/ko/get-free-and-total-size-of-volumes-in-android/",
    "draft": "false"
})
data['posts'].append({
    "title": "Android Q, Scoped Storage",
    "url": "https://codechacha.com/ko/android-q-scoped-storage/",
    "draft": "false"
})


print(data)

file_path = "./sample.json"
with open(file_path, "r") as json_file:
    json_data = json.load(json_file)
    print(json_data)
    print("\n")
    print(json_data["posts"][0]["title"])
    print("")



WriteJson("sample.json",data)
'''