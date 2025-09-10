import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Agregar columna 'imagen' si no existe
try:
    cursor.execute("ALTER TABLE productos ADD COLUMN imagen TEXT")
    print("Columna 'imagen' agregada correctamente.")
except sqlite3.OperationalError:
    print("La columna 'imagen' ya existe o hubo un error.")

conn.commit()
conn.close()