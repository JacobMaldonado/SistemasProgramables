import RPi.GPIO as gpio
from time import sleep

ledonoff = 18
# Asignamos el mmodo bcm en la rasp
gpio.setmode(gpio.BCM)
# Ponemos el GPIO 18 que es el pin 12 fisico como salida del led
gpio.setup(ledonoff, gpio.OUT)
try:
    while True:
        estado = True
        gpio.output(ledonoff, estado)
        sleep(1)
        estado=False
        gpio.output(ledonoff, estado)
        sleep(1)
except KeyboardInterrupt:
    gpio.cleanup()