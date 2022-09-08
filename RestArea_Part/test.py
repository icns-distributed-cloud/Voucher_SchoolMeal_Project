import time
import threading
import Adafruit_DHT
import datetime as dt
from dateutil.tz import gettz
try:
    import RPi.GPIO as GPIO
    #GPIO.setwarnings(False)
except RuntimeError:
    print("[Error] Cannot import RPI.GPIO!")


def Dht():
    dhtDevice = Adafruit_DHT.DHT11
    dhtPin = 18

    while True:
        try:
            today = dt.datetime.now(gettz('Asia/Seoul')).isoformat()
            humid, tempC = Adafruit_DHT.read_retry(dhtDevice, dhtPin)

            print("[Time: {}]\nTemperature: {:.1F}C / Humidity: {}%".format(today, tempC, humid))
            time.sleep(1)
        
        except KeyboardInterrupt:
            pass
            print("Exit with ^C")
            GPIO.cleanup()
            exit()
            

def Gas():
    try:
        gasPin = 4

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gasPin, GPIO.IN)

        while True:
            if GPIO.input(gasPin):
                print("YES!")
            else:
                print("NO!")

            time.sleep(1)
    
    except KeyboardInterrupt:
        pass
        print("Exit with ^C")
        GPIO.cleanup()
        exit()


def Cds():
    GPIO.setmode(GPIO.BCM)
    CdsPin = 11

    while True:
        try:
            GPIO.setup(CdsPin, GPIO.OUT)
            GPIO.output(CdsPin, GPIO.LOW)
            time.sleep(0.1)

            GPIO.setup(CdsPin, GPIO.IN)
            CdsTime = time.time()
            CdsDiff = 0

            print(GPIO.input(CdsPin))
            print(GPIO.LOW)

            while(GPIO.input(CdsPin) == GPIO.LOW):
                CdsDiff = time.time() - CdsTime

            print(CdsDiff*1000)
            time.sleep(1)

        except KeyboardInterrupt:
            pass
            print("Exit with ^C")
            exit()


if __name__ == "__main__":
    Cds()


"""import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("[Error] Cannot import RPI.GPIO!")

GPIO.setmode(GPIO.BOARD)
CdsPin = 5
CdsResultPin = 6

while True:
    try:
        GPIO.setup(CdsPin, GPIO.OUT)
        GPIO.output(CdsPin, GPIO.LOW) 
        time.sleep(0.1)

        GPIO.setup(CdsResultPin, GPIO.IN)
        GPIO.output(CdsResultPin, GPIO.LOW)

        print(GPIO.output(CdsResultPin))
        time.sleep(1)

    except KeyboardInterrupt:
        pass
        print("Exit with ^C")
        exit()"""

"""
def Cds():
    GPIO.setmode(GPIO.BOARD)
    CdsPin = 11

    while True:
        try:
            GPIO.setup(CdsPin, GPIO.OUT)
            GPIO.output(CdsPin, GPIO.LOW)
            time.sleep(0.1)

            GPIO.setup(CdsPin, GPIO.IN)
            count = 0

            #print(GPIO.input(CdsPin))
            #print(GPIO.LOW)

            while(GPIO.input(CdsPin) == GPIO.LOW):
                print(count)
                count += 1

            print(count)
            time.sleep(1)

        except KeyboardInterrupt:
            pass
            print("Exit with ^C")
            GPIO.cleanup()
            exit()

"""