import subprocess
import threading
import os
import sys
import time

sys.path.append('/home/icns/gitMeal/Voucher_SchoolMeal_Project/')
sys.path.append('/home/icns/gitMeal/Voucher_SchoolMeal_Project/SchoolMeal_Part')

def LED_Start():
    subprocess.run(["python3 led_controller_v1.py"], shell = True)
	
    #subprocess.call(["cd controller", "python3 led_controller_v1.py"], shell=True)
    #subprocess.call("python3 led_controller_v1.py", shell=True)
	
def Detect_Start():
	subprocess.call(["python3 main_controller.py"], shell = True)
	
	
while(True):
	if (os.path.isdir("/mnt/share/") is True) and (os.path.isfile("/mnt/share/TIC_Image.jpg") is True):
		LED_Thread = threading.Thread(target=LED_Start)
		LED_Thread.daemon = True
		LED_Thread.start()
		subprocess.run(["python3 main_controller.py"], shell = True, cwd = "/home/icns/gitMeal/Voucher_SchoolMeal_Project/")
		break
	time.sleep(1)

#subprocess.SW_HIDE = 1

#r = subprocess.Popen(r'/home/icns/gitMeal/Voucher_SchoolMeal_Project/', shell=True).wait()


#Detect_Thread = threading.Thread(target=Detect_Start)
#Detect_Thread.daemon = True
#Detect_Thread.start()

#print("aaa")
#subprocess.call(["python3 main_controller.py"], shell = True)
#subprocess.call(["python3 led_controller_v1.py"], shell = True)