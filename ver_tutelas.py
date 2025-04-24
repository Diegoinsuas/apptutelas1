import tkinter as tk
from tkinter import ttk
import sqlite3

class VerTutelas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Tutelas registradas")
        self.ventana.geometry("1400x700")

        # Frame contenedor
        frame = tk.Frame(self.ventana)
        frame.pack(fill='both', expand=True)

        # Configurar Treeview con una sola columna
        columnas = ("datos",)
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings")
        self.tree.heading("datos", text="Datos")
        self.tree.column("datos", width=1350, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scroll horizontal
        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(fill='x', side='bottom')
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        # Botón para cargar datos
        tk.Button(self.ventana, text="Cargar Datos", command=self.cargar_datos).pack(pady=10)

    def conectar(self):
        """Conexión a la base de datos."""
        try:
            return sqlite3.connect('tutelas.db')
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def cargar_datos(self):
        """Carga los datos de las tutelas en la tabla."""
        conn = self.conectar()
        if not conn:
            return
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

        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar registros en formato plano
        for consulta in consultas.values():
            cursor.execute(consulta)
            registros = cursor.fetchall()

            for registro in registros:
                # Convertir el registro a una lista de cadenas separadas por "|"
                fila = "|".join(map(str, registro))
                self.tree.insert("", "end", values=(fila,))

        conn.close()

# Ejecutar ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VerTutelas(root)
    root.mainloop()