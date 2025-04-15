import sqlite3
import getpass
import pandas as pd

# Función para conectarse a la base de datos
def conectar():
    return sqlite3.connect('tutelas.db')

# Función para verificar login
def login():
    conn = conectar()
    cursor = conn.cursor()

    print("🔐 INICIO DE SESIÓN")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ") #getpass.getpass se usa para ocultar la contraseña a cambio de imput

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\n👋 Bienvenido, {user[1]}!\n")
        return True
    else:
        print("❌ Usuario o contraseña incorrectos.\n")
        return False

# Función para registrar nueva tutela
def registrar_tutela():
    print("\n📝 REGISTRO DE TUTELA")

    entidad = input("Entidad reportadora: ")
    tipo_id = input("Tipo de identificación: ")
    num_id = input("Número de identificación: ")
    nombre = input("Nombre del beneficiario: ")
    radicado = input("Número de radicado: ")
    fecha_fallo = input("Fecha del fallo (YYYY-MM-DD): ")
    tipo_fallo = input("Tipo de fallo: ")
    servicios = input("Servicios reclamados: ")
    estado = input("Estado: ")
    obs = input("Observaciones: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tutelas (
            entidad_reportadora, tipo_identificacion, numero_identificacion,
            nombre_beneficiario, numero_radicado, fecha_fallo, tipo_fallo,
            servicios_reclamados, estado, observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (entidad, tipo_id, num_id, nombre, radicado, fecha_fallo, tipo_fallo, servicios, estado, obs))

    conn.commit()
    conn.close()
    print("✅ Tutela registrada con éxito.\n")

# Función para mostrar todas las tutelas
def ver_tutelas():
    print("\n📋 TUTELAS REGISTRADAS")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tutelas")
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        print("⚠️ No hay tutelas registradas.\n")
    else:
        for r in registros:
            print(f"ID: {r[0]}, Beneficiario: {r[4]}, Radicado: {r[5]}, Fecha: {r[6]}, Fallo: {r[7]}")
        print("")

#Exportar tutelas a excel

def exportar_tutelas_excel():
    print("\n📤 EXPORTANDO TUTELAS A EXCEL...")

    semestre = input("Escribe el semestre (ej: 2024-I o 2024-II): ").strip().upper()
    if semestre not in ["2024-I", "2024-II", "2025-I", "2025-II"]:
        print("⚠️ Semestre inválido. Usa el formato 2024-I o 2024-II.\n")
        return

    # NIT fijo
    nit_entidad = "000900876345"

    # Determinar fecha de corte según semestre
    if semestre.endswith("I"):
        fecha_corte = f"{semestre[:4]}0630"  # 30 de junio
    else:
        fecha_corte = f"{semestre[:4]}1231"  # 31 de diciembre

    nombre_archivo = f"IVC170TIDS{fecha_corte}NI{nit_entidad}.xlsx"

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tutelas")
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()

    if not registros:
        print("⚠️ No hay tutelas para exportar.\n")
        return

    df = pd.DataFrame(registros, columns=columnas)
    df.to_excel(nombre_archivo, index=False)

    print(f"✅ Archivo '{nombre_archivo}' generado con éxito.\n")


# Menú principal
def menu():
    while True:
        print("📌 MENÚ PRINCIPAL")
        print("1. Registrar nueva tutela")
        print("2. Ver tutelas registradas")
        print("3. Exportar tutelas a Excel")
        print("4. Salir")

        opcion = input("Elige una opción: ")
        if opcion == '1':
            registrar_tutela()
        elif opcion == '2':
            ver_tutelas()
        elif opcion == '3':
            exportar_tutelas_excel()
        elif opcion == '4':
            print("👋 Hasta pronto.")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.\n")



# Inicio del programa
if __name__ == "__main__":
    if login():
        menu()
