import urllib.request
import urllib.parse
import json
import time
from serial import Serial
import threading

import gpiozero
import RPi.GPIO as gpio

# Se habilitan los pines para los ctuadores
ledPin = gpiozero.PWMLED(18)
servoPin = gpiozero.AngularServo(17, min_angle=-180, max_angle=180)
bz = gpiozero.Buzzer(16)
gpio.setmode(gpio.BCM)
gpio.setup(12, gpio.OUT)


# Se habilita el puerto serial para leer los datos del arduino
ser = Serial('/dev/ttyACM0',9600)
s = [0]

# Se establece la estructura de manejo de datos con datos ficticios
params = {
        "id":1,        
        "temperatura": 28.01,
        "humedad": "18%",
        "luminosidad": 100,
        "movimiento": False,
        "humo": "0%",
        "flama": False
    }

# Variables de actuadores uusadas para manipular diversos numeros de actuadores
actuadorLuz = [ledPin]
actuadorPuerta = [servoPin]
actuadorVentilador = [1]
actuadorAspersor = [1]
actuadorAlarma = [bz]

# Petición a el servidor, enviando datos de sensores y recibimos los nuevos estados de los actuadores
def peticion():
    url = "http://192.168.43.76:4000/datos"  
    #url = "http://192.168.1.145:4000/datos"
    # Hacemos un Encode a la información a enviar en formato utf8
    data = json.dumps(params).encode('utf8')
    # Se hace la petición
    request = urllib.request.Request(url,data=data,headers={'content-type': 'application/json'})
    with urllib.request.urlopen( request) as response:         
        # Se lee la respuesta y se cambian valores de los actuadores en base a la respuesta
        response_text = response.read()
        cambiarValores(json.loads(response_text))


# función que actualiza valores de actuadores
def cambiarValores(valores):
    luces(valores["luz"])
    puerta(valores["puerta"])
    ventilador(valores["ventilador"])
    aspersor(valores["aspersor"])
    alarma(valores["alarma"])

# Función que manipula actuadores de luz
def luces(val):
    if val:
        # prendemos cada luz
        for luz in actuadorLuz:
            luz.value = 1
    else:
        # Apagamos cada luz
        for luz in actuadorLuz:
            luz.value = 0

# Función que manipula los servos
def puerta(val):
    if val:
        # Abrir puerta
        for p in actuadorPuerta:
            p.angle = -180
    else:
        # Cerrar puerta
        for p in actuadorPuerta:
            p.angle = 180

# Función que manipula el ventilador
def ventilador(val):
    if val:
        # Prender ventiladores
        for ven in actuadorVentilador:
            gpio.output(12, True)
    else:
        # Apagar ventiladores
        for ven in actuadorVentilador:
            gpio.output(12, False)

# Función para manipular los aspersores
def aspersor(val):
    if val:
        # Prender aspersores
        for asp in actuadorAspersor:
            # TODO: prender aspersor
            bz.on()
    else:
        # Apagar aspersores
        for asp in actuadorAspersor:
            # TODO: apagar aspersor
            bz.off()

# Función para manipular la alarma
def alarma(val):
    if val:
        # Prender alarmas
        for alarm in actuadorAlarma:
            # TODO: prender alarmas
            alarm.on()
            pass
    else:
        # Apagar alarmas
        for alarm in actuadorAlarma:
            # TODO: apagar alarmas
            alarm.off()
            pass

# Función que corre en segundo plano que actualiza los datos de los sensores
def leerSerial():
    # Leemos el serial
    try:
        while True:
            s[0] = str(ser.readline())
            if s[0]:
                print(s[0])
                # Si es de distancia
                if str(s[0]).find("cm") != -1:
                    params["distancia"] = s[0][2:str(s[0]).find("cm") + 2]
                # Si es de la Fotoresistencia
                elif str(s[0]).find("fotores") != -1:
                    params["luminosidad"] = s[0][str(s[0]).find("fotores") + 9: str(s[0]).find("\\") ]
                # Si es de flama
                elif str(s[0]).find("flamita") != -1:
                    params["flama"] = s[0][str(s[0]).find("flamita") + 9: str(s[0]).find("\\") ] == "1"
                # Si es de Humedad
                elif str(s[0]).find("Humedad") != -1:
                    params["humedad"] = s[0][str(s[0]).find("Humedad") + 9: str(s[0]).find("%") - 1 ]
                # Si es de Temperatura
                elif str(s[0]).find("Temperatura") != -1:
                    params["temperatura"] = s[0][str(s[0]).find("Temperatura") + 13: str(s[0]).find("\\") ]
                # Si es de movimiento
                elif str(s[0]).find("mov: ") != -1:
                    params["movimiento"] = int(s[0][str(s[0]).find("mov:") + 5: str(s[0]).find("\\") ]) == 1
    except KeyboardInterrupt:
        gpio.cleanup()
        exit()

    
# METODO PINCIPAL 
def main():
    # Corre la Función "leerSerial" en segundo plano
    threading.Thread(target=leerSerial, daemon=True).start()
    try:
        while True:
            # Hacemos la petición cada medio segundo
            peticion()
            time.sleep(0.5)
    except KeyboardInterrupt:
        gpio.cleanup()
        
# LLamamos al main
main()