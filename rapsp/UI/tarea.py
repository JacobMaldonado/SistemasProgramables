import tkinter
from PIL import ImageTk, Image
# import gpiozero
# Boolean para la pluma
plumaLevantada = False

root = tkinter.Tk()

root.minsize(640,480)
# ports 
#ledPin = gpiozero.PWMLED(17)


frameLU = tkinter.Frame(root)
frameLU.grid(column=1, row=1)
frameRU = tkinter.Frame(root)
frameRU.grid(column=2, row=1)
frameLD = tkinter.Frame(root)
frameLD.grid(column=1, row=2)
frameRD = tkinter.Frame(root)
frameRD.grid(column=2, row=2)


# Comportamiento pluma
def pluma():
    global plumaLevantada
    if not plumaLevantada:
        plumaLevantada = True
        btnPluma["text"] = "Bajar Pluma"
    else:
        plumaLevantada = False
        btnPluma["text"] = "Levantar Pluma"

# Comportamiento ultrasonico
def ultrasonicoAlarma():
    if btnUltra["text"] == "Alarma on":
        btnUltra["text"] = "Alarma off" 
    else:
        btnUltra["text"] = "Alarma on"


# Levantar pluma
btnPluma = tkinter.Button(frameRU, text="Levantar Pluma", command=pluma)
btnPluma.pack()

# Comportamiento temperatura
termometro = tkinter.Canvas(frameRD, bg="white",height=200, width=200)
termometro.grid(column=1, row=1)
load = Image.open("termometro.png").resize((200, 200), Image.LANCZOS)
render = ImageTk.PhotoImage(load)
termometro.create_image(0,0,image = render, anchor = "nw")
# Dibujamos rallitas en el termometro
def dibujarTemp(temp):
    termometro.delete("all")
    termometro.create_image(0,0,image = render, anchor = "nw")
    labelTemp["text"] = "Temperatura: " + str(temp) + "°" 
    if temp > 40:
        termometro.create_rectangle(90,110,110,120, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,90,110,100, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,70,110,80, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,50,110,60, outline="#fb0", fill="#f00")
    elif temp > 30:
        termometro.create_rectangle(90,110,110,120, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,90,110,100, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,70,110,80, outline="#fb0", fill="#f00")
    elif temp > 20:
        termometro.create_rectangle(90,90,110,100, outline="#fb0", fill="#f00")
        termometro.create_rectangle(90,70,110,80, outline="#fb0", fill="#f00")
    elif temp > 10:
        termometro.create_rectangle(90,70,110,80, outline="#fb0", fill="#f00")
# Label temperatura
labelTemp = tkinter.Label(frameRD,text="Temperatura: ")
labelTemp.grid(column=2, row=1)
dibujarTemp(32)

# Comportamiento ultrasonico
ultrasonico = tkinter.Canvas(frameLD, bg="white",height=200, width=200)
ultrasonico.grid(column=1, row=1)
load2 = Image.open("ultra.jpg").resize((200, 200), Image.LANCZOS)
render2 = ImageTk.PhotoImage(load2)
ultrasonico.create_image(0,0,image = render2, anchor = "nw")
# arcos rojos
def arcosUltrasonico(valor):
    ultrasonico.delete("all")
    ultrasonico.create_image(0,0,image = render2, anchor = "nw")
    labelUltra["text"] = "Distancia: " + str(valor)
    if valor > 150:
        ultrasonico.create_arc( 145, 110, 45, 32, start=90, extent=110, outline="red", style="arc", width=10)
        ultrasonico.create_arc( 135, 100, 60, 47, start=90, extent=110, outline="red", style="arc", width=10)
        ultrasonico.create_arc( 125, 90, 75, 62, start=90, extent=110, outline="red", style="arc", width=10)
    elif valor > 50:
        ultrasonico.create_arc( 135, 100, 60, 47, start=90, extent=110, outline="red", style="arc", width=10)
        ultrasonico.create_arc( 125, 90, 75, 62, start=90, extent=110, outline="red", style="arc", width=10)
    elif valor > 20:
        ultrasonico.create_arc( 125, 90, 75, 62, start=90, extent=110, outline="red", style="arc", width=10) 

# Label ultrasonico
labelUltra = tkinter.Label(frameLD,text="Distancia: ")
labelUltra.grid(column=2, row=1)
btnUltra = tkinter.Button(frameLD, text="Alarma on", command=ultrasonicoAlarma)
btnUltra.grid(column=2, row=2)
arcosUltrasonico(50)   

# función led
def prenderLed():
    if btnLed["text"] == "prender led":
        #ledPin.value = 1
        btnLed["text"] = "apagar led"
    else:
        #ledPin.value = 0
        btnLed["text"] = "prender led"


# funcion cambiar intensidad
def intLed(*args):
    for i in args:
        print(i)
    if args[0] == "moveto":
        #args[1] es el valor entre 0 y 1 segun la cantidad
        pass
    elif args[0] == "scroll":
        # Incrementa
        if int(args[1]) > 0:
            pass
        # Decrementa
        elif int(args[1]) < 0:
            pass

# Scrollbar
Main = tkinter.Canvas(frameLU, height = 200,width =50)
Main.configure(scrollregion=Main.bbox("all"))
scroll = tkinter.Scrollbar(frameLU ,orient="vertical", command=intLed)
Main.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")
Main.pack(side = tkinter.BOTTOM, anchor = tkinter.NW,fill="x")
Main.create_line(500, 1000, 1000, 2000)
Main.configure(scrollregion=Main.bbox("all"))
# button
btnLed = tkinter.Button(frameLU, text="prender led", command=prenderLed)
btnLed.pack(side=tkinter.LEFT)
root.mainloop()