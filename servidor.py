from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'clave_secreta_segura'

USUARIOS_FILE = 'usuarios.json'
HISTORIAL_FILE = 'historial.json'

# ---------------- FUNCIONES ---------------- #
def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, 'r') as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=4)

# ---------------- RUTAS WEB ---------------- #
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        usuarios = cargar_usuarios()
        if usuario in usuarios:
            return "Usuario ya existe"
        usuarios[usuario] = generate_password_hash(clave)
        guardar_usuarios(usuarios)
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/validar', methods=['POST'])
def validar():
    usuario = request.form['usuario']
    clave = request.form['clave']
    usuarios = cargar_usuarios()
    if usuario in usuarios and check_password_hash(usuarios[usuario], clave):
        session['usuario'] = usuario
        return redirect(url_for('historial'))
    return "Credenciales inválidas"

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    with open(HISTORIAL_FILE, 'r') as f:
        operaciones = json.load(f)
    return render_template('index.html', operaciones=operaciones)

@app.route('/api/historial')
def api_historial():
    with open(HISTORIAL_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
