import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from formulario_tutelas import registro_tutelas
from ver_tutelas import VerTutelas



# Función para conectarse a la base de datos
def conectar():
    return sqlite3.connect('tutelas.db')

# Función de login
def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
    user = cursor.fetchone()
    conn.close()

    if user:
        nombre_admin = user[0]
        messagebox.showinfo("Login exitoso", f"Bienvenido, {nombre_admin}!")
        ventana_login.destroy()
        mostrar_menu_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Menú principal
def mostrar_menu_principal():
    menu = tk.Tk()
    menu.title("Menú Principal")

    tk.Label(menu, text="Menú Principal", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(menu, text="Registrar nueva tutela", width=30, command=formulario_tutela).pack(pady=5)
    tk.Button(menu, text="Ver tutelas registradas", width=30, command=ver_tutelas_regis).pack(pady=5)
    tk.Button(menu, text="Salir", width=30, command=menu.destroy).pack(pady=5)

# Registro de tutela
def formulario_tutela():
    ventana = tk.Toplevel()
    registro_tutelas(ventana)

# Ver tutelas registradas
def ver_tutelas_regis():
    ventana = tk.Toplevel()
    VerTutelas(ventana)

# Ventana de Login
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("300x200")

tk.Label(ventana_login, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.pack(pady=5)

tk.Button(ventana_login, text="Ingresar", command=verificar_login).pack(pady=10)

ventana_login.mainloop()
