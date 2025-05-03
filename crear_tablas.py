import sqlite3
import bcrypt

conn = sqlite3.connect('tutelas.db')
cursor = conn.cursor()

# Tabla de Usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    username TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL
)
''')

# Crear un usuario por defecto
contraseña_admin = bcrypt.hashpw("101012".encode('utf-8'), bcrypt.gensalt())
cursor.execute("INSERT OR IGNORE INTO usuarios (username, usuario, contraseña) VALUES (?, ?, ?)", ("Administrador", "admin", contraseña_admin))

# Tipo 1: Registro de control
cursor.execute('''
CREATE TABLE IF NOT EXISTS registro_control (
    tipo_registro1 TEXT DEFAULT 1,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    total_registros INTEGER NOT NULL
)
''')

# Tipo 2: Caracterización del beneficiario
cursor.execute('''
CREATE TABLE IF NOT EXISTS caracterizacion_beneficiario (
    tipo_registro2 TEXT DEFAULT 2,
    consecutivo INTEGER NOT NULL,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    tipo_doc_beneficiario TEXT NOT NULL,
    num_doc_beneficiario TEXT NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    pais_origen TEXT NOT NULL,
    migrante TEXT NOT NULL,
    regimen_afiliacion TEXT NOT NULL,
    cod_habilitacion TEXT NOT NULL,
    fecha_nacimiento TEXT NOT NULL,
    sexo TEXT NOT NULL,
    gestacion TEXT NOT NULL,
    etnia TEXT NOT NULL,
    poblacion_especial TEXT NOT NULL,
    tipo_afiliado TEXT NOT NULL,
    municipio_residencia TEXT NOT NULL,
    indicador_actualizacion TEXT NOT NULL
    num_radicacion TEXT NOT NULL,
)
''')

# Tipo 3: Datos generales
cursor.execute('''
CREATE TABLE IF NOT EXISTS datos_generales (
    tipo_registro3 TEXT DEFAULT 3,
    consecutivo INTEGER NOT NULL,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    tipo_doc_beneficiario TEXT NOT NULL,
    num_doc_beneficiario TEXT NOT NULL,
    municipio_tutela TEXT NOT NULL,
    num_radicacion TEXT NOT NULL,
    fecha_radicado TEXT NOT NULL,
    decision_primera TEXT NOT NULL,
    impugnacion TEXT NOT NULL,
    decision_segunda TEXT NOT NULL,
    incidente_desacato TEXT NOT NULL,
    indicador_actualizacion TEXT NOT NULL
)
''')

# Tipo 4: Problemas jurídicos
cursor.execute('''
CREATE TABLE IF NOT EXISTS problemas_juridicos (
    tipo_registro4 TEXT DEFAULT 4,
    consecutivo INTEGER NOT NULL,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    tipo_doc_beneficiario TEXT NOT NULL,
    num_doc_beneficiario TEXT NOT NULL,
    num_radicacion TEXT NOT NULL,
    cod_problema_juridico TEXT NOT NULL,
    fuente_financiacion TEXT NOT NULL,
    causa_demora TEXT NOT NULL,
    desc_demora TEXT NOT NULL,
    desc_negacion TEXT NOT NULL,
    dia_principal TEXT NOT NULL,
    dia_relacionado TEXT NOT NULL,
    dia_enf_huerfana TEXT NOT NULL,
    indicador_actualizacion TEXT NOT NULL
)
''')

# Tipo 5: Causas asociadas a problemas jurídicos
cursor.execute('''
CREATE TABLE IF NOT EXISTS causas_problemas_juridicos (
    tipo_registro5 TEXT DEFAULT 5,
    consecutivo INTEGER NOT NULL,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    tipo_doc_beneficiario TEXT NOT NULL,
    num_doc_beneficiario TEXT NOT NULL,
    num_radicacion TEXT NOT NULL,
    cod_problema_juridico TEXT NOT NULL,
    cod_causa_tutela TEXT NOT NULL,
    indicador_actualizacion TEXT NOT NULL
)
''')

# Tipo 6: Pretensiones asociadas a las causas
cursor.execute('''
CREATE TABLE IF NOT EXISTS pretensiones_tutelas (
    tipo_registro6 TEXT DEFAULT 6,
    consecutivo INTEGER NOT NULL,
    tipo_doc_entidad TEXT NOT NULL,
    num_doc_entidad TEXT NOT NULL,
    tipo_doc_beneficiario TEXT NOT NULL,
    num_doc_beneficiario TEXT NOT NULL,
    num_radicacion TEXT NOT NULL,
    cod_problema_juridico TEXT NOT NULL,
    cod_causa_tutela TEXT NOT NULL,
    cod_pretension TEXT NOT NULL,
    indicador_actualizacion TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("✅ Base de datos y tablas creadas correctamente.")
