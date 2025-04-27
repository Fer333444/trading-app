import MetaTrader5 as mt5

def conectar_mt5():
    # Verificamos si ya estamos conectados a MT5
    if mt5.account_info() is None:
        print("❌ No hay conexión activa con MetaTrader 5")
        return False
    print("✅ Conectado con MetaTrader 5")
    return True

def obtener_operaciones():
    operaciones = mt5.history_deals_get()
    if operaciones is None:
        print("❌ No se pudieron obtener operaciones")
        return []
    return operaciones

def cerrar_mt5():
    mt5.shutdown()
