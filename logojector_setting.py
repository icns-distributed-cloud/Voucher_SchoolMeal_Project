import serial, time
import threading
import json
ser_front = serial.Serial(port='/dev/ttyAMA1',baudrate=115200)


global home_ver = 0, home_hor = 0

def home_setting():
        file = open('LogojectorData.json')
        jsonString = json.load(file)
        global home_ver = jsonString.get("home_vertical")
		global home_hor = jsonString.get("home_horizontal")
		file.close()

def set_home():
	try:
		user_setting_ver = home_ver
		user_setting_hor = home_hor
		keyinput = 88

		print("home 초기값으로 로고젝터가 이동합니다")
		mytuple = (str(int(user_setting_ver)),",",str(int(user_setting_hor)),"/")
		stm32_msg = "".join(mytuple)
		stm32_msg = stm32_msg.encode('utf-8')
		ser_front = write(stm32_msg)

		while(1):
			currunt_state_print = '현재 상태 ver : {0}, hor : {1}'.format(user_setting_ver,user_setting_hor)
			print(currunt_state_print)
			
			print("0 입력 시 설정 종료")
			print("1 입력 시 설정 시작")
			keyinput = int(input("입력 : "))
			if(keyinput == 0):
				break
			else :
				user_setting_ver = int(input("ver setting : 300~500사이 값 입력 "))
				user_setting_hor = int(input("hor setting : 250~650사이 값 입력 "))

				if(ver < 300 or ver > 500):
					print("ver 값은 300이상 500이하의 값만 설정 가능합니다")
					continue
				
				if(hor < 250 or hor > 650):
					print("hor 값은 250이상 650이하의 값만 설정 가능합니다")
					continue

				print("stm32 보드로 전송")
				mytuple = (str(int(user_setting_ver)),",",str(int(user_setting_hor)),"/")
				stm32_msg = "".join(mytuple)
				stm32_msg = stm32_msg.encode('utf-8')
				ser_front = write(stm32_msg)

		global home_ver = user_setting_ver
		global home_hor = user_setting_hor	

		file = open('LogojectorData.json')
        jsonString = json.load(file)
		file.close()
		jsonString['home_vertical'] = home_ver
		jsonString['home_horizontal'] = home_hor

		with open('LogojectorData.json', 'w', encoding='utf-8') as f:
			json.dump(jsonString, f, indent="\t")
		
		f.close()

	except KeyboardInterrupt:
		ser_front.close()
		pass


def calculate_CCR(width, height, x,y):
	ratio_w = 1
	ratop_h = int(width / (2*height))

	amount_of_change_x = int(x * (400 / (width*ratio_w)))
	amount_of_change_y = int(y * (200 / (height*ratop_h)))

	CCRX = home_hor - amount_of_change_x
	CCRY = home_ver + amount_of_change_y

	if(CCRX < 250):
		CCRX = 250
	elif(CCRX > 650):
		CCRX = 650

	if(CCRY < 300):
		CCRY = 300
	elif(CCRY > 500):
		CCRY = 500

	return CCRX, CCRY


event = threading.Event()


def calculate_CCR_loop(width, height, x, y):

	#change x,y to ver,hor
	try:
		while(1):

			if event.is_set():
				print("calculate CCR loop가 종료되었습니다")
				return
			
			CCRX,CCRY = calculate_CCR(width,height,x,y)

			print("stm32 보드로 전송")
			mytuple = (str(int(CCRX)),",",str(int(CCRY)),"/")
			stm32_msg = "".join(mytuple)
			stm32_msg = stm32_msg.encode('utf-8')
			ser_front = write(stm32_msg)

	except KeyboardInterrupt:
		ser_front.close()
		pass


def select_mode_number():

	

	print("mode select")
	print("1 : home setting")
	print("2 : logojector operation")
	print("3 : logojector test")

	setting_number = int(input("input : "))

	return setting_number


if __name__ == '__main__':
	try:
		while(1):
			mode_number = select_mode_number()
			if(mode_number == 1):
				event.set()
				time.sleep(1)
				set_home()

			elif(mode_number == 2):
				event.clear()
				print("calculate CCR loop가 실행됩니다")
				time.sleep(1)
				cal_thread = threading.Thread(target=calculate_CCR_loop, args=(width, height, x, y), daemon = True)
				cal_thread.start()
				

	except KeyboardInterrupt:
		ser_front.close()
		pass

	
