import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
from dotenv import load_dotenv
import os, sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

env_path = resource_path(".env")
load_dotenv(env_path)

class GestionUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")
        self.db_path = "tutelas.db"  # Cambia esto si necesitas una ruta dinámica

        # Campo para ingresar el nombre de usuario
        tk.Label(root, text="Nombre de Usuario:").pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        # Campo para ingresar el usuario
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack(pady=5)

        # Campo para ingresar la contraseña
        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_contraseña = tk.Entry(root, show="*")
        self.entry_contraseña.pack(pady=5)

        # Botones para agregar y eliminar usuarios
        tk.Button(root, text="Agregar Usuario", width=30,command=self.agregar_usuario).pack(pady=5)
        tk.Button(root, text="Eliminar Usuario", width=30, command=self.eliminar_usuario).pack(pady=5)
        tk.Button(root, text="Mostrar Usuarios", width=30, command=self.mostrar_usuarios).pack(pady=5)

    def conectar(self):
        """Conexión a la base de datos."""
        return sqlite3.connect(self.db_path)

    def agregar_usuario(self):
        """Agrega un usuario a la base de datos."""
        username = self.entry_username.get()
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        if not username or not contraseña:
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
            return

        # Encriptar la contraseña
        contraseña_encrypted = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())


        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (username, usuario, contraseña) VALUES (?, ?, ?)", (username, usuario, contraseña_encrypted))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{username}' agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar el usuario:\n{e}")
        finally:
            conn.close()

    def eliminar_usuario(self):
        """Elimina un usuario de la base de datos."""
        username = self.entry_username.get()

        # Lista de usuarios protegidos
        usuarios_protegidos = ["admin", "Administrador"]

        if username in usuarios_protegidos:
            messagebox.showwarning("Acción Restringida", f"No se puede eliminar el usuario protegido '{username}'.")
            return

        if not username:
            messagebox.showwarning("Campo Vacío", "Por favor, ingresa el nombre de usuario.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Usuario '{username}' eliminado correctamente.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró el usuario '{username}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar el usuario:\n{e}")
        finally:
            conn.close()

    def mostrar_usuarios(self):
        """Muestra todos los usuarios en la base de datos."""
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT username, usuario FROM usuarios")
            usuarios = cursor.fetchall()

            if usuarios:
                usuarios_str = "\n".join([f"Usuario: {u[0]}" for u in usuarios])
                messagebox.showinfo("Usuarios Registrados", usuarios_str)
            else:
                messagebox.showinfo("Usuarios Registrados", "No hay usuarios registrados.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al mostrar los usuarios:\n{e}")
        finally:
            conn.close()


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")

        # Recuperar la contraseña desde el archivo .env
        self.contraseña = os.getenv("LOGIN_PASSWORD", "default_password")

        tk.Label(root, text="Contraseña:", width=30).pack(pady=5)
        self.entry_contraseña = tk.Entry(root, show="*")
        self.entry_contraseña.pack(pady=5)

        tk.Button(root, text="Ingresar", command=self.verificar_contraseña).pack(pady=5)

    def verificar_contraseña(self):
        """Verifica si la contraseña ingresada es correcta."""
        if self.entry_contraseña.get() == self.contraseña:
            self.root.destroy()
            self.abrir_gestion_usuarios()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

    def abrir_gestion_usuarios(self):
        """Abre la interfaz de gestión de usuarios."""
        gestion_root = tk.Tk()
        app = GestionUsuarios(gestion_root)
        gestion_root.mainloop()


# Crear la ventana de inicio de sesión
if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()