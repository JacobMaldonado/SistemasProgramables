import RPi.GPIO as GPIO
from tkinter import *
from gpiozero import Buzzer
def RuidoBuzzer():
    global bz
    global ruido
    if ruido:
        bz.off()
    else:
        bz.on()
    ruido = not ruido

def IniciarPines():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpiobuzzer, GPIO.OUT)
gpiobuzzer = 16
IniciarPines()
bz = Buzzer(gpiobuzzer)
ruido = False
root = Tk()
btn_Buz16 = Button(root, text="RuidoBuzzer", command=RuidoBuzzer)
btn_Buz16.pack()
root.mainloop()

