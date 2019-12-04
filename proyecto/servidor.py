from flask import Flask, request, jsonify, redirect
import pyrebase
import datetime
from flask_cors import CORS, cross_origin


config = {
  "apiKey": "AIzaSyA3uxfagTOgqzoy9hdV4M4IH4UIQREGeIg",
  "authDomain": "https://sistemasprogramables-bc045.firebaseapp.com",
  "databaseURL": "https://sistemasprogramables-bc045.firebaseio.com/",
  "storageBucket": "https://sistemasprogramables-bc045.appspot.com"
}

params = {
        "id":1,        
        "temperatura": 28.01,
        "humedad": "18%",
        "luminosidad": 100,
        "movimiento": False,
        "humo": "0%",
        "flama": False
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

sistemas = {
    "sistemaLuces": False,
    "sistemaEnfriamiento": False,
    "sistemaIncendios": False,
    "sistemaAlarma": False,
}

estados = {
    "luz": True,
    "puerta": False,
    "ventilador": False,
    "aspersor": False,
    "alarma": False 
}
# Creamos una copia para compararlos


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/datos", methods=[ "POST"])
def recibirDatos():
    datos = request.get_json()
    print(datos)
    if datos["id"] == 1:
        registrarEnDB(datos)
        logicaSistemas(datos)
        return jsonify(estados)
    
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
        if int(luz) < 100 and movimiento:
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
        
# Ruta de visualización y control
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
        cambiosEnActuador(ultimoEstado, name)
        sistemas["sistemaLuces"] = request.form["sistemaLuces"]== "true"
        sistemas["sistemaEnfriamiento"] = request.form["sistemaEnfriamiento"]== "true"
        sistemas["sistemaIncendios"] = request.form["sistemaIncendios"]== "true"
        sistemas["sistemaAlarma"] = request.form["sistemaAlarma"]== "true"
        cambiosEnSistemas(ultimoSistemas, name)
        return "success"

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

@app.route("/controlUser/<string:name>", methods=["GET", "POST"])
def controlUser(name):
    if request.method == "GET":
        return app.send_static_file('controlUsuario.html')
    elif request.method == "POST":
        print(request.form)
        estados["ventilador"] = request.form["ventilador"] == "true"
        estados["puerta"] = request.form["puerta"]== "true"
        estados["luz"] = request.form["luces"]== "true"
        estados["alarma"] = request.form["alarma"]== "true"
        estados["aspersor"] = request.form["aspersor"]== "true"
        return "success"

@app.route("/agregarUsuario", methods=["GET","POST"])
def agregarUsuario():
    if request.method=="GET":
        return app.send_static_file('addUser.html')
    else:
        val = {
            "pass":request.form["usuario"],
            "tipo":request.form["tipo"]
        }

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


@app.route("/leerdatos", methods=["GET"])
def leer():
    dic = {}
    dic["sensores"] = db.child("ultimo").get().val()
    dic["estados"] = estados
    dic["sistemas"] = sistemas
    return jsonify(dic)


#app.run(host="192.168.43.76", port=4000, debug=True)
#app.run(host="192.168.1.145", port=4000, debug=True)
app.run(host="localhost", port=4000, debug=True)