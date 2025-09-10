import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear tabla de usuarios con columna 'rol'
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    clave TEXT NOT NULL,
    rol TEXT NOT NULL
)
''')

# Insertar usuarios con roles
cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES ('admin', '1234', 'admin')")
cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES ('usuario1', '5678', 'usuario')")

# Crear tabla de productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
''')

conn.commit()
conn.close()
