import RPi.GPIO as GPIO
from time import sleep

ledpwm = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledpwm, GPIO.OUT)
led = GPIO.PWM(ledpwm, 100)

try:
    while True:
        led.start(0)
        for x in range(1,10):
            led.ChangeDutyCycle(x * 10)
            sleep(1)
except KeyboardInterrupt:
    led.stop()
    GPIO.cleanup()        