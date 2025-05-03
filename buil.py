import os
import subprocess

# Comando para generar el ejecutable
command = [
    "pyinstaller",
    "--onefile",
    "--noconsole",
    "--add-data", "tutelas.db;.",
    "--add-data", ".env;.",
    "--add-data", "recursos/manual_2025.pdf;recursos",
    "--icon", "recursos/icono.ico",
    "main.py"
]

# Ejecutar el comando
subprocess.run(command, check=True)

print("✅ Ejecutable generado correctamente.")