<img src="https://user-images.githubusercontent.com/61390950/141596451-c3f69064-7152-4d07-80b0-141b60265c02.png" style="width: 500px; height: 300px; border-radius: 100px">

HID python library for emulating mouse and keyboard on PI zero.

## Setup - Tested on [Raspbian](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit) lite 5.10

1. Install apt dependencies

```bash
sudo apt-get update
sudo apt-get install -y git python3-pip
```  


2. install usb gadget module  https://github.com/Pant3x/rpizero-hid/tree/main/usb_gadget
3. Install `rpizero-hid` with `pip`
```bash
pip3 install rpizero-hid
```

## Usage
Note: You should connect the data usb port (left one) to the raspberry, and NOT the power port  
  
- Control mouse
```python
from rpizero_hid import Mouse
m = Mouse()
for i in range(5):
    m.move_relative(10, 10)
```
- Control keyboard
```python
from rpizero_hid import Keyboard

k = Keyboard()
k.type('Hello world!')
```
