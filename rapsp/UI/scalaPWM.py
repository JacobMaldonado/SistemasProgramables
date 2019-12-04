from tkinter import *
import RPi.GPIO as GPIO

def Valor():
    selection = "Intensidad = " + str(var.get())
    labelintensidad.config(text = selection)
    led.ChangeDutyCycle(var.get())
    root.after(1000, Valor)

def iniciarPines():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledpwm, GPIO.OUT)

ledpwm = 18
iniciarPines()
led = GPIO.PWM(ledpwm, 100)
led.start()
root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var)
scale.pack(anchor=CENTER)
labelintensidad = Label(root)
