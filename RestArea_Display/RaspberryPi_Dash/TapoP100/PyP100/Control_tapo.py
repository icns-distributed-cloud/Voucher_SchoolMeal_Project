from . import PyP100
from dotenv import load_dotenv
import os

class Plug:
    def __init__(self, ip: str, email, pw, name):
        """
        Param -> ip: "IP1" ~ "IP3"
        """
        load_dotenv()

        self.__ip = ip
        self.__email = email
        self.__password = pw
        self.__name = name

        self.__p100 = PyP100.P100(self.__ip, self.__email, self.__password)
        self.__p100.handshake()
        self.__p100.login()

    def reconnect(self):
        self.__p100.handshake()
        self.__p100.login()
    
    def turn_off(self):
        self.__p100.turnOff()                                                                                                     
        print(f"{self.__name} tapo off!")


    def turn_on(self):
        self.__p100.turnOn()
        print(f"{self.__name} tapo on!")
