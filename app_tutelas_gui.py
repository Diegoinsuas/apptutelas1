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
    tk.Button(menu, text="Exportar tutelas a txt", width=30, command=exportar_tutelas_txt).pack(pady=5)
    tk.Button(menu, text="Reiniciar Base de Datos", width=30, command=reiniciar_base_datos).pack(pady=5)
    tk.Button(menu, text="Salir", width=30, command=menu.destroy).pack(pady=5)

# Registro de tutela
def formulario_tutela():
    ventana = tk.Toplevel()
    registro_tutelas(ventana)

# Ver tutelas registradas
def ver_tutelas_regis():
    ventana = tk.Toplevel()
    VerTutelas(ventana)

#Reiniciar base de datos
def reiniciar_base_datos():
    """Elimina todos los datos de las tablas relacionadas con las tutelas."""
    if not messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas borrar todos los datos de las tutelas? Esta acción no se puede deshacer."):
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Eliminar datos de las tablas relacionadas con las tutelas
        tablas = [
            "registro_control",
            "caracterizacion_beneficiario",
            "datos_generales",
            "problemas_juridicos",
            "causas_problemas_juridicos",
            "pretensiones_tutelas"
        ]
        for tabla in tablas:
            cursor.execute(f"DELETE FROM {tabla}")

        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Todos los datos de las tutelas han sido eliminados.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al reiniciar la base de datos:\n{e}")    

# Exportar a TXT
def exportar_tutelas_txt():
    semestre = simple_input_popup("Exportar a TXT", "Escribe el semestre (ej: 2024-1):")
    if not semestre or semestre.upper() not in ["2024-1", "2024-2", "2025-1", "2025-2"]:
        messagebox.showwarning("Formato inválido", "Usa el formato correcto, por ejemplo: 2024-2")
        return

    nit_entidad = "000900876345"
    if semestre.endswith("1"):
        fecha_corte = f"{semestre[:4]}0630"
    else:
        fecha_corte = f"{semestre[:4]}1231"

    nombre_archivo = f"IVC170TIDS{fecha_corte}NI{nit_entidad}.txt"

    conn = conectar()
    cursor = conn.cursor()

    # Consultas organizadas por tipo de registro
    consultas = {
        "1": "SELECT * FROM registro_control",
        "2": "SELECT * FROM caracterizacion_beneficiario",
        "3": "SELECT * FROM datos_generales",
        "4": "SELECT * FROM problemas_juridicos",
        "5": "SELECT * FROM causas_problemas_juridicos",
        "6": "SELECT * FROM pretensiones_tutelas"
    }

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for tipo, consulta in consultas.items():
                cursor.execute(consulta)
                registros = cursor.fetchall()

                for registro in registros:
                    # Convertir el registro a una línea de texto separada por "|"
                    linea = "|".join(map(str, registro))
                    archivo.write(f"{linea}\n")

        messagebox.showinfo("Exportación", f"Archivo '{nombre_archivo}' exportado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar los datos:\n{e}")
    finally:
        conn.close()
# Popup simple de entrada de texto
def simple_input_popup(titulo, mensaje):
    popup = tk.Toplevel()
    popup.title(titulo)
    popup.geometry("300x120")
    tk.Label(popup, text=mensaje).pack(pady=5)
    entrada = tk.Entry(popup)
    entrada.pack(pady=5)
    resultado = {"valor": None}

    def aceptar():
        resultado["valor"] = entrada.get()
        popup.destroy()

    tk.Button(popup, text="Aceptar", command=aceptar).pack()
    popup.wait_window()
    return resultado["valor"]

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
