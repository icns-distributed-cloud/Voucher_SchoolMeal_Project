from asyncio.windows_events import NULL
import json

#Version 1.01

FilePath = ""

def WriteJson(fileName, data):
    if(data != NULL):
        with open(FilePath + fileName, 'w') as outfile:
            json.dump(data, outfile, indent=4)


def GetJson(fileName):
    with open(FilePath + fileName, "r") as json_file:
        json_data = json.load(json_file)
        if(json_data != NULL):
            return json_data




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

