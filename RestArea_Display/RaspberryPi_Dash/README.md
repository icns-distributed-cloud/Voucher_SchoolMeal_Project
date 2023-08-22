# 라즈베리파이 소스코드 사용 법

## 1. Raspberry 환경

[Raspberry Pi OS](https://www.raspberrypi.com/software/)를 사용 및 [도커](https://docs.docker.com/get-docker/)를 설치한다.

## 2. Database

도커 컨테이너를 생성해 그 안에 3306포트를 통해 MySQL을 띄운다.

## 3. 센서 데이터 수집

센서 데이터 수집을 위해 Controller.py를 실행한다.
```
python3 Controller.py
```

## 4. Daash 설정
Web_Dashboard 디렉토리에서 app.py를 실행한다.
```
python3 app.py
```