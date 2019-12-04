import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(12, gpio.OUT)
gpio.output(12, True)
time.sleep(10)
gpio.output(12, False)
