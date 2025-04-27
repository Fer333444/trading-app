import MetaTrader5 as mt5
import pyttsx3

# Reemplaza con tus datos reales
cuenta = {
    "login": 12345678,
    "password": "tu_password",
    "server": "NombreDelServidor"  # Ej: "MetaQuotes-Demo"
}

def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def probar_conexion():
    conectado = mt5.initialize(login=cuenta["login"], password=cuenta["password"], server=cuenta["server"])
    if not conectado:
        print("❌ No se pudo conectar a MetaTrader 5.")
        hablar("No se pudo conectar a MetaTrader 5.")
        return

    info = mt5.account_info()
    if info:
        print(f"✅ Conectado con éxito:")
        print(f"  Cuenta: {info.login}")
        print(f"  Nombre: {info.name}")
        print(f"  Broker: {info.server}")
        print(f"  Saldo: {info.balance}")
        print(f"  Equity: {info.equity}")

        hablar(f"Conectado a la cuenta {info.login}, a nombre de {info.name}.")
    else:
        print("⚠️ Conectado, pero no se pudo obtener la información de la cuenta.")
        hablar("Conectado, pero no se pudo obtener la información de la cuenta.")

    mt5.shutdown()

# Ejecutar
probar_conexion()
