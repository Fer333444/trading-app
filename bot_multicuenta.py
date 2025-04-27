import MetaTrader5 as mt5
import json
import os
from datetime import datetime

def conectar_mt5(login, password, server):
    if mt5.initialize(login=login, password=password, server=server):
        print(f"✅ Conectado a MT5 con login {login}")
        return True
    else:
        print("❌ Error al conectar a MT5:", mt5.last_error())
        return False

def guardar_operacion(usuario_id, operacion):
    json_path = f"historiales/{usuario_id}.json"
    if not os.path.exists("historiales"):
        os.makedirs("historiales")
    try:
        with open(json_path, "r") as file:
            historial = json.load(file)
    except FileNotFoundError:
        historial = []

    historial.append(operacion)

    with open(json_path, "w") as file:
        json.dump(historial, file, indent=4)

    print(f"✅ Historial guardado para usuario {usuario_id}")

# 🔧 Ejecutar solo como script directo
if __name__ == "__main__":
    login = 12345678
    password = "tu_contraseña"
    server = "MetaQuotes-Demo"
    usuario_id = str(login)

    if conectar_mt5(login, password, server):
        operacion = {
            "ticket": 987654,
            "par": "EURUSD",
            "tipo": "Buy",
            "lotes": 0.10,
            "precio_entrada": 1.0842,
            "precio_cierre": 1.0872,
            "ganancia": 30.0,
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        guardar_operacion(usuario_id, operacion)
        mt5.shutdown()
