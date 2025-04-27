import MetaTrader5 as mt5
import requests

# 🔹 Configuración de Telegram
TOKEN_TELEGRAM = "8184570217:AAHzMMwkGPxmU22qQZA7YncMzGtbGRRAX04"  # Reemplaza con tu token real
CHAT_ID = "6005216541"  # Reemplaza con tu ID de usuario en Telegram

def enviar_mensaje_telegram(mensaje):
    """ Función para enviar mensajes a Telegram """
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    return response.json()

# 🔧 Ejecutar solo si es script directo
if __name__ == "__main__":
    # 🔹 Conexión con MetaTrader 5
    if not mt5.initialize():
        enviar_mensaje_telegram("❌ *Error al conectar con MT5*")
        quit()

    # 🔹 Lista de símbolos a monitorear
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF"]

    # 🔹 Revisar el estado del mercado
    mensaje = "📡 *Señales de Trading - MT5:*\n"
    for symbol in symbols:
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            mensaje += f"✅ *{symbol}* -> Bid: {tick.bid}, Ask: {tick.ask}\n"
        else:
            mensaje += f"⚠ *{symbol}* no tiene datos disponibles en MT5\n"

    # 🔹 Enviar la señal a Telegram
    enviar_mensaje_telegram(mensaje)

    # 🔹 Cerrar conexión con MT5
    mt5.shutdown()
