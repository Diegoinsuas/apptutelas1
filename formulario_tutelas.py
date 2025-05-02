import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3, os
from datetime import datetime

class registro_tutelas:
    def __init__(self, root):
        self.NIT = "900876345"
        self.db = "tutelas.db"

        self.root = root
        self.root.title("Formulario Unificado Tutelas")

        # Dimensiones de la ventana
        ancho_ventana = 1000
        alto_ventana = 600

        # Actualizar la ventana para obtener dimensiones correctas
        self.root.update_idletasks()

        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Calcular la posición centrada
        pos_x = (ancho_pantalla // 2) - (ancho_ventana // 4)
        pos_y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Establecer la geometría centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

        # Crear las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_tutela = tk.Frame(self.notebook)
        self.notebook.add(self.tab_tutela, text="Tutela")

        self.tab_beneficiario = tk.Frame(self.notebook)
        self.notebook.add(self.tab_beneficiario, text="Beneficiario")

        self.tab_juridica = tk.Frame(self.notebook)
        self.notebook.add(self.tab_juridica, text="Jurídica")

        self.variables = {}
        self._crear_campos()

    def conectar(self):
        return sqlite3.connect(self.db)

    def validar_campos_completos(self):
        errores = []

        def validar(var, etiqueta, tipo="texto", obligatorio=True):
            valor = self.variables[var].get().strip()
            for tab in self.notebook.winfo_children():
                for frame in tab.winfo_children():
                    for widget in frame.winfo_children():
                        if isinstance(widget, tk.Entry) and widget.cget("textvariable") == str(self.variables[var]):
                            widget.configure(bg="white")
                            if obligatorio and not valor:
                                errores.append(f"El campo '{etiqueta}' es obligatorio.")
                                widget.configure(bg="#FFCCCC")
                            elif valor and tipo == "fecha":
                                try:
                                    datetime.strptime(valor, "%Y-%m-%d")
                                except ValueError:
                                    errores.append(f"El campo '{etiqueta}' tiene un formato de fecha inválido (AAAA-MM-DD).")
                                    widget.configure(bg="#FFCCCC")

        validar("municipio_tutela", "Municipio tutela")
        validar("migrante", "Migrante")
        validar("num_radicacion", "Número radicado")
        validar("fecha_radicado", "Fecha radicado", tipo="fecha")
        validar("decision_primera", "Decisión 1ra instancia")
        validar("impugnacion", "Impugnación")
        validar("incidente_desacato", "Incidente desacato")
        validar("tipo_doc_beneficiario", "Tipo documento Beneficiario")
        validar("num_doc_beneficiario", "Número documento Beneficiario")
        validar("nombre", "Nombre")
        validar("apellido", "Apellido")
        validar("pais_origen", "País origen")
        validar("regimen_afiliacion", "Régimen de Afiliación")
        validar("fecha_nacimiento", "Fecha nacimiento", tipo="fecha")
        validar("sexo", "Sexo")
        validar("tipo_afiliado", "Tipo de afiliado")
        validar("municipio_residencia", "Municipio de residencia")
        validar("cod_problema_juridico", "Código problema jurídico")
        validar("indicador_actualizacion", "Indicador actualización")
        validar("gestacion", "Gestación")
        validar("etnia", "Etnia")
        validar("poblacion_especial", "Población especial")
        validar("causa_demora", "Causa demora")
        validar("desc_demora", "Descripción demora")
        validar("desc_negacion", "Descripción negación")
        validar("dia_principal", "Diagnóstico principal")
        validar("cod_causa_tutela", "Código causa tutela")
        validar("cod_pretension", "Código pretensión")
        # Opcionales
        validar("decision_segunda", "Decisión 2da instancia", obligatorio=False)
        validar("fuente_financiacion", "Fuente financiación", obligatorio=False)
        validar("dia_relacionado", "Diagnóstico relacionado", obligatorio=False)
        validar("dia_enf_huerfana", "Diagnóstico enfermedad huérfana", obligatorio=False)


        if errores:
            messagebox.showerror("Errores en el formulario", "\n".join(errores))
            return False

        return True

    def guardar_tutela(self):
        print("Guardando tutela...")

        if not self.validar_campos_completos():
            return

        v = self.variables

        try:
            fecha_radicado = datetime.strptime(v["fecha_radicado"].get(), "%Y-%m-%d")
            año = fecha_radicado.year
            mes = fecha_radicado.month

            if 1 <= mes <= 6:  # Primer semestre
                fecha_inicio = f"{año}-01-01"
                fecha_fin = f"{año}-06-30"
            else:  # Segundo semestre
                fecha_inicio = f"{año}-07-01"
                fecha_fin = f"{año}-12-31"
        except ValueError:
            messagebox.showerror("Error", "La fecha de radicado no tiene un formato válido (AAAA-MM-DD).")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            # Verificar si ya existe un registro de control para las fechas dadas
            cursor.execute("""
            SELECT COUNT(*) FROM registro_control
            WHERE fecha_inicio = ? AND fecha_fin = ?
            """, (fecha_inicio, fecha_fin))
            existe_control = cursor.fetchone()[0]

            if existe_control == 0:
            # TIPO 1: REGISTRO CONTROL
                cursor.execute("""
                INSERT INTO registro_control (
                tipo_registro1,
                tipo_doc_entidad,
                num_doc_entidad,
                fecha_inicio,
                fecha_fin,
                total_registros)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "1",
                "NI",
                self.NIT,
                fecha_inicio,
                fecha_fin,
                "1"
                ))

            # TIPO 2: CARACTERIZACIÓN BENEFICIARIO
            cursor.execute("""
                INSERT INTO caracterizacion_beneficiario (
                tipo_registro2,
                consecutivo,
                tipo_doc_entidad,
                num_doc_entidad,
                tipo_doc_beneficiario,
                num_doc_beneficiario,
                nombre,
                apellido,
                pais_origen,
                migrante,
                regimen_afiliacion,
                cod_habilitacion,
                fecha_nacimiento,
                sexo,
                gestacion,
                etnia,
                poblacion_especial,
                tipo_afiliado,
                municipio_residencia,
                indicador_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "2",
                "1",
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["nombre"].get(),
                v["apellido"].get(),
                v["pais_origen"].get(),
                v["migrante"].get(),
                v["regimen_afiliacion"].get(),
                "7300102831",
                v["fecha_nacimiento"].get(),
                v["sexo"].get(),
                v["gestacion"].get(),
                v["etnia"].get(),
                v["poblacion_especial"].get(),
                v["tipo_afiliado"].get(),
                v["municipio_residencia"].get(),
                v["indicador_actualizacion"].get()
                ))

            # TIPO 3: DATOS GENERALES
            cursor.execute("""
                INSERT INTO datos_generales(
                tipo_registro3,
                consecutivo,
                tipo_doc_entidad,
                num_doc_entidad,
                tipo_doc_beneficiario,
                num_doc_beneficiario,
                municipio_tutela,
                num_radicacion,
                fecha_radicado,
                decision_primera,
                impugnacion,
                decision_segunda,
                incidente_desacato,
                indicador_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "3",
                "1",
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["municipio_tutela"].get(),
                v["num_radicacion"].get(),
                v["fecha_radicado"].get(),
                v["decision_primera"].get(),
                v["impugnacion"].get(),
                v["decision_segunda"].get(),
                v["incidente_desacato"].get(),
                v["indicador_actualizacion"].get()
                ))

            # TIPO 4: PROBLEMAS JURÍDICOS
            cursor.execute("""
                INSERT INTO problemas_juridicos(
                tipo_registro4,
                consecutivo,
                tipo_doc_entidad,
                num_doc_entidad,
                tipo_doc_beneficiario,
                num_doc_beneficiario,
                num_radicacion,
                cod_problema_juridico,
                fuente_financiacion,
                causa_demora,
                desc_demora,
                desc_negacion,
                dia_principal,
                dia_relacionado,
                dia_enf_huerfana,
                indicador_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "4",
                "1",
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["num_radicacion"].get(),
                v["cod_problema_juridico"].get(),
                v["fuente_financiacion"].get(),
                v["causa_demora"].get(),
                v["desc_demora"].get(),
                v["desc_negacion"].get(),
                v["dia_principal"].get(),
                v["dia_relacionado"].get(),
                v["dia_enf_huerfana"].get(),
                v["indicador_actualizacion"].get()
                ))

            # TIPO 5: CAUSAS DEL PROBLEMA JURÍDICO
            cursor.execute("""
                INSERT INTO causas_problemas_juridicos(
                tipo_registro5,
                consecutivo,
                tipo_doc_entidad,
                num_doc_entidad,
                tipo_doc_beneficiario,
                num_doc_beneficiario,
                num_radicacion,
                cod_problema_juridico,
                cod_causa_tutela,
                indicador_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "5",
                "1",
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["num_radicacion"].get(),
                v["cod_problema_juridico"].get(),
                v["cod_causa_tutela"].get(),
                v["indicador_actualizacion"].get()
                ))

            # TIPO 6: PRETENSIONES
            cursor.execute("""
                INSERT INTO pretensiones_tutelas(
                tipo_registro6,
                consecutivo,
                tipo_doc_entidad,
                num_doc_entidad,
                tipo_doc_beneficiario,
                num_doc_beneficiario,
                num_radicacion,
                cod_problema_juridico,
                cod_causa_tutela,
                cod_pretension,
                indicador_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "6",
                "1",
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["num_radicacion"].get(),
                v["cod_problema_juridico"].get(),
                v["cod_causa_tutela"].get(),
                v["cod_pretension"].get(),
                v["indicador_actualizacion"].get()
                ))

            conn.commit()
            messagebox.showinfo("✅ Registro exitoso", "Los datos se han guardado correctamente. ")
        
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error:\n{e}")
        finally:
            conn.close()

    def _crear_campos(self):
        def add(label, varname, frame_destino, readonly=False, ayuda=None):
            row = frame_destino.grid_size()[1]  # Obtiene el número actual de filas en el frame
    
            # Etiqueta del campo
            tk.Label(frame_destino, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=10, pady=2)
    
            # Campo de entrada
            self.variables[varname] = tk.StringVar()
            entry = tk.Entry(frame_destino, textvariable=self.variables[varname])
            if readonly:
                entry.configure(state="readonly")
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=2)
    
            # Ayuda opcional
            if ayuda:
                tk.Label(frame_destino, text=ayuda, font=("Arial", 8), fg="gray").grid(
                    row=row, column=2, sticky="w", padx=10, pady=2
                )
    
        # ---- INFO FIJA DE LA ENTIDAD ----
        entidad_frame = tk.LabelFrame(self.tab_tutela, text="Información de la Entidad", padx=10, pady=5, font=("Arial", 10, "bold"))
        entidad_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 10))
    
        tk.Label(entidad_frame, text="Tipo documento Entidad: NI", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=2)
        tk.Label(entidad_frame, text="Número documento Entidad: 900876345", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=2)
        tk.Label(entidad_frame, text="Código de habilitación: 7300102831", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=2)
        
        # ---- AGRUPAR CAMPOS EN BLOQUES VISUALES ----
        tutela_frame = tk.LabelFrame(self.tab_tutela, text="Datos Generales de la Tutela", padx=10, pady=5, font=("Arial", 10, "bold"))
        tutela_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(10, 10))
        
        beneficiario_frame = tk.LabelFrame(self.tab_beneficiario, text="Datos del Beneficiario", padx=10, pady=5, font=("Arial", 10, "bold"))
        beneficiario_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 10))

        juridico_frame = tk.LabelFrame(self.tab_juridica, text="Información Jurídica", padx=10, pady=5, font=("Arial", 10, "bold"))
        juridico_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 10))
        
        tk.Label(self.root, text="⚠ RECUERDE LLENAR TODO EN MAYÚSCULAS", font=("Arial", 15, "bold"), fg="red").pack(pady=20)

        # ---- CAMPOS ----
        add("Municipio tutela", "municipio_tutela", tutela_frame, False, "Código DIVIPOLA según manual")
        add("Número radicado", "num_radicacion", tutela_frame, False, "Número sin puntos, comas o espacios")
        add("Fecha radicado (AAAA-MM-DD)", "fecha_radicado", tutela_frame, False, "Fecha exacta de radicado")
        add("Decisión 1ra instancia", "decision_primera", tutela_frame, False, "Código de decisión según manual")
        add("Impugnación", "impugnacion", tutela_frame, False, "1: Sí, 2: No")
        add("Decisión 2da instancia", "decision_segunda", tutela_frame, False, "Código de decisión según manual")
        add("Incidente desacato", "incidente_desacato", tutela_frame, False, "1: Sí, 2: No")
        
        add("Tipo documento Beneficiario", "tipo_doc_beneficiario", beneficiario_frame, False, "CC, CD, CE, TI, PA, RC, si es otro consultar manual")
        add("Número documento Beneficiario", "num_doc_beneficiario", beneficiario_frame, False, "Número sin puntos, comas o espacios")
        add("Nombre", "nombre", beneficiario_frame, False, "Primer nombre en mayúscula sostenida")
        add("Apellido", "apellido", beneficiario_frame, False, "Primer apellido en mayúscula sostenida")
        add("País origen", "pais_origen", beneficiario_frame, False, "Código país según manual")
        add("Migrante", "migrante", beneficiario_frame, False, "1: Regular, 2: Irregular, 3: No es migrante, 4: Desconocido")
        add("Régimen de Afiliación", "regimen_afiliacion", beneficiario_frame, False, "C, E, N, O, P, S")
        add("Fecha nacimiento (AAAA-MM-DD)", "fecha_nacimiento", beneficiario_frame, False, "Formato: Año-Mes-Día")
        add("Sexo", "sexo", beneficiario_frame, False, "H: Hombre, M: Mujer, I: Indefinido")
        add("Gestación", "gestacion", beneficiario_frame, False, "1: Sí, 2: No")
        add("Etnia", "etnia", beneficiario_frame, False, "Código de etnia según manual")
        add("Población especial", "poblacion_especial", beneficiario_frame, False, "Código de población especial según manual")
        add("Tipo de afiliado", "tipo_afiliado", beneficiario_frame, False, "1: Cotizante, 2: Beneficiario, 3: Adicional, 4: No cotizante, 5: Titular")
        add("Municipio de residencia", "municipio_residencia", beneficiario_frame, False, "Código DIVIPOLA según manual")
    
        add("Código problema jurídico", "cod_problema_juridico", juridico_frame, False, "Código problema jurídico según manual")
        add("Fuente financiación", "fuente_financiacion", juridico_frame, False, "Código fuente financiación según manual")
        add("Causa demora", "causa_demora", juridico_frame, False, "Código de causa demora según manual")
        add("Descripción demora", "desc_demora", juridico_frame, False, "Código demora según manual")
        add("Descripción negación", "desc_negacion", juridico_frame, False, "Código negación según manual")
        add("Diagnóstico principal (CIE10)", "dia_principal", juridico_frame, False, "Código CIE10 según manual")
        add("Diagnóstico relacionado", "dia_relacionado", juridico_frame, False, "Código CIE10 según manual")
        add("Diagnóstico enfermedad huérfana", "dia_enf_huerfana", juridico_frame, False, "Código enfermedad según manual")
        add("Código causa tutela", "cod_causa_tutela", juridico_frame, False, "Código causa según manual")
        add("Código pretensión", "cod_pretension", juridico_frame, False, "Código pretensión según manual")
        add("Indicador actualización", "indicador_actualizacion", juridico_frame, False, "I: Insertar el registro al sistema A: Actualizar un registro reportado en el mismo año")
    
        # Botones
        tk.Button(self.tab_juridica, text="Guardar Tutela", command=self.guardar_tutela, bg="green", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=10)
        tk.Button(self.tab_tutela, text="Abrir Manual Guía", command=self.abrir_guia, bg="green", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=5)

    def abrir_guia(self):
        try:
            # Ruta del archivo de la guía
            guia_path = os.path.join(os.getcwd(), "recursos", "manual_2025.pdf")
            os.startfile(guia_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo de la guía.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = registro_tutelas(root)
    root.mainloop()
