import RPi.GPIO as GPIO
import time
import threading
import json


# GPIO.setmode(GPIO.BCM)  # 상위 컨트롤러에서 호출

class led_controller_v1(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.green_channel = 0
		self.red_channel = 0
		self.blue_channel = 0
		self.buzzer_channel = 0

	def gpio_setup(self):
		self.green_channel = 17
		self.red_channel = 27
		self.blue_channel = 22
		self.buzzer_channel = 10
		
		GPIO.setup(self.green_channel, GPIO.OUT)
		GPIO.setup(self.blue_channel, GPIO.OUT)
		GPIO.setup(self.buzzer_channel, GPIO.OUT)
		GPIO.setup(self.red_channel, GPIO.OUT)

	def light_on(self, pin):
	GPIO.output(pin, GPIO.LOW)

	def light_off(self, pin):
	GPIO.output(pin, GPIO.HIGH)

	def run(self):
		try:
			light_off(green_channel)
			light_off(red_channel)
			light_off(blue_channel)
			light_off(buzzer_channel)

				while(1):
					time.sleep(1)
					file = open('LightType.json')
					jsonString = json.load(file)
					lightType = jsonString.get("lightType")
					file.close()

					#lightType만 받고 다시 파일 값은 0으로 바꿔준다.
					jsonString["lightType"] = 0
					with open('LightType.json', 'w', encoding='utf-8') as f:
						json.dump(jsonString, f, indent="\t")
					f.close()

					if(lightType == 1):
						light_on(red_channel)
						time.sleep(2)
						light_off(red_channel)
					elif(lightType == 2):
						light_on(red_channel)
						light_on(blue_channel)
						time.sleep(2)
						light_off(red_channel)
						light_off(blue_channel)
					elif(lightType == 3):
						light_on(red_channel)
						light_on(green_channel)
						time.sleep(2)
						light_off(red_channel)
						light_off(green_channel)
					elif(lightType == 4):
						light_on(buzzer_channel)
						time.sleep(2)
						light_off(buzzer_channel)
					else:
						GPIO.cleanup()
						break

					
			except KeyboardInterrupt:
				GPIO.cleanup()
				pass
			
con = led_controller_v1()
con.run()

#GPIO.cleanup()


		
	