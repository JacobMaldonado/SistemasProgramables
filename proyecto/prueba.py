import urllib.request
import urllib.parse
import json
import time

params = {
        "id":1,        
        "temperatura": 28.10,
        "humedad": "19%",
        "luminosidad": 100,
        "movimiento": False,
        "humo": "0%",
        "flama": False
    }

# Variables de actuadores
actuadorLuz = []
actuadorPuerta = []
actuadorVentilador = []
actuadorAspersor = []
actuadorAlarma = []

# Petición a el servidor
def peticion():
    url = "http://127.0.0.1:4000/datos"  
    data = json.dumps(params).encode('utf8')
    request = urllib.request.Request(url,data=data,headers={'content-type': 'application/json'})
    with urllib.request.urlopen( request) as response:         
        response_text = response.read()         
        print( response_text )


# función que actualiza valores de actuadores
def cambiarValores(valores):
    luces(valores["luz"])
    puerta(valores["puerta"])
    ventilador(valores["ventilador"])
    aspersor(valores["aspersor"])
    alarma(valores["alarma"])

def luces(val):
    if val:
        # prendemos cada luz
        for luz in actuadorLuz:
            # TODO: prender luces 
            pass
    else:
        # Apagamos cada luz
        for luz in actuadorLuz:
            # TODO: Apagar luces
            pass

def puerta(val):
    if val:
        # Abrir puerta
        for p in actuadorPuerta:
            # TODO: Abrir puerta
            pass
    else:
        # Cerrar puerta
        for p in actuadorPuerta:
            # TODO: Cerrar puerta
            pass

def ventilador(val):
    if val:
        # Prender ventiladores
        for ven in actuadorVentilador:
            # TODO: prender ventilador
            pass
    else:
        # Apagar ventiladores
        for ven in actuadorVentilador:
            # TODO: apagar ventilador
            pass

def aspersor(val):
    if val:
        # Prender aspersores
        for asp in actuadorAspersor:
            # TODO: prender aspersor
            pass
    else:
        # Apagar aspersores
        for asp in actuadorAspersor:
            # TODO: apagar aspersor
            pass

def alarma(val):
    if val:
        # Prender alarmas
        for alarm in actuadorAlarma:
            # TODO: prender alarmas
            pass
    else:
        # Apagar alarmas
        for alarm in actuadorAlarma:
            # TODO: apagar alarmas
            pass
    
# METODO PINCIPAL 
def main():
    #while True:
    peticion()
    time.sleep(0.01)

main()
