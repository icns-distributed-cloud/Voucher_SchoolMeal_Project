import json

file = open('../SchoolMeal_Part/TIC_Data/LightType.json','r', encoding='utf-8')
jsonString = json.load(file)
jsonString['lightType'] = 1
file.close()
file = open('../SchoolMeal_Part/TIC_Data/LightType.json','w', encoding='utf-8')
json.dump(jsonString, file, indent='\t')
file.close()

