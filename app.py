# Archivo completo app.py corregido y ordenado

import requests
from flask import Flask, render_template, redirect, url_for, request, session
from flask import send_file, jsonify
import mysql.connector
import bcrypt
import json
import os
from werkzeug.security import check_password_hash
import pandas as pd
from datetime import datetime

import jwt
from datetime import datetime, timedelta

SECRET_KEY_JWT = 'mi_clave_secreta_ultrasegura'

def generar_token(usuario):
    payload = {
        'usuario': usuario,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')
    return token

app = Flask(__name__)
app.secret_key = 'clave_segura_123'

def conectar_a_mt5():
    if mt5 is None:
        return False  # No intentar conectar si no hay MetaTrader5
    if not all(k in session for k in ['mt5_usuario', 'mt5_password', 'mt5_servidor']):
        return False
    if not mt5.initialize(
        login=int(session['mt5_usuario']),
        server=session['mt5_servidor'],
        password=session['mt5_password']
    ):
        print("❌ Error al conectar con MT5:", mt5.last_error())
        return False
    return True

import os

import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'tramway.proxy.rlwy.net'),
        user=os.getenv('DB_USER', 'flujo'),
        password=os.getenv('DB_PASSWORD', 'MiClave1234!'),
        database=os.getenv('DB_DATABASE', 'railway'),
        port=int(os.getenv('DB_PORT', 39408))
    )

# Funcion calcular lotaje Stinu

def calcular_lotaje_stinu(symbol, capital, riesgo_pct, stop_loss):
    valor_pip_fijo = {
        'EUR/USD': 10.00,
        'GBP/USD': 10.00,
        'AUD/USD': 10.00,
        'NZD/USD': 10.00,
        'USD/JPY': 7.00,
        'USD/CHF': 9.20,
        'USD/CAD': 7.23,
        'EUR/GBP': 8.60,
        'EUR/JPY': 7.13,
        'GBP/JPY': 8.70,
        'AUD/JPY': 6.98,
        'NZD/JPY': 6.70,
        'CAD/JPY': 6.80,
        'EUR/CAD': 7.30,
        'EUR/AUD': 6.20,
        'EUR/CHF': 9.10,
        'GBP/CHF': 9.00,
        'GBP/CAD': 7.50,
        'GBP/NZD': 6.10,
        'XAU/USD': 10.00
    }

    symbol = symbol.upper()
    valor_pip = valor_pip_fijo.get(symbol, 10.0)
    riesgo_dinero = round(capital * (riesgo_pct / 100), 2)
    lotaje = round(riesgo_dinero / (stop_loss * valor_pip), 2)
    return lotaje, riesgo_dinero

def calcular_porcentaje_operacion(operacion):
    try:
        ganancia = float(operacion.get("profit", 0))
        entrada = float(operacion.get("price", 0))
        if entrada != 0:
            porcentaje = (ganancia / entrada) * 100
            return round(porcentaje, 2)
    except:
        pass
    return 0.0

# Rutas Flask
	
import os
import json
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'clave_super_secreta_123'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Missing username or password", 400

        try:
            usuarios = {}
            if os.path.exists('usuarios.json'):
                with open('usuarios.json', 'r') as f:
                    usuarios = json.load(f)

            if username in usuarios:
                return "User already exists", 400

            hashed_password = generate_password_hash(password, method='scrypt')
            usuarios[username] = hashed_password

            with open('usuarios.json', 'w') as f:
                json.dump(usuarios, f, indent=4)

            session['pre_username'] = username  # ← se guarda para autocompletar
            return redirect(url_for('login'))

        except Exception as e:
            print(f"Error en /register: {e}")
            return "Internal error", 500

    return render_template('register.html')

@app.route('/editar_perfil')
def editar_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('editar_perfil.html', usuario=session['usuario'])

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html', usuario=session['usuario'])

@app.route('/bienvenida')
def bienvenida():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('bienvenida.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    try:
        with open('historial.json', 'r') as file:
            historial_data = json.load(file)
    except FileNotFoundError:
        historial_data = []

    historial_usuario = [op for op in historial_data if op['usuario'] == session['usuario']]
    return render_template('historial.html', historial=historial_usuario)

@app.route('/sistema_riesgo', methods=['GET', 'POST'])
def sistema_riesgo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    guardar_operaciones_mt5(usuario)

    # ✅ Manejar niveles_config.json vacío, dañado o inexistente
    try:
        if not os.path.exists("niveles_config.json") or os.path.getsize("niveles_config.json") == 0:
            raise ValueError("Archivo niveles_config.json inexistente o vacío.")

        with open("niveles_config.json", "r") as f:
            contenido = f.read().strip()

        if not contenido.startswith("{"):
            raise ValueError("Archivo niveles_config.json corrupto o mal formado.")

        config = json.loads(contenido)

    except Exception as e:
        config = {
            "nivel_actual": 1,
            "nivel_anterior": "-",
            "capital_referencia": 100000.0,
            "porcentajes": [0.0481, 0.0722, 0.1082, 0.1624, 0.2436, 0.3654]
        }
        with open("niveles_config.json", "w") as f:
            json.dump(config, f, indent=4)

    nivel = config["nivel_actual"]
    nivel_anterior = config.get("nivel_anterior", "-")
    capital_base = obtener_balance_mt5()
    porcentaje = config["porcentajes"][nivel - 1]

    ultimas_operaciones = []
    try:
        if os.path.exists("historial.json") and os.path.getsize("historial.json") > 0:
            with open("historial.json", "r") as file:
                historial = json.load(file)
            ops_usuario = [op for op in historial if op['usuario'] == usuario]
            ultimas_operaciones = [op for op in ops_usuario if float(op.get("profit", 0)) != 0 or op.get("accion")]
        else:
            ultimas_operaciones = []
    except Exception:
        ultimas_operaciones = []

    ult_op = ultimas_operaciones[-1] if ultimas_operaciones else None

    accion = request.form.get("accion") if request.method == 'POST' else None

    if accion == "ejecutar_mt5":
        if not conectar_a_mt5():
            return "❌ No se pudo conectar con MetaTrader 5."

        sl_raw = request.form.get("mt5_sl")
        tp_raw = request.form.get("mt5_tp")

        if sl_raw is None or tp_raw is None or sl_raw.strip() == "" or tp_raw.strip() == "":
            return redirect(url_for('sistema_riesgo'))

        try:
            symbol = request.form.get("mt5_symbol").upper()
            tipo = request.form.get("mt5_type").lower()
            volumen = float(request.form.get("mt5_volume"))
            sl = float(sl_raw)
            tp = float(tp_raw)

            resultado = enviar_orden_mt5(symbol, tipo, volumen, sl, tp)
            print(f"✅ Orden enviada: {resultado}")

        except Exception as e:
            print(f"❌ Error al ejecutar orden MT5: {e}")

    if accion == "manual":
        try:
            if os.path.exists("historial.json") and os.path.getsize("historial.json") > 0:
                with open("historial.json", "r") as file:
                    historial = json.load(file)
            else:
                historial = []
        except Exception:
            historial = []

        nueva_op = {
            "symbol": request.form.get("manual_symbol"),
            "type": int(request.form.get("manual_type")),
            "volume": float(request.form.get("manual_volume")),
            "price": 0,
            "profit": float(request.form.get("manual_profit")),
            "usuario": usuario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": "manual"
        }

        historial.append(nueva_op)
        with open("historial.json", "w") as file:
            json.dump(historial, file, indent=4)

    if accion in ["tp", "sl"]:
        config["nivel_anterior"] = config["nivel_actual"]
        if accion == "tp":
            config["nivel_actual"] = 1
        elif accion == "sl" and config["nivel_actual"] < 6:
            config["nivel_actual"] += 1

    if accion == "tp":
        try:
            nuevo_capital = float(request.form.get("capital_actual", capital_base))
            config["capital_referencia"] = nuevo_capital
        except ValueError:
            pass

    with open("niveles_config.json", "w") as file:
        json.dump(config, file, indent=4)

    capital = capital_base
    tabla = []
    for i in range(6):
        ganancia_real = 0
        if ult_op and i == nivel - 1:
            try:
                ganancia_real = float(ult_op.get("profit", 0))
            except:
                pass

        if i == nivel - 1:
            if config.get("accion_anterior") == "sl":
                nuevo_capital = capital
            else:
                nuevo_capital = capital + ganancia_real
        else:
            nuevo_capital = capital + capital * porcentaje

        fila = {
            'nivel': i + 1,
            'capital': capital,
            'nuevo_capital': nuevo_capital
        }

        capital = nuevo_capital
        tabla.append(fila)

    return render_template('sistema_riesgo.html', tabla=tabla, nivel_actual=nivel, nivel_anterior=nivel_anterior, porcentaje_actual=porcentaje, ult_op=ult_op)

@app.route('/lotaje_tiempo_real', methods=['GET', 'POST'])
def lotaje_tiempo_real():
    lotaje = None
    riesgo_dinero = None
    error = None
    capital = ''
    riesgo_pct = ''
    riesgo_monto = ''
    stop_loss = ''
    symbol = 'EUR/USD'
    tipo_riesgo = 'porcentaje'

    if request.method == 'POST':
        try:
            symbol = request.form['symbol']
            capital = float(request.form['capital'])
            stop_loss = float(request.form['stop_loss'])
            tipo_riesgo = request.form.get('tipo_riesgo')
            riesgo_dinero = 0

            # ✅ Validación general
            if not symbol or not stop_loss or not tipo_riesgo:
                raise ValueError("Completa todos los campos antes de calcular.")

            if tipo_riesgo == "porcentaje":
                riesgo_pct_str = request.form.get('riesgo_pct')
                if not riesgo_pct_str:
                    raise ValueError("Debes ingresar el porcentaje de riesgo.")
                riesgo_pct = float(riesgo_pct_str)
                riesgo_dinero = round(capital * (riesgo_pct / 100), 2)

            elif tipo_riesgo == "monto":
                riesgo_monto_str = request.form.get('riesgo_monto')
                if not riesgo_monto_str:
                    raise ValueError("Debes ingresar el monto de riesgo.")
                riesgo_monto = float(riesgo_monto_str)
                riesgo_dinero = riesgo_monto
            else:
                raise ValueError("Tipo de riesgo no válido.")

            # 🧠 Asumimos valor pip fijo 10.0, reemplaza si tienes más lógica
            valor_pip_fijo = {
                'EUR/USD': 10.00,
                'GBP/USD': 10.00,
                'AUD/USD': 10.00,
                'NZD/USD': 10.00,
                'USD/JPY': 7.00,
                'USD/CHF': 9.20,
                'USD/CAD': 7.23,
                'EUR/GBP': 8.60,
                'EUR/JPY': 7.13,
                'GBP/JPY': 8.70,
                'AUD/JPY': 6.98,
                'NZD/JPY': 6.70,
                'CAD/JPY': 6.80,
                'EUR/CAD': 7.30,
                'EUR/AUD': 6.20,
                'EUR/CHF': 9.10,
                'GBP/CHF': 9.00,
                'GBP/CAD': 7.50,
                'GBP/NZD': 6.10,
                'XAU/USD': 10.00
            }

            symbol = symbol.upper()
            valor_pip = valor_pip_fijo.get(symbol, 10.0)

            lotaje = round(riesgo_dinero / (stop_loss * valor_pip), 2)

        except ValueError as e:
            error = f"⚠️ {e}"
        except Exception as e:
            error = f"❌ Error inesperado: {e}"

    return render_template(
        'lotaje_tiempo_real.html',
        lotaje=lotaje,
        riesgo_dinero=riesgo_dinero,
        error=error,
        capital=capital,
        riesgo_pct=riesgo_pct,
        riesgo_monto=riesgo_monto,
        stop_loss=stop_loss,
        symbol=symbol,
        tipo_riesgo=tipo_riesgo
    )
@app.route('/exportar_excel')
def exportar_excel():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    try:
        with open('historial.json', 'r') as file:
            historial = json.load(file)
        datos_usuario = [op for op in historial if op['usuario'] == usuario]
    except FileNotFoundError:
        datos_usuario = []

    if not datos_usuario:
        return "⚠️ No hay datos para exportar."

    columnas_deseadas = []
    for op in datos_usuario:
        columnas_deseadas.append({
            'symbol': op.get('symbol'),
            'type': op.get('type'),
            'volume': float(op.get('volume', 0)),
            'profit': float(op.get('profit', 0))
        })

    df = pd.DataFrame(columnas_deseadas)
    nombre_archivo = f"historial_{usuario}.xlsx"
    df.to_excel(nombre_archivo, index=False, float_format="%.8f")
@app.route('/')
def inicio():
    return render_template('inicio.html')

    return send_file(nombre_archivo, as_attachment=True)
@app.route('/exportar_todo_excel')
def exportar_todo_excel():
    try:
        with open('historial.json', 'r') as file:
            historial = json.load(file)
    except FileNotFoundError:
        historial = []

    if not historial:
        return "⚠️ No hay operaciones registradas."

    df = pd.DataFrame(historial)
    archivo_excel = "historial_completo.xlsx"
    df.to_excel(archivo_excel, index=False)

    return send_file(archivo_excel, as_attachment=True)
@app.route('/cambiar_cuenta_mt5', methods=['GET', 'POST'])
def cambiar_cuenta_mt5():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        usuario = request.form['mt5_usuario']
        password = request.form['mt5_password']
        servidor = request.form['mt5_servidor']

        session['mt5_usuario'] = usuario
        session['mt5_password'] = password
        session['mt5_servidor'] = servidor

        return redirect(url_for('sistema_riesgo'))

    return render_template('cambiar_cuenta_mt5.html')
@app.route('/api/lotaje', methods=['POST'])
def api_lotaje():
    data = request.get_json()
    symbol = data.get('symbol')
    capital = data.get('capital')
    riesgo_pct = data.get('riesgo_pct')
    stop_loss = data.get('stop_loss')

    if not symbol or capital is None or riesgo_pct is None or stop_loss is None:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        lotaje, riesgo_dinero = calcular_lotaje_stinu(symbol, float(capital), float(riesgo_pct), float(stop_loss))
        return jsonify({
            "lotaje": lotaje,
            "riesgo_dinero": riesgo_dinero
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/historial', methods=['GET'])
def api_historial():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario = verificar_token(token)

    if not usuario:
        return jsonify({"error": "Token inválido o expirado"}), 401

    try:
        with open('historial.json', 'r') as file:
            historial = json.load(file)
        historial_usuario = [op for op in historial if op['usuario'] == usuario]
    except FileNotFoundError:
        historial_usuario = []

    return jsonify(historial_usuario), 200
@app.route('/api/sistema_riesgo', methods=['GET'])
def api_sistema_riesgo():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario = verificar_token(token)

    if not usuario:
        return jsonify({"error": "Token inválido o expirado"}), 401

    try:
        with open("niveles_config.json", "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {
            "nivel_actual": 1,
            "nivel_anterior": "-",
            "capital_referencia": 100000.0,
            "porcentajes": [0.0481, 0.0722, 0.1082, 0.1624, 0.2436, 0.3654]
        }

    capital_base = obtener_balance_mt5()
    nivel = config["nivel_actual"]
    nivel_anterior = config.get("nivel_anterior", "-")
    porcentaje = config["porcentajes"][nivel - 1]

    # Calcula la tabla de riesgo
    capital = capital_base
    tabla = []
    for i in range(6):
        nuevo_capital = capital + (capital * porcentaje)
        fila = {
            'nivel': i + 1,
            'capital': round(capital, 2),
            'nuevo_capital': round(nuevo_capital, 2)
        }
        capital = nuevo_capital
        tabla.append(fila)

    return jsonify({
        "nivel_actual": nivel,
        "nivel_anterior": nivel_anterior,
        "capital_base": round(capital_base, 2),
        "porcentaje": porcentaje,
        "tabla": tabla
    }), 200

@app.route('/api/logout', methods=['POST'])
def api_logout():
    # No hay forma de 'borrar' un JWT en el servidor porque es stateless
    # Pero podemos simplemente decir al cliente que borre su token
    return jsonify({"mensaje": "Sesión cerrada exitosamente. Elimina el token en el cliente."}), 200
@app.route('/api/operacion_manual', methods=['POST'])
def api_operacion_manual():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario = verificar_token(token)

    if not usuario:
        return jsonify({"error": "Token inválido o expirado"}), 401

    data = request.get_json()

    symbol = data.get('symbol')
    tipo = data.get('type')
    volumen = data.get('volume')
    profit = data.get('profit')

    if not symbol or tipo is None or volumen is None or profit is None:
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    nueva_op = {
        "symbol": symbol.upper(),
        "type": int(tipo),
        "volume": float(volumen),
        "price": 0,
        "profit": float(profit),
        "usuario": usuario,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": "manual"
    }

    try:
        if os.path.exists("historial.json") and os.path.getsize("historial.json") > 0:
            with open("historial.json", "r") as file:
                historial = json.load(file)
        else:
            historial = []
    except Exception:
        historial = []

    historial.append(nueva_op)

    with open("historial.json", "w") as file:
        json.dump(historial, file, indent=4)

    return jsonify({"mensaje": "Operación manual registrada exitosamente."}), 201
@app.route('/api/operar_mt5', methods=['POST'])
def api_operar_mt5():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario = verificar_token(token)

    if not usuario:
        return jsonify({"error": "Token inválido o expirado"}), 401

    if not conectar_a_mt5():
        return jsonify({"error": "No se pudo conectar con MetaTrader 5."}), 500

    data = request.get_json()

    symbol = data.get('symbol')
    tipo = data.get('type')  # "buy" o "sell"
    volumen = data.get('volume')
    sl = data.get('sl')
    tp = data.get('tp')

    if not symbol or not tipo or volumen is None or sl is None or tp is None:
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    try:
        resultado = enviar_orden_mt5(symbol.upper(), tipo.lower(), float(volumen), float(sl), float(tp))
        return jsonify({"mensaje": f"Orden enviada exitosamente: {resultado}"}), 201
    except Exception as e:
        return jsonify({"error": f"❌ Error al enviar orden MT5: {str(e)}"}), 500
@app.route('/api/perfil', methods=['GET'])
def api_perfil():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario = verificar_token(token)

    if not usuario:
        return jsonify({"error": "Token inválido o expirado"}), 401

    # Para este ejemplo, simplemente devolvemos el nombre del usuario
    return jsonify({
        "usuario": usuario
    }), 200
@app.route('/api/editar_perfil', methods=['POST'])
def api_editar_perfil():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    usuario_actual = verificar_token(token)

    if not usuario_actual:
        return jsonify({"error": "Token inválido o expirado"}), 401

    data = request.get_json()
    nuevo_usuario = data.get('nuevo_usuario')
    nueva_password = data.get('nueva_password')

    if not nuevo_usuario and not nueva_password:
        return jsonify({"error": "Debes enviar al menos un campo para actualizar."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    if nuevo_usuario:
        cursor.execute("UPDATE usuarios SET usuario = %s WHERE usuario = %s", (nuevo_usuario, usuario_actual))
        session['usuario'] = nuevo_usuario  # Actualizar sesión si cambió el nombre

    if nueva_password:
        hashed_password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE usuarios SET clave_hash = %s WHERE usuario = %s", (hashed_password.decode('utf-8'), nuevo_usuario or usuario_actual))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Perfil actualizado correctamente."}), 200
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"error": "Usuario y password requeridos."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT clave_hash FROM usuarios WHERE usuario = %s", (usuario,))
    stored_hash = cursor.fetchone()
    cursor.close()
    conn.close()

    if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash[0].encode('utf-8')):
        # ✅ Generamos token JWT
        payload = {
            'usuario': usuario,
            'exp': datetime.utcnow() + timedelta(hours=12)  # Token dura 12 horas
        }
        token = jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')

        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"error": "Usuario y password son requeridos."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario,))
    existente = cursor.fetchone()

    if existente:
        cursor.close()
        conn.close()
        return jsonify({"error": "Usuario ya existe."}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO usuarios (usuario, clave_hash) VALUES (%s, %s)", (usuario, hashed_password.decode('utf-8')))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado exitosamente."}), 201
@app.errorhandler(500)
def error_500(e):
    return f"Error interno general: {e}", 500
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            with open('usuarios.json', 'r') as f:
                usuarios = json.load(f)

            if username not in usuarios:
                return "Usuario no encontrado", 404

            hashed_password = usuarios[username]
            if check_password_hash(hashed_password, password):
                session['usuario'] = username
                return redirect(url_for('bienvenida'))
            else:
                return "Contraseña incorrecta", 401

        except Exception as e:
            return f"Error interno: {e}", 500

    return render_template('login.html', pre_username=session.get('pre_username', ''))



if __name__ == '__main__':
    import os
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
