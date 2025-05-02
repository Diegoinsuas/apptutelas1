import sqlite3

def mostrar_usuarios(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Consultar todos los registros de la tabla usuarios
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    print("\nTabla: usuarios")
    for usuario in usuarios:
        print(usuario)

    conn.close()

# Llamar a la función para mostrar los usuarios
mostrar_usuarios("tutelas.db")