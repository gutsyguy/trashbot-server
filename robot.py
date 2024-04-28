import RPi.GPIO as gpio
from gpiozero import AngularServo
from time import sleep
import sys

s = AngularServo(21, min_angle=0, max_angle=180)

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

def BackwardStride():
    gpio.output(3, False)
    gpio.output(11, True)
    gpio.output(5, False)
    gpio.output(26, True)

def TrayCollection(s):
    s.angle = 0
    sleep(1)
    s.angle = 100
    sleep(1)
    s.angle()
