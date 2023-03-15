import subprocess
import time

## ------------------ How to Use -----------------#

##########proc = CheckCameraProc()
###############proc.Run()

time.sleep(30)
##############subprocess.run(["sudo ./flirgtk"], shell = True)


while(True):
    subprocess.run(["sudo ./flirgtk"], shell = True)
    print("Start")
## ------------------ How to Use -----------------#

