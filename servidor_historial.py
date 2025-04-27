from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de conexión MySQL
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mi_base_datos'  # Asegúrate que esta base exista
}

# Ruta principal: Login
@app.route('/')
def index():
    return render_template('login.html')

# Validar usuario y mostrar pantalla de bienvenida
@app.route('/validar', methods=['POST'])
def validar():
    usuario = request.form['usuario']
    clave = request.form['clave']

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    user = cursor.fetchone()
    conexion.close()

    if user and clave:
        session['usuario'] = usuario
        return render_template('bienvenida.html', usuario=usuario)
    return "Credenciales inválidas"

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

# Ruta del historial de operaciones
@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('historial.html', usuario=session['usuario'])

# Ruta para ver cuentas del usuario
@app.route('/cuentas')
def cuentas():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('cuentas.html', usuario=session['usuario'])

if __name__ == '__main__':
    app.run(debug=True)
