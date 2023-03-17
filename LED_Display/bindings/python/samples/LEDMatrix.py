import time
import sys
from PIL import Image
from rgbmatrix import *


image_file = "/home/icns/Downloads/spring.png"
image = Image.open(image_file)

options = rgbmatrixoptions()
options.row = 32
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = rgbmatrix(options=options)

image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)