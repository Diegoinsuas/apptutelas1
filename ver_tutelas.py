import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import shutil

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

        # Botones en la misma fila
        boton_frame = tk.Frame(self.ventana)
        boton_frame.pack(pady=10)

        tk.Button(boton_frame, text="Ver Tutelas", width=20, command=self.cargar_datos).pack(side="left", padx=10)
        tk.Button(boton_frame, text="Actualizar Consecutivos", width=30, command=self.actualizar_consecutivos).pack(side="left", padx=10)
        tk.Button(boton_frame, text="Exportar tutelas a txt", width=30, command=self.exportar_tutelas_txt).pack(side="left", padx=10)
        tk.Button(boton_frame, text="Reiniciar Base de Datos", width=30, command=self.reiniciar_base_datos).pack(side="left", padx=10)
        tk.Button(boton_frame, text="Respaldar Base de Datos", width=30, command=self.respaldar_base_datos).pack(side="left", padx=10)
        
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

    def actualizar_consecutivos(self):
        """Recalcula y actualiza los consecutivos dinámicamente en la base de datos, y actualiza el total de registros."""
        conn = self.conectar()
        if not conn:
            return
        cursor = conn.cursor()

        try:
            # Obtener el total de tutelas existentes
            cursor.execute("SELECT COUNT(*) FROM caracterizacion_beneficiario")
            total_tutelas = cursor.fetchone()[0]

            if total_tutelas == 0:
                tk.messagebox.showinfo("Información", "No hay tutelas registradas para actualizar.")
                return

            # Recalcular y actualizar consecutivos dinámicos
            for index in range(1, total_tutelas + 1):
                consecutivo_tipo2 = index
                consecutivo_tipo3 = index + total_tutelas
                consecutivo_tipo4 = index + total_tutelas * 2
                consecutivo_tipo5 = index + total_tutelas * 3
                consecutivo_tipo6 = index + total_tutelas * 4

                # Actualizar consecutivos en las tablas correspondientes
                cursor.execute("UPDATE caracterizacion_beneficiario SET consecutivo = ? WHERE rowid = ?", (consecutivo_tipo2, index))
                cursor.execute("UPDATE datos_generales SET consecutivo = ? WHERE rowid = ?", (consecutivo_tipo3, index))
                cursor.execute("UPDATE problemas_juridicos SET consecutivo = ? WHERE rowid = ?", (consecutivo_tipo4, index))
                cursor.execute("UPDATE causas_problemas_juridicos SET consecutivo = ? WHERE rowid = ?", (consecutivo_tipo5, index))
                cursor.execute("UPDATE pretensiones_tutelas SET consecutivo = ? WHERE rowid = ?", (consecutivo_tipo6, index))

            # Actualizar el total de registros en la tabla registro_control
            cursor.execute("UPDATE registro_control SET total_registros = ? WHERE rowid = 1", (consecutivo_tipo6,))

            conn.commit()
            tk.messagebox.showinfo("Éxito", "Los consecutivos y el total de registros se han actualizado correctamente.")

            # Refrescar la vista
            self.cargar_datos()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Ocurrió un error al actualizar los consecutivos:\n{e}")
        finally:
            conn.close()

    def exportar_tutelas_txt(self):
        """Exporta los datos de las tutelas a un archivo TXT sin pedir semestre."""
        nit_entidad = "000900876345"

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            # Obtener la fecha_fin más reciente de la tabla registro_control
            cursor.execute("SELECT MAX(fecha_fin) FROM registro_control")
            fecha_corte = cursor.fetchone()[0]  # Formato: AAAA-MM-DD
            if not fecha_corte:
                tk.messagebox.showwarning("Sin registros", "No hay tutelas registradas para exportar.")
                return

            fecha_corte_txt = fecha_corte.replace("-", "")  # Ej: 2025-06-30 -> 20250630
            nombre_archivo = f"IVC170TIDS{fecha_corte_txt}NI{nit_entidad}.txt"

            # Seleccionar la ubicación y el nombre del archivo
            archivo_destino = filedialog.asksaveasfilename(
                title="Guardar archivo TXT",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")],
                initialfile=nombre_archivo
            )

            if not archivo_destino:
                return  # El usuario canceló la operación

            # Consultas organizadas por tipo de registro
            consultas = {
                "1": "SELECT * FROM registro_control",
                "2": "SELECT * FROM caracterizacion_beneficiario",
                "3": "SELECT * FROM datos_generales",
                "4": "SELECT * FROM problemas_juridicos",
                "5": "SELECT * FROM causas_problemas_juridicos",
                "6": "SELECT * FROM pretensiones_tutelas"
            }

            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                for tipo, consulta in consultas.items():
                    cursor.execute(consulta)
                    registros = cursor.fetchall()
                    for registro in registros:
                        linea = "|".join(map(str, registro))
                        archivo.write(f"{linea}\n")

            tk.messagebox.showinfo("✅ Exportación completada", f"Archivo exportado como:\n{nombre_archivo}")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Ocurrió un error al exportar:\n{e}")
        finally:
            conn.close()

    def simple_input_popup(self, titulo, mensaje):
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
    
    #Reiniciar base de datos
    def reiniciar_base_datos(self):
        """Elimina todos los datos de las tablas relacionadas con las tutelas."""
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas borrar todos los datos de las tutelas? Esta acción no se puede deshacer."):
            return

        try:    
            conn = self.conectar()
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
            
    def respaldar_base_datos(self):
        """Crea un respaldo de la base de datos SQLite."""
        try:
            # Seleccionar la ubicación del respaldo
            archivo_respaldo = filedialog.asksaveasfilename(
                title="Guardar Respaldo",
                defaultextension=".db",
                filetypes=[("Base de Datos SQLite", "*.db")],
                initialfile="respaldo_tutelas.db"
            )

            if not archivo_respaldo:
                return  # El usuario canceló la operación

            # Copiar el archivo de la base de datos al destino seleccionado
            shutil.copy("tutelas.db", archivo_respaldo)

            # Confirmar el respaldo
            messagebox.showinfo("Respaldo Exitoso", f"El respaldo se guardó correctamente en:\n{archivo_respaldo}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el respaldo:\n{e}")

# Ejecutar ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VerTutelas(root)
    root.mainloop()