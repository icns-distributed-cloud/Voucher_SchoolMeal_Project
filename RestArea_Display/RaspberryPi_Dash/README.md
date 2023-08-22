# 라즈베리파이 디스플레이용 소스코드 사용 법

## 1. Raspberry 환경

[Raspberry Pi OS](https://www.raspberrypi.com/software/)를 사용 및 [도커](https://docs.docker.com/get-docker/)를 설치한다.

## 2. Database

MySQL 이미지로 도커 컨테이너를 생성해 3306포트를 통해 MySQL을 실행한다.

## 3. Controller.py 수정
```
# Controller.py의 config 정보를 수정해주어야 한다.

# host: 기본적으로 localhost로 설정되어있음, 본인 database ip로 변경가능

# port: 포트는 2번에서 생성한 3306포트로 지정

# user: 2번에서 설정한 user명

# password: 2번에서 설정한 password


 con = pymysql.connect(host="localhost",
 port=3306, 
 user=USER, 
 password=PW, 
 db ="sensor_data")
```

## 4. 센서 데이터 수집

센서 데이터 수집을 위해 Controller.py를 실행한다.
```
python3 Controller.py
```

## 5. Dash 설정
Web_Dashboard 디렉토리에서 app.py를 실행한다.
```
python3 app.py
```