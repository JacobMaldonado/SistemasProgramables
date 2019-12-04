from tkinter import *
from gpiozro import AngularServo
def ServoMotor():
    global abierto
    if abierto:
        sermot.angle = 0
        servoEtqBoton = "Abrir"
    else:
        sermot.angle=90
        servoEtqBoton = "Cerrar"
    btn_servo.configure(text = servoEtqBoton)
    abierto = not abierto
gpioservo = 17
abierto = False 
sermot = AngularServo(gpioservo)
root = Tk()
btn_servo = Button(root, text = "Abrir", command=ServoMotor)
btn_servo.pack()
root.mainloop()
