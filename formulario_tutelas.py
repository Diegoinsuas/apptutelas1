import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class registro_tutelas:
    def __init__(self, root):
        self.NIT = "900876345"
        self.db = "tutelas.db"

        self.root = root
        self.root.title("Formulario Unificado Tutelas")
        self.root.geometry("1500x1000")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_beneficiario = tk.Frame(self.notebook)
        self.notebook.add(self.tab_beneficiario, text="Beneficiario")

        self.tab_tutela = tk.Frame(self.notebook)
        self.notebook.add(self.tab_tutela, text="Tutela")

        self.tab_juridica = tk.Frame(self.notebook)
        self.notebook.add(self.tab_juridica, text="Jurídica")

        self.variables = {}
        self._crear_campos()

    def conectar(self):
        return sqlite3.connect(self.db)

    def validar_fecha(self, fecha_str):
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validar_campos_completos(self):
        from datetime import datetime

        campos_requeridos = list(self.variables.values())
        campos_invalidos = []

        for var in campos_requeridos:
            valor = var.get().strip()
            if valor == "":
                campos_invalidos.append(var)

        # Validar que las fechas sean correctas
        fechas = ["fecha_inicio", "fecha_fin", "fecha_nacimiento", "fecha_radicado"]
        for fecha in fechas:
            valor = self.variables[fecha].get().strip()
            try:
                datetime.strptime(valor, "%Y-%m-%d")
            except ValueError:
                campos_invalidos.append(self.variables[fecha])

        if campos_invalidos:
            messagebox.showerror("Error", "Hay campos vacíos o fechas inválidas. Por favor revisa todos los campos.")
            return False

        return True
    def obtener_consecutivo(self):
        """Obtiene el último consecutivo registrado en la base de datos y lo incrementa."""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(consecutivo) FROM caracterizacion_beneficiario")
        ultimo_consecutivo = cursor.fetchone()[0]
        conn.close()
        return (ultimo_consecutivo or 0) + 1

    def guardar_tutela(self):
        print("Guardando tutela...")
        if not self.validar_campos_completos():
            return
        consecutivo = self.obtener_consecutivo()
        v = self.variables

        conn = self.conectar()
        cursor = conn.cursor()

        try:
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
                v["fecha_inicio"].get(),
                v["fecha_fin"].get(),
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
                consecutivo,
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
            consecutivo += 1

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
                consecutivo,
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
            consecutivo += 1

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
                consecutivo,
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
            consecutivo += 1

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
                consecutivo,
                "NI",
                self.NIT,
                v["tipo_doc_beneficiario"].get(),
                v["num_doc_beneficiario"].get(),
                v["num_radicacion"].get(),
                v["cod_problema_juridico"].get(),
                v["cod_causa_tutela"].get(),
                v["indicador_actualizacion"].get()
                ))
            consecutivo += 1

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
                consecutivo,
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
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error:\n{e}")
        finally:
            conn.close()

    def _crear_campos(self):
        def add(label, varname, frame_destino, readonly=False, ayuda=None):
            row = frame_destino.grid_size()[1]  # obtiene el número actual de filas en el frame

            tk.Label(frame_destino, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=10, pady=2)

            self.variables[varname] = tk.StringVar()
            entry = tk.Entry(frame_destino, textvariable=self.variables[varname])
            if readonly:
                entry.configure(state="readonly")
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=2)

            if ayuda:
                tk.Label(frame_destino, text=ayuda, font=("Arial", 8), fg="gray").grid(
                    row=row + 1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5)
                )

        # ---- INFO FIJA DE LA ENTIDAD ----
        entidad_frame = tk.LabelFrame(self.tab_tutela, text="Información de la Entidad", padx=10, pady=5, font=("Arial", 10, "bold"))
        entidad_frame.pack(fill="x", padx=10, pady=(10, 10))

        tk.Label(entidad_frame, text="Tipo documento Entidad: NI", font=("Arial", 10)).pack(anchor="w")
        tk.Label(entidad_frame, text="Número documento Entidad: 900876345", font=("Arial", 10)).pack(anchor="w")
        tk.Label(entidad_frame, text="Codigo de habilitacion: 7300102831", font=("Arial", 10)).pack(anchor="w")

        # ---- AGRUPAR CAMPOS EN BLOQUES VISUALES ----
        beneficiario_frame = tk.LabelFrame(self.tab_beneficiario, text="Datos del Beneficiario", padx=10, pady=5, font=("Arial", 10, "bold"))
        beneficiario_frame.pack(fill="x", padx=10, pady=(10, 10))

        tutela_frame = tk.LabelFrame(self.tab_tutela, text="Datos Generales de la Tutela", padx=10, pady=5, font=("Arial", 10, "bold"))
        tutela_frame.pack(fill="x", padx=10, pady=(10, 10))

        juridico_frame = tk.LabelFrame(self.tab_juridica, text="Información Jurídica", padx=10, pady=5, font=("Arial", 10, "bold"))
        juridico_frame.pack(fill="x", padx=10, pady=(10, 10))

        # ---- CAMPOS ----
        add("Tipo documento Beneficiario", "tipo_doc_beneficiario", beneficiario_frame, False, "Ejemplo: CC, TI, CE")
        add("Número documento Beneficiario", "num_doc_beneficiario", beneficiario_frame, False, "Número de identificación del paciente")
        add("Nombre", "nombre", beneficiario_frame, False, "Nombres en mayúsculas")
        add("Apellido", "apellido", beneficiario_frame, False, "Apellidos en mayúsculas")
        add("País origen", "pais_origen", beneficiario_frame, False, "Código ISO 3166-1")
        add("Migrante", "migrante", beneficiario_frame, False, "1: Regular, 2: Irregular")
        add("Régimen de Afiliación", "regimen_afiliacion", beneficiario_frame, False, "C, S, E, P")
        add("Fecha nacimiento (YYYY-MM-DD)", "fecha_nacimiento", beneficiario_frame, False, "Formato: Año-Mes-Día")
        add("Sexo", "sexo", beneficiario_frame, False, "M: Masculino, F: Femenino")
        add("Gestación", "gestacion", beneficiario_frame, False, "1: Sí, 2: No")
        add("Etnia", "etnia", beneficiario_frame, False, "Código DANE")
        add("Población especial", "poblacion_especial", beneficiario_frame, False, "Ej: Desplazado")
        add("Tipo de afiliado", "tipo_afiliado", beneficiario_frame, False, "1: Cotizante, 2: Beneficiario")
        add("Municipio de residencia", "municipio_residencia", beneficiario_frame, False, "Código DIVIPOLA")
        
        add("Fecha inicio (YYYY-MM-DD)", "fecha_inicio", tutela_frame, False, "Inicio del periodo reportado")
        add("Fecha fin (YYYY-MM-DD)", "fecha_fin", tutela_frame, False, "Fin del periodo reportado")
        add("Municipio tutela", "municipio_tutela", tutela_frame, False, "Código DIVIPOLA")
        add("Número radicado", "num_radicacion", tutela_frame, False, "Número sin espacios")
        add("Fecha radicado (YYYY-MM-DD)", "fecha_radicado", tutela_frame, False, "Fecha exacta")
        add("Decisión 1ra instancia", "decision_primera", tutela_frame, False, "1: A favor, 2: En contra")
        add("Impugnación", "impugnacion", tutela_frame, False, "1: Sí, 2: No")
        add("Decisión 2da instancia", "decision_segunda", tutela_frame, False, "1: A favor, 2: En contra")
        add("Incidente desacato", "incidente_desacato", tutela_frame, False, "1: Sí, 2: No")

        add("Código problema jurídico", "cod_problema_juridico", juridico_frame, False, "Según lista oficial")
        add("Fuente financiación", "fuente_financiacion", juridico_frame, False, "UPC, Recobro, etc.")
        add("Causa demora", "causa_demora", juridico_frame, False, "Código de causa")
        add("Descripción demora", "desc_demora", juridico_frame, False, "Texto o código")
        add("Descripción negación", "desc_negacion", juridico_frame, False, "Texto o código")
        add("Diagnóstico principal (CIE10)", "dia_principal", juridico_frame, False, "CIE10 principal")
        add("Diagnóstico relacionado", "dia_relacionado", juridico_frame, False, "Opcional")
        add("Diagnóstico enfermedad huérfana", "dia_enf_huerfana", juridico_frame, False, "Código oficial")
        add("Código causa tutela", "cod_causa_tutela", juridico_frame, False, "Código estándar")
        add("Código pretensión", "cod_pretension", juridico_frame, False, "Código oficial")
        add("Indicador actualización", "indicador_actualizacion", juridico_frame, False, "I: Ingresar registro al sistema, A: Actualizar registro existente del mismo año")

        tk.Button(self.tab_juridica, text="Guardar Tutela", command=self.guardar_tutela, bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = registro_tutelas(root)
    root.mainloop()
