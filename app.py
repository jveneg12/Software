from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# 🔐 Validación de usuario
def validar_usuario(usuario, clave):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, rol FROM usuarios WHERE usuario=? AND clave=?", (usuario, clave))
    resultado = cursor.fetchone()
    conn.close()
    return resultado  # Devuelve (usuario, rol)

# 🟢 Login + Registro en la misma vista
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'ingresar' in request.form:
            usuario = request.form['usuario']
            clave = request.form['clave']
            resultado = validar_usuario(usuario, clave)
            if resultado:
                session['usuario'] = resultado[0]
                session['rol'] = resultado[1]
                return redirect(url_for('menu') if session['rol'] == 'admin' else url_for('inicio'))
            else:
                return render_template('login.html', error='Credenciales incorrectas')

        elif 'registrar' in request.form:
            nuevo_usuario = request.form['nuevo_usuario']
            nueva_clave = request.form['nueva_clave']
            rol = 'usuario'  # Fijamos el rol como usuario

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (nuevo_usuario,))
            existente = cursor.fetchone()

            if existente:
                conn.close()
                return render_template('login.html', error_registro='El usuario ya existe.')

            cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)",
                           (nuevo_usuario, nueva_clave, rol))
            conn.commit()
            conn.close()

            # Iniciar sesión automáticamente y redirigir al inicio
            session['usuario'] = nuevo_usuario
            session['rol'] = rol
            return redirect(url_for('inicio'))

    return render_template('login.html')

# 🏠 Menú principal
@app.route('/menu')
def menu():
    if 'usuario' in session:
        return render_template('menu.html', usuario=session['usuario'])
    return redirect(url_for('login'))

# 🧱 CRUD de productos
@app.route('/productos')
def productos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    lista = cursor.fetchall()
    conn.close()
    return render_template('mantenedor.html', productos=lista)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    imagen = request.form['imagen']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)", (nombre, precio, imagen))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cursor.execute("UPDATE productos SET nombre=?, precio=? WHERE id=?", (nombre, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))
    else:
        cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
        producto = cursor.fetchone()
        conn.close()
        return render_template('editar_producto.html', producto=producto)

# 📊 Proceso: total del inventario
@app.route('/proceso')
def proceso():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(precio) FROM productos")
    total = cursor.fetchone()[0]
    conn.close()
    return render_template('proceso.html', total=total)

# 📋 Reporte: productos con precio > 0
@app.route('/reporte')
def reporte():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE precio > 0")
    productos = cursor.fetchall()
    conn.close()
    return render_template('reporte.html', productos=productos)

# 🛒 Carrito
def calcular_total_carrito(carrito):
    return sum(item['precio'] * item['cantidad'] for item in carrito)

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if 'usuario' in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if request.method == 'POST':
            filtro = request.form['filtro']
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + filtro + '%',))
        else:
            cursor.execute("SELECT * FROM productos")

        productos = cursor.fetchall()
        conn.close()

        if 'carrito' not in session:
            session['carrito'] = []

        total = calcular_total_carrito(session['carrito'])

        return render_template('inicio.html', usuario=session['usuario'], productos=productos, total=total)
    return redirect(url_for('login'))

@app.route('/comprar/<int:id>')
def comprar(id):
    if 'usuario' in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
        producto = cursor.fetchone()
        conn.close()

        if producto:
            carrito = session.get('carrito', [])
            encontrado = False

            for item in carrito:
                if item['id'] == producto[0]:
                    item['cantidad'] += 1
                    encontrado = True
                    break

            if not encontrado:
                carrito.append({
                    'id': producto[0],
                    'nombre': producto[1],
                    'precio': producto[2],
                    'imagen': producto[3],
                    'cantidad': 1
                })

            session['carrito'] = carrito

        return redirect(url_for('inicio'))
    return redirect(url_for('login'))

@app.route('/vaciar_carrito')
def vaciar_carrito():
    if 'usuario' in session:
        session['carrito'] = []
        return redirect(url_for('inicio'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 🚀 Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)