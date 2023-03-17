import RPi.GPIO as GPIO
import time
import threading
import json


# GPIO.setmode(GPIO.BCM)  # 상위 컨트롤러에서 호출

class frequency_generator_v1(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.frequency_channel = 0
        self.IsMouse = False

    def gpio_setup(self):
        self.frequency_channel = 23
        GPIO.setup(green_channel, GPIO.OUT)

    def sound_off(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def sound_on(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def run(self):
        try:
            while(1):
                file = open('04_ResultDataMouse.json')
                jsonString = json.load(file)
                self.IsMouse = jsonString.get("IsMouse")
                file.close()

                if(IsMouse):
                    sound_on(frequency_channel)
                else:
                    sound_off(green_channel)

	except KeyboardInterrupt:
		GPIO.cleanup()
		pass

	
con = frequency_generator_v1()
con.run()

# GPIO.cleanup() # 상위 컨트롤러에서 호출