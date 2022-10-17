import serial, time
import threading
import json
import time


class logojector_controller_v1(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.ser_front = serial.Serial(port='/dev/ttyAMA1',baudrate=115200)
		self.home_ver = 0
		self.home_hor = 0

	def home_setting(self):
		file = open('LogojectorData.json')
		jsonString = json.load(file)
        self.home_ver = jsonString.get("home_vertical")
		self.home_hor = jsonString.get("home_horizontal")
		file.close()

	def calculate_CCR(self, width, height, x,y):
		ratio_w = 1
		ratop_h = int(width / (2*height))

		amount_of_change_x = int(x * (400 / (width*ratio_w)))
		amount_of_change_y = int(y * (200 / (height*ratop_h)))

		CCRX = self.home_hor - amount_of_change_x
		CCRY = self.home_ver + amount_of_change_y

		if(CCRX < 250):
			CCRX = 250
		elif(CCRX > 650):
			CCRX = 650

		if(CCRY < 300):
			CCRY = 300
		elif(CCRY > 500):
			CCRY = 500

		return CCRX, CCRY

	def calculate_CCR_loop(self, width, height, x, y):
		try:
			print("열화상 카메라 해상도 수신")
			file = open('Resolution.json')
			jsonString = json.load(file)
			width = jsonString.get("width")
			height = jsonString.get("height")
			is_slippery = jsonString.get("is_slippery")
			file.close()
			while(1):
				if(is_slippery):
					print("미끄럼 구역 확인")
					file = open('SlipperySector.json')
					jsonString = json.load(file)
					x = jsonString.get("x")
					y = jsonString.get("y")
					file.close()
					CCRX,CCRY = self.calculate_CCR(width,height,x,y)

					print("stm32 보드로 전송")
					mytuple = (str(int(CCRX)),",",str(int(CCRY)),"/")
					stm32_msg = "".join(mytuple)
					stm32_msg = stm32_msg.encode('utf-8')
					ser_front = write(stm32_msg)

		except KeyboardInterrupt:
			ser_front.close()
			pass

	def run(self):
		try:
			self.home_setting()
			self.calculate_CCR_loop(width,height,x,y)
					
		except KeyboardInterrupt:
			ser_front.close()
			pass

con = logojector_controller_v1()
con.run()
