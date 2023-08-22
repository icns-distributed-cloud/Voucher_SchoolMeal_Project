FROM python:3.10.8

WORKDIR /app
copy . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "Controller.py"]
