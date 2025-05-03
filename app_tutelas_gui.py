import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from formulario_tutelas import registro_tutelas
from ver_tutelas import VerTutelas
from gestion_usuarios import Login
import bcrypt, sys, os

# Función para conectarse a la base de datos
def conectar():
    db_path = resource_path("tutelas.db")
    return sqlite3.connect(db_path)

# Obtener la ruta base del ejecutable o del script
def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Función de login
def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT username, contraseña FROM usuarios WHERE usuario = ?", (usuario,))
    user = cursor.fetchone()
    conn.close()

    # Verificar si el usuario existe y la contraseña es correcta
    if user and bcrypt.checkpw(contraseña.encode('utf-8'), user[1].encode('utf-8') if isinstance(user[1], str) else user[1]):
        username = user[0]
        messagebox.showinfo("Login exitoso", f"Bienvenido, {username}!")
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
    tk.Button(menu, text="Gestión de Usuarios", width=30, command=abrir_gestion_usuarios).pack(pady=5)

# Registro de tutela
def formulario_tutela():
    ventana = tk.Toplevel()
    registro_tutelas(ventana)

# Ver tutelas registradas
def ver_tutelas_regis():
    ventana = tk.Toplevel()
    VerTutelas(ventana)

# Gestión de usuarios
def abrir_gestion_usuarios():
    """Abre la ventana de inicio de sesión para la gestión de usuarios."""
    root = tk.Toplevel()
    Login(root)

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
