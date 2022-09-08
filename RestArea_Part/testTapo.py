# reference : https://csatlas.com/python-import-file-module/
import os
import sys
import time

import TapoP100.PyP100.Control_tapo as tapo


if __name__ == "__main__":
    plug = tapo.Plug("IP1")
    flag = True

    while True:
        if flag:
            plug.turn_on()
            flag = False
        else:
            plug.turn_off()
            flag = True

        time.sleep(3)











"""
now_dir = os.path.dirname(__file__)
tapo_dir = os.path.join(now_dir, "..", "TapoP100", "PyP100")
sys.path.append(tapo_dir)

import Control_tapo

Control_tapo.turn_off()
"""