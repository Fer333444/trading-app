
import speech_recognition as sr
import pyttsx3
import time

# Configura tus datos de cuenta MT5
cuenta = {
    "login": 510065036,
    "password": "8j!gSx?FL",
    "server": "FTMO-Server"  # Ej: "MetaQuotes-Demo"
}

def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def escuchar_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        hablar("Estoy escuchando. Da tu orden.")
        print("🎙️ Esperando comando...")
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="es-ES").lower()
        print(f"🗣️ Dijiste: {comando}")
        return comando
    except:
        hablar("No entendí el comando.")
        return None

def ejecutar_orden(comando):
    if not mt5.initialize(login=cuenta["login"], password=cuenta["password"], server=cuenta["server"]):
        print("❌ Error al conectar con MT5")
        hablar("No pude conectarme a MetaTrader.")
        return

    simbolos = ["eurusd", "gbpusd", "usdchf", "usdjpy"]
    for simbolo in simbolos:
        if simbolo in comando:
            accion = None
            if "compra" in comando:
                accion = 0  # Buy
            elif "venta" in comando or "vender" in comando:
                accion = 1  # Sell

            if accion is not None:
                orden = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": simbolo.upper(),
                    "volume": 0.1,
                    "type": mt5.ORDER_TYPE_BUY if accion == 0 else mt5.ORDER_TYPE_SELL,
                    "price": mt5.symbol_info_tick(simbolo.upper()).ask if accion == 0 else mt5.symbol_info_tick(simbolo.upper()).bid,
                    "sl": 0,
                    "tp": 0,
                    "deviation": 10,
                    "magic": 234000,
                    "comment": "Operación por voz",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }

                resultado = mt5.order_send(orden)
                if resultado.retcode == mt5.TRADE_RETCODE_DONE:
                    hablar(f"Orden de {'compra' if accion == 0 else 'venta'} ejecutada en {simbolo.upper()}.")
                else:
                    hablar(f"Error al ejecutar orden en {simbolo.upper()}. Código: {resultado.retcode}")
                break
    else:
        hablar("No reconocí el símbolo en tu orden.")

    mt5.shutdown()

# 🔧 NUEVA FUNCIÓN para verificar conexión con login y nombre del usuario
def verificar_conexion():
    conectado = mt5.initialize(login=cuenta["login"], password=cuenta["password"], server=cuenta["server"])
    if conectado:
        info = mt5.account_info()
        if info is not None:
            login = info.login
            nombre = info.name  # nombre del usuario
            hablar(f"Estoy conectado a MetaTrader 5. Cuenta número {login}, a nombre de {nombre}.")
        else:
            hablar("Estoy conectado, pero no pude obtener la información de la cuenta.")
        mt5.shutdown()
    else:
        hablar("No pude conectarme a MetaTrader.")

# 🔁 Ejecución principal
if __name__ == "__main__":
    while True:
        comando = escuchar_comando()
        if comando:
            if "estado" in comando or "conexión" in comando or "conectado" in comando:
                verificar_conexion()
            elif "salir" in comando:
                hablar("Saliendo del sistema.")
                break
            else:
                ejecutar_orden(comando)
        time.sleep(2)
