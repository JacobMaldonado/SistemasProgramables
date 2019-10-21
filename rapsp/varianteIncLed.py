import RPi.GPIO as gpio

GPIO.setupmode(GPIO.BCM)
GPIO.setup(ledpwm, GPIO.OUT)
led = GPIO.PWM(ledpwm, 100)
led.start(0)
try:
    while True:
        intensidad = float(input("Ingrese una intensidad entre 0 y 100 -> "))
        if intensidad < 0:
            break
        elif intensidad > 0 and intensidad < 101:
            led.ChangeDutyCycle(intensidad)
        else:
            led.ChangeDutyCycle(100)
except KeyboardInterrupt:
    led.stop()
    GPIO.cleanup()