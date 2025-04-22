import tkinter as tk
from tkinter import ttk
import sqlite3

class ver_tutela:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Tutelas registradas - Vista avanzada")
        self.ventana.geometry("1400x700")

        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True)

        self.pestañas = []
        self.trees = []
        self.scrollbars = []  # Para almacenar los scrollbars

        # Nombres de las pestañas como en el Excel
        nombres_pestañas = ["TIPO 1", "TIPO 2", "TIPO 3", "TIPO 4", "TIPO 5", "TIPO 6"]

        for nombre in nombres_pestañas:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=nombre)
            self.pestañas.append(frame)

            tree = ttk.Treeview(frame, show="headings")
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            self.trees.append(tree)

            # Agregar scrollbar horizontal
            scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            scrollbar.pack(fill='x', side='bottom')
            tree.configure(xscrollcommand=scrollbar.set)
            self.scrollbars.append(scrollbar)

        # Botón general para cargar datos
        tk.Button(self.ventana, text="Cargar Datos", command=self.cargar_todas_las_tutelas).pack(pady=10)

        self.cargar_todas_las_tutelas()

    def conectar(self):
        return sqlite3.connect('tutelas.db')

    def cargar_todas_las_tutelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        # Consultas SQL específicas por cada tipo
        consultas_por_tipo = [
            "SELECT tipo_registro1, tipo_doc_entidad, num_doc_entidad, fecha_inicio, fecha_fin, total_registros FROM registro_control",
            "SELECT tipo_registro2, consecutivo, tipo_doc_entidad, num_doc_entidad, tipo_doc_beneficiario, num_doc_beneficiario, nombre, apellido, pais_origen, migrante, regimen_afiliacion, cod_habilitacion, fecha_nacimiento, sexo, gestacion, etnia, poblacion_especial, tipo_afiliado, municipio_residencia, indicador_actualizacion FROM caracterizacion_beneficiario",
            "SELECT tipo_registro3, consecutivo, tipo_doc_entidad, num_doc_entidad, tipo_doc_beneficiario, num_doc_beneficiario, municipio_tutela, num_radicacion, fecha_radicado, decision_primera, impugnacion, decision_segunda, incidente_desacato, indicador_actualizacion FROM datos_generales",
            "SELECT tipo_registro4, consecutivo, tipo_doc_entidad, num_doc_entidad, tipo_doc_beneficiario, num_doc_beneficiario, num_radicacion, cod_problema_juridico, fuente_financiacion, causa_demora, desc_demora, desc_negacion, dia_principal, dia_relacionado, dia_enf_huerfana, indicador_actualizacion FROM problemas_juridicos",
            "SELECT tipo_registro5, consecutivo, tipo_doc_entidad, num_doc_entidad, tipo_doc_beneficiario, num_doc_beneficiario, num_radicacion, cod_problema_juridico, cod_causa_tutela, indicador_actualizacion FROM causas_problemas_juridicos",
            "SELECT tipo_registro6, consecutivo, tipo_doc_entidad, num_doc_entidad, tipo_doc_beneficiario, num_doc_beneficiario, num_radicacion, cod_problema_juridico, cod_causa_tutela, cod_pretension, indicador_actualizacion FROM pretensiones_tutelas"
        ]

        columnas_por_tipo = [
            ("tipo_registro1", "tipo_doc_entidad", "num_doc_entidad", "fecha_inicio", "fecha_fin", "total_registros"),
            ("tipo_registro2", "consecutivo", "tipo_doc_entidad", "num_doc_entidad", "tipo_doc_beneficiario", "num_doc_beneficiario", "nombre", "apellido", "pais_origen", "migrante", "regimen_afiliacion", "cod_habilitacion", "fecha_nacimiento", "sexo", "gestacion", "etnia", "poblacion_especial", "tipo_afiliado", "municipio_residencia", "indicador_actualizacion"),
            ("tipo_registro3", "consecutivo", "tipo_doc_entidad", "num_doc_entidad", "tipo_doc_beneficiario", "num_doc_beneficiario", "municipio_tutela", "num_radicacion", "fecha_radicado", "decision_primera", "impugnacion", "decision_segunda", "incidente_desacato", "indicador_actualizacion"),
            ("tipo_registro4", "consecutivo", "tipo_doc_entidad", "num_doc_entidad", "tipo_doc_beneficiario", "num_doc_beneficiario", "num_radicacion", "cod_problema_juridico", "fuente_financiacion", "causa_demora", "desc_demora", "desc_negacion", "dia_principal", "dia_relacionado", "dia_enf_huerfana", "indicador_actualizacion"),
            ("tipo_registro5", "consecutivo", "tipo_doc_entidad", "num_doc_entidad", "tipo_doc_beneficiario", "num_doc_beneficiario", "num_radicacion", "cod_problema_juridico", "cod_causa_tutela", "indicador_actualizacion"),
            ("tipo_registro6", "consecutivo", "tipo_doc_entidad", "num_doc_entidad", "tipo_doc_beneficiario", "num_doc_beneficiario", "num_radicacion", "cod_problema_juridico", "cod_causa_tutela", "cod_pretension", "indicador_actualizacion")
        ]

        for i, tree in enumerate(self.trees):
            # Ejecutar la consulta específica
            cursor.execute(consultas_por_tipo[i])
            registros = cursor.fetchall()

            # Limpiar árbol
            for item in tree.get_children():
                tree.delete(item)

            columnas = columnas_por_tipo[i]
            tree["columns"] = columnas

            for col in columnas:
                tree.heading(col, text=col.replace("_", " ").capitalize())
                tree.column(col, width=150, anchor="center")

            for fila in registros:
                tree.insert("", "end", values=fila)

        conn.close()
