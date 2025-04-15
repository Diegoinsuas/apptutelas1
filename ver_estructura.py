import sqlite3

def mostrar_tablas(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()

    for tabla in tablas:
        print(f"\nTabla: {tabla[0]}")
        cursor.execute(f"PRAGMA table_info({tabla[0]})")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"  {col[1]} ({col[2]})")

    conn.close()

mostrar_tablas("tutelas.db")
