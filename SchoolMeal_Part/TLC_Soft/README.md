## install lib
sudo apt install libgtk-3-dev 
sudo apt install libjpeg-dev 
sudo apt install libusb-1.0-0-dev 
sudo apt install libcjson-dev


## libusb & udev
For access rights of the application to the USB device:

    cp 77-flirone-lusb.rules /lib/udev/rules.d/
    udevadm control --reload-rules


## run
cd in this directory

./flirgtk

