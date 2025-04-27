import MetaTrader5 as mt5
from datetime import datetime

def revisar_operaciones():
    # Inicializar conexión con MT5
    if not mt5.initialize():
        print("❌ Error al conectar con MetaTrader 5")
        return

    # Verificar la cuenta conectada
    account_info = mt5.account_info()
    if account_info is not None:
        print(f"✅ Conectado a la cuenta {account_info.login}")
    else:
        print("❌ No se pudo obtener información de la cuenta")
        mt5.shutdown()
        return

    # 🔹 1. Verificar órdenes abiertas
    orders = mt5.positions_get()
    if orders:
        print("\n📌 Órdenes abiertas:")
        for order in orders:
            print(f"🔹 Ticket: {order.ticket}, Símbolo: {order.symbol}, Tipo: {'BUY' if order.type == 0 else 'SELL'}, Volumen: {order.volume}, Precio: {order.price_open}")
    else:
        print("\n⚠️ No hay órdenes activas en este momento.")

    # 🔹 2. Verificar historial de órdenes ejecutadas en las últimas 24 horas
    time_from = datetime.now().timestamp() - 86400  # Últimos 24h
    time_to = datetime.now().timestamp()
    history = mt5.history_deals_get(from_date=time_from, to_date=time_to)

    if history:
        print("\n📌 Historial de operaciones en las últimas 24h:")
        for deal in history:
            print(f"🔹 Ticket: {deal.ticket}, Símbolo: {deal.symbol}, Tipo: {'BUY' if deal.type == 0 else 'SELL'}, Volumen: {deal.volume}, Precio: {deal.price}, Beneficio: {deal.profit}")
    else:
        print("\n⚠️ No hay historial de operaciones en las últimas 24 horas.")

    mt5.shutdown()

# ✅ Ejecutar solo si se corre como script directo
if __name__ == "__main__":
    revisar_operaciones()
