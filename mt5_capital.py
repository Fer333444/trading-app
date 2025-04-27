

def conectar_mt5():
    if mt5.account_info() is None:
        print("❌ No hay conexión activa con MetaTrader 5")
        return False
    print("✅ Ya conectado con MetaTrader 5")
    return True

def obtener_operaciones():
    operaciones = mt5.history_deals_get()
    if operaciones is None:
        print("❌ No se pudieron obtener operaciones")
        return []
    return operaciones

def cerrar_mt5():
    if mt5.account_info() is not None:
        mt5.shutdown()

# ✅ NUEVA función segura para obtener el balance
def obtener_balance_mt5():
    if mt5.account_info() is None:
        print("❌ No estás conectado a MT5")
        return 0.0
    return mt5.account_info().balance
