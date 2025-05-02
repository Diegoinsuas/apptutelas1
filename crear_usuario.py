import sqlite3

def crear_usuario():
    username = input("Nombre completo: ")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    conn = sqlite3.connect("tutelas.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO usuarios (username, usuario, contraseña)
            VALUES (?, ?, ?)
        ''', (username, usuario, contraseña))

        conn.commit()
        print("✅ Usuario creado con éxito.")
    except sqlite3.IntegrityError:
        print("❌ El nombre de usuario ya existe.")
    finally:
        conn.close()

if __name__ == "__main__":
    crear_usuario()
