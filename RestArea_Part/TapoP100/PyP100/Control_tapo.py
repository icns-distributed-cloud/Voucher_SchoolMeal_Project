from . import PyP100
from dotenv import load_dotenv
import os

class Plug:
    def __init__(self, ip: str):
        """
        Param -> ip: "IP1" ~ "IP3"
        """
        load_dotenv()

        self.__ip = os.environ.get(ip)
        self.__email = os.environ.get("Email")
        self.__password = os.environ.get("Password")

        self.__p100 = PyP100.P100(self.__ip, self.__email, self.__password)
        self.__p100.handshake()
        self.__p100.login()

    
    def turn_off(self):
        self.__p100.turnOff()                                                                                                     
        print("tapo off!")


    def turn_on(self):
        self.__p100.turnOn()
        print("tapo on!")
