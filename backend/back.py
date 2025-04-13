from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)
DATABASE_FILE = "database.json"






def cargar_datos():
    try:
        with open(DATABASE_FILE, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}



def guardar_datos(datos):
    with open(DATABASE_FILE, "w") as archivo:
        json.dump(datos, archivo, indent=4)






@app.route("/registro", methods=["POST"])
def registrar_usuario():
    datos = request.json
    db = cargar_datos()

    if datos["username"] in db:
        return jsonify({"mensaje": "Error: El username ya está registrado"}), 400

    for usuario in db.values():
        if usuario["correo"] == datos["correo"]:
            return jsonify({"mensaje": "Error: El correo ya está registrado"}), 400

    datos["entrada"] = None  
    datos["salida"] = None  
    datos["horas_trabajadas"] = None  
    datos["total_receso"] = "0:00:00"  

    db[datos["username"]] = datos
    guardar_datos(db)
    return jsonify({"mensaje": "Usuario registrado correctamente!"}), 200






@app.route("/login", methods=["POST"])
def iniciar_sesion():
    datos = request.json
    db = cargar_datos()

    for usuario in db.values():
        if usuario["correo"] == datos["correo"] and usuario["contrasena"] == datos["contrasena"]:
            usuario["entrada"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_datos(db)
            return jsonify({"mensaje": "Login exitoso, hora de entrada registrada"}), 200

    return jsonify({"mensaje": "Error: Correo o contraseña incorrectos"}), 400







@app.route("/guardar_tiempo", methods=["POST"])
def guardar_tiempo():
    datos = request.json
    db = cargar_datos()

    correo = datos["correo"]
    if correo not in db:
        return jsonify({"mensaje": "Error: Usuario no encontrado"}), 400

    entrada = datetime.datetime.strptime(db[correo]["entrada"], "%Y-%m-%d %H:%M:%S")
    salida = datetime.datetime.now()
    tiempo_trabajado = salida - entrada - datetime.timedelta(seconds=int(db[correo]["total_receso"].split(":")[2]))  # Descuenta recesos

    db[correo]["salida"] = salida.strftime("%Y-%m-%d %H:%M:%S")
    db[correo]["horas_trabajadas"] = str(tiempo_trabajado)

    guardar_datos(db)
    return jsonify({"mensaje": f"Salida registrada. Tiempo trabajado: {tiempo_trabajado}"}), 200





if __name__ == "__main__":
    app.run(debug=True)