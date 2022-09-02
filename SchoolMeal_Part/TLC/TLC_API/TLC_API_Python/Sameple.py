from TLC_API import * # Should Import API

#---------------------- How to Use --------------------------#    
   
mTLC_API = TLC_API()  # 1. Initialization

## Save Json File Data
mTest_Dic = {'ssaa': True} # You Have Use Dictionary
mTLC_API.SaveAllJson(mTest_Dic, "DummyDataT") # Save JsonData, Fir argument value is Dictionary, Second value is FileName


## Load&Get Json File Data
mTLC_API.SetFilePath("FLC_Data/") # You can seet W/R file path, Default path is "FLC_Data/", First argument value is Change FilePath
mTLC_API.LoadAllJsonData("DummyData") # Load All data of TLC Data (Temperature Data, Fire Data...), First argument value is FileNam. Return value is Dictionary about TLC Data

mTLC_API.GetTmperatureList(PixelType.TenByTen, "DummyData") # Get TCL->TemperatureList about 10x10 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array
mTLC_API.GetTmperatureList(PixelType.FortyByForty, "DummyData") # Get TCL->TemperatureList about 40x40 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array

mTLC_API.GetFireList("DummyData") # Get TCL->Fire about 10x10 List, First argument is FileName. Return value is 2 Dimensional Array

## Get Image Pixel Position Data##
mTLC_API.GetAllPixelData(PixelType.TenByTen) # Get All Pixell Data, is 10x10 Data, return value is 3 Dimensional Array
mTLC_API.GetAllPixelData(PixelType.FortyByForty) # Get All Pixell Data, is 40x40 Data, return value is 3 Dimensional Array

mTLC_API.GetOnePixelData(0, 5, PixelType.TenByTen) # Get One Pixel(cell) in 10x10 Data, return 2 Dimensional Array, First,Second argument value is x,y vertex, Third is PixelType
mTLC_API.GetOnePixelData(15, 27, PixelType.FortyByForty) # Get One Pixel(cell) in 40x40 Data, return 2 Dimensional Array, First,Second argument value is x,y vertex, Third is PixelType




#---------------------- How to Use --------------------------#