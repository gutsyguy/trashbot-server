import RPi.GPIO as gpio
from gpiozero import AngularServo
import time
import sys

s = AngularServo()

def Init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(3, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(5, gpio.OUT)
    gpio.setup(26, gpio.OUT)

def ForwardStride():
    gpio.output(3, True)
    gpio.output(11, False)
    gpio.output(5, True)
    gpio.output(26, False)

# def Transfer():
