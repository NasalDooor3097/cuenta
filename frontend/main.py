import tkinter as tk
from tkinter import messagebox
import requests
import datetime

URL_BACKEND = "http://127.0.0.1:5000"
tiempo_inicio = None
tiempo_receso = None
tiempo_total_receso = datetime.timedelta()


def enviar_datos():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    contrasena = entry_contrasena.get()

    if not nombre or not correo or not contrasena:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    datos = {"username": nombre, "correo": correo, "contrasena": contrasena}
    respuesta = requests.post(URL_BACKEND + "/registro", json=datos)

    if respuesta.status_code == 200:
        messagebox.showinfo("Éxito", respuesta.json()["mensaje"])
    else:
        messagebox.showerror("Error", respuesta.json()["mensaje"])


def enviar_login():
    global tiempo_inicio
    correo = entry_login_correo.get()
    contrasena = entry_login_contrasena.get()

    if not correo or not contrasena:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    datos = {"correo": correo, "contrasena": contrasena}
    respuesta = requests.post(URL_BACKEND + "/login", json=datos)

    if respuesta.status_code == 200:
        tiempo_inicio = datetime.datetime.now()
        messagebox.showinfo("Éxito", respuesta.json()["mensaje"])
        mostrar_pantalla_principal(correo)
    else:
        messagebox.showerror("Error", respuesta.json()["mensaje"])


def iniciar_receso():
    global tiempo_receso
    tiempo_receso = datetime.datetime.now()
    messagebox.showinfo("Receso", "Receso iniciado, el tiempo de trabajo se ha pausado.")


def finalizar_receso():
    global tiempo_receso, tiempo_total_receso
    if tiempo_receso:
        tiempo_total_receso += datetime.datetime.now() - tiempo_receso
        tiempo_receso = None
        messagebox.showinfo("Receso", "Receso finalizado, el tiempo de trabajo se reanuda.")


def cerrar_sesion(correo):
    global tiempo_inicio, tiempo_total_receso
    if tiempo_inicio:
        tiempo_salida = datetime.datetime.now()
        tiempo_trabajado = tiempo_salida - tiempo_inicio - tiempo_total_receso  # Excluye recesos
        
        datos = {
            "correo": correo,
            "entrada": tiempo_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "salida": tiempo_salida.strftime("%Y-%m-%d %H:%M:%S"),
            "horas_trabajadas": str(tiempo_trabajado)
        }

        requests.post(URL_BACKEND + "/guardar_tiempo", json=datos)
        tiempo_inicio, tiempo_total_receso = None, datetime.timedelta()
        messagebox.showinfo("Sesión cerrada", f"Tiempo trabajado registrado: {tiempo_trabajado}")

    mostrar_login()


def mostrar_pantalla_principal(correo):
    limpiar_pantalla()
    tk.Label(ventana, text="¡Bienvenido!", font=("Arial", 16)).pack(pady=20)

    tk.Button(ventana, text="Iniciar Receso", command=iniciar_receso).pack(pady=5)
    tk.Button(ventana, text="Finalizar Receso", command=finalizar_receso).pack(pady=5)
    tk.Button(ventana, text="Cerrar Sesión", command=lambda: cerrar_sesion(correo)).pack(pady=10)


def mostrar_login():
    limpiar_pantalla()
    tk.Label(ventana, text="Login", font=("Arial", 14)).pack(pady=10)

    global entry_login_correo, entry_login_contrasena
    tk.Label(ventana, text="Correo:").pack()
    entry_login_correo = tk.Entry(ventana)
    entry_login_correo.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entry_login_contrasena = tk.Entry(ventana, show="*")
    entry_login_contrasena.pack()

    tk.Button(ventana, text="Iniciar Sesión", command=enviar_login).pack(pady=10)


def mostrar_registro():
    limpiar_pantalla()
    tk.Label(ventana, text="Registro de Usuario", font=("Arial", 14)).pack(pady=10)

    global entry_nombre, entry_correo, entry_contrasena
    tk.Label(ventana, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Correo:").pack()
    entry_correo = tk.Entry(ventana)
    entry_correo.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    tk.Button(ventana, text="Registrar", command=enviar_datos).pack(pady=10)


def limpiar_pantalla():
    for widget in ventana.winfo_children():
        widget.destroy()
    crear_navbar() 


ventana = tk.Tk()
ventana.title("App de Registro de Horarios")
ventana.geometry("300x300")


def crear_navbar():
    navbar = tk.Frame(ventana, bg="gray")
    navbar.pack(fill="x")
    tk.Button(navbar, text="Login", command=mostrar_login).pack(side="left", padx=20, pady=5)
    tk.Button(navbar, text="Registro", command=mostrar_registro).pack(side="left", padx=20, pady=5)

crear_navbar()
mostrar_login()  

ventana.mainloop()