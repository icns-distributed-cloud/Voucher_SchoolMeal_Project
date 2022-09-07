from TLC_API import * # Should Import API

#---------------------- How to Use --------------------------#


## FilePath
TLC_API.getInstance().SetFilePath("SchoolMeal_Part/FLC_Data/") # If You want use other FilePath, You can set W/R file path, Default path is "FLC_Data/", First argument value is Change FilePath


## Save Json File Data
mTest_Dic = {'IsFire': True} # You Have Use Dictionary when save Data, It's Test Dictionary
TLC_API.getInstance().SaveAllJson(mTest_Dic, "ResultData") # Save JsonData, Fir argument value is Dictionary, Second value is FileName


## Get Json File Data
All_TCL_Data = TLC_API.getInstance().GetAllJsonData("DummyData") # Load All data of TLC Data (Temperature Data, Fire Data...), First argument value is FileNam. Return value is Dictionary about TLC Data

TmperatureList_10x10 = TLC_API.getInstance().GetTmperatureList(PixelType.TenByTen.value, "DummyData") # Get TCL->TemperatureList about 10x10 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array
TmperatureList_40x40 = TLC_API.getInstance().GetTmperatureList(PixelType.FortyByForty.value, "DummyData") # Get TCL->TemperatureList about 40x40 List, First argument value is PixelType, Sceond value is FileName. Return value is 2 Dimensional Array

FireList = TLC_API.getInstance().GetAllFireList("FireResult") # Get TCL->Fire about 10x10 List, First argument is FileName. Return value is 2 Dimensional Array
NowFireCellList = TLC_API.getInstance().GetNowFireCellList("FireResult") # Get Get Now Fire Cell in 10x10 All Fire List. return 2 Dimensional Array


## Get Image Pixel Position Data##
AllPixelList_10x10 = TLC_API.getInstance().GetAllCellData(PixelType.TenByTen.value) # Get All Cell Data, is 10 x 10 Data, First argumenet value is PixelType. return value is 3 Dimensional Array
AllPixelList_40x40 = TLC_API.getInstance().GetAllCellData(PixelType.FortyByForty.value) # Get All Cell Data, is 40 x 40 Data, First argumenet value is PixelType. return value is 3 Dimensional Array

OnePixel_10x10 = TLC_API.getInstance().GetOneCellData(0, 0, PixelType.TenByTen.value) # Get One Cell in 10 x 10 Data, First,Second argument value is x,y vertex, Third is PixelType, return 2 Dimensional Array, 
OnePixel_40x40 =TLC_API.getInstance().GetOneCellData(0, 0, PixelType.FortyByForty.value) # Get One Cell in 40 x 40 Data, First,Second argument value is x,y vertex, Third is PixelType, return 2 Dimensional Array, 


#---------------------- How to Use --------------------------#