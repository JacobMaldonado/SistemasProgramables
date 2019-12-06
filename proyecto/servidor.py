from flask import Flask, request, jsonify, redirect
import pyrebase
import datetime
from flask_cors import CORS, cross_origin

# Configuración de la base de datos de firebase
config = {
  "apiKey": "AIzaSyA3uxfagTOgqzoy9hdV4M4IH4UIQREGeIg",
  "authDomain": "https://sistemasprogramables-bc045.firebaseapp.com",
  "databaseURL": "https://sistemasprogramables-bc045.firebaseio.com/",
  "storageBucket": "https://sistemasprogramables-bc045.appspot.com"
}

# Establecemos la estructura de los parametros que recibiremos con parametros irrelevantes
params = {
        "id":1,        
        "temperatura": 28.01,
        "humedad": "18%",
        "luminosidad": 100,
        "movimiento": False,
        "humo": "0%",
        "flama": False
    }

# Iniciamos la conexión a la base de datos
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Diccionario que nos permite conocer el estado actual de los sistemas, inicializado con valores irrelevantes
sistemas = {
    "sistemaLuces": False,
    "sistemaEnfriamiento": False,
    "sistemaIncendios": False,
    "sistemaAlarma": False,
}

# Diccionario que se mandara como respuesta a la rasp para cambiar el estado de los actuadores
estados = {
    "luz": True,
    "puerta": False,
    "ventilador": False,
    "aspersor": False,
    "alarma": False 
}

# Instanciamos el servicio WEB
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Ruta que permite leer los datos de los sensores enviados por la rasp
@app.route("/datos", methods=[ "POST"])
def recibirDatos():
    datos = request.get_json()
    print(datos)
    if datos["id"] == 1:
        #registrarEnDB(datos)
        logicaSistemas(datos)
        return jsonify(estados)

# Ruta para conectarse como usuario
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return app.send_static_file('login.html')
    if request.method == "POST":
        val = {}
        try:
            val = db.child("usuarios").child(request.form["usuario"]).get().val()
            print(val)
            if val["pass"] == request.form["contraseña"]:
                registrarLogin(request.form["usuario"], val)
                if val["tipo"] == "admin":
                    print( request.form["usuario"])
                    print( request.form["contraseña"])
                    return redirect("/control/" + request.form["usuario"])
                elif val["tipo"] == "mant":
                    return redirect("/controlMant/" + request.form["usuario"])
                else:
                    return redirect("/controlUser/" + request.form["usuario"])
        except:
            return "El usuario no existe"
        
# Ruta de visualización y control de administrador
@app.route("/control/<string:name>", methods=["GET", "POST"])
def control(name):
    if request.method == "GET":
        return app.send_static_file('control.html')
    elif request.method == "POST":
        ultimoEstado = estados.copy()
        ultimoSistemas = sistemas.copy()
        estados["ventilador"] = request.form["ventilador"] == "true"
        estados["puerta"] = request.form["puerta"]== "true"
        estados["luz"] = request.form["luces"]== "true"
        estados["alarma"] = request.form["alarma"]== "true"
        estados["aspersor"] = request.form["aspersor"]== "true"
        #cambiosEnActuador(ultimoEstado, name)
        sistemas["sistemaLuces"] = request.form["sistemaLuces"]== "true"
        sistemas["sistemaEnfriamiento"] = request.form["sistemaEnfriamiento"]== "true"
        sistemas["sistemaIncendios"] = request.form["sistemaIncendios"]== "true"
        sistemas["sistemaAlarma"] = request.form["sistemaAlarma"]== "true"
        #cambiosEnSistemas(ultimoSistemas, name)
        return "success"

# Ruta de visualización y control de Mantenimiento
@app.route("/controlMant/<string:name>", methods=["GET", "POST"])
def controlMant(name):
    if request.method == "GET":
        return app.send_static_file('controlMantenimiento.html')
    elif request.method == "POST":
        print(request.form)
        ultimoEstado = estados.copy()
        estados["ventilador"] = request.form["ventilador"] == "true"
        estados["puerta"] = request.form["puerta"]== "true"
        estados["luz"] = request.form["luces"]== "true"
        estados["alarma"] = request.form["alarma"]== "true"
        estados["aspersor"] = request.form["aspersor"]== "true"
        cambiosEnActuador(ultimoEstado, name)
        return "success"

# Ruta de visualización y control de usuario normal
@app.route("/controlUser/<string:name>", methods=["GET", "POST"])
def controlUser(name):
    if request.method == "GET":
        return app.send_static_file('controlUsuario.html')

# Ruta de prueba para añadir usuarios
@app.route("/agregarUsuario", methods=["GET","POST"])
def agregarUsuario():
    if request.method=="GET":
        return app.send_static_file('addUser.html')
    else:
        val = {
            "pass":request.form["usuario"],
            "tipo":request.form["tipo"]
        }

# Ruta para que las paginas consulten el estado actual de los sensores
@app.route("/leerdatos", methods=["GET"])
def leer():
    dic = {}
    #dic["sensores"] = db.child("ultimo").get().val()
    dic["estados"] = estados
    dic["sistemas"] = sistemas
    return jsonify(dic)
    
# Registrar valores de los sensores
def registrarEnDB(datos):
    db.child("ultimo").set(datos)
    db.child("lecturas").push(datos)

# Registrar cambios en los actuadores
def cambiosEnActuador(ultimoEstado, usuario):
    if estados != ultimoEstado:
        registrarCambio(estados, ultimoEstado, "cambiosActuadores", usuario)

# Registra cambios tomando el actual y el anterior
def registrarCambio(act, ant, ref, usuario): 
    datos = {}
    datos["fecha"] = str(datetime.datetime.now()).replace(" ", "/")
    datos["usuario"] = usuario
    datos["privilegio"] = db.child("usuarios").child(usuario).get().val()["tipo"]
    for x in act:
        if act[x] != ant[x]:
            datos["cambio"] = x
            datos["estadoNuevo"] = act[x]
            datos["estadoAnterior"] = ant[x]
    db.child(ref).push(datos)


# Función que controla el sistema de enfriamiento
def sistemaEnfriamiento(temp, humedad):
    if sistemas["sistemaEnfriamiento"]:
        if float(temp) > 25 or float(humedad) > 25:
            # Prender ventiladores
            estados["ventilador"] = True
        else:
            # Apagar Ventiladores
            estados["ventilador"] = False

# Función que controla el Sistema de Incendios
def sistemaIncendios(flama):
    if sistemas["sistemaIncendios"]:
        if flama:
            # Prendemos el aspersor
            estados["aspersor"] = True
        else:
            # Apagamos el aspersor
            estados["aspersor"] = False

# Función que controla el sistema de Alarma
def sistemaAlarma(movimiento):
    if sistemas["sistemaAlarma"]:
        if movimiento:
            # Prendemos la alarma
            estados["alarma"] = True
        else:
            # Apagamos la alarma
            estados["alarma"] = False


# Función que controla el sistema de Luces
def sistemaLuces(luz, movimiento):
    if sistemas["sistemaLuces"]:
        if int(luz) < 20 and movimiento:
            # Prendemos el sistema de luces
            estados["luces"] = True
        else:
            # Las apagamos
            estados["luces"] = False

# Función principal de logica
def logicaSistemas(datos):
    sistemaLuces(datos["luminosidad"], datos["movimiento"])
    sistemaEnfriamiento(datos["temperatura"], datos["humedad"])
    sistemaIncendios(datos["flama"])
    sistemaAlarma(datos["movimiento"])



# Registrar cambios en los sistemas
def cambiosEnSistemas(ultimoSistemas, usuario):
    if sistemas != ultimoSistemas:
        registrarCambio(sistemas, ultimoSistemas, "cambioSistemas", usuario)

# Registrar login en bd
def registrarLogin(usuario, datos):
    val = {}
    val["fechaIngreso"] = str(datetime.datetime.now()).replace(" ", "/")
    val["usuario"] = usuario
    val["tipoUsuario"] = datos["tipo"]
    db.child("logins").push(val)

# Corremos el servicio web en el puerto 4000 con la ip segun la red
#app.run(host="192.168.43.76", port=4000, debug=True)
#app.run(host="192.168.1.145", port=4000, debug=True)
app.run(host="localhost", port=4000, debug=True)