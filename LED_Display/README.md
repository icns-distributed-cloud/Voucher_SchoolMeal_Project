# LED_Display

### Clone

```
git clone https://github.com/icns-distributed-cloud/LED_Display.git
```

### Package Install

```
pip install -r requirements.txt
```

### Action

```
cd bindings/python/samples

sudo python3 displaydata.py --led-cols=64 --led-no-hardware=LED_NO_HARDWARE_PULSE --led-slowdown-gpio=4

```

### Result
![image](https://user-images.githubusercontent.com/70564639/209068191-5a7f557b-a98c-4da0-aab7-744ff9480da7.png)

### Related with
```
덕인이 열화상 repo
```

### Notice
```
라즈베리파이 또는 인터넷 환경에 따라 TIC_Data.json을 실시간으로 읽어오지 못하고 딜레이가 생기는 에러가 발생할 수 있습니다.
이때, 본 프로그램을 사용하는 기기의 파일 읽기/쓰기 권한을 확인하거나,
Voucher_SchoolMeal_Project/SchoolMeal_Part/FireDetect/DetectFiretProc.py의 __Second를 늘려서 동시에 같은 파일에 접근하지 않도록하여 해결할 수 있습니다.
```
