from datetime import datetime
import json

# ✅ FUNCIÓN para guardar historial (no modificar)
def guardar_operaciones_mt5(usuario):
    from_date = datetime(2020, 1, 1)
    to_date = datetime.now()
    deals = mt5.history_deals_get(from_date, to_date)

    if deals is None or len(deals) == 0:
        print("⚠️ No hay operaciones históricas.")
        return

    try:
        with open("historial.json", "r") as file:
            historial = json.load(file)
    except FileNotFoundError:
        historial = []

    ids_existentes = {op['ticket'] for op in historial if 'ticket' in op}
    nuevas_op = []

    for deal in deals:
        if deal.ticket in ids_existentes:
            continue
        if deal.type not in [0, 1]:
            continue
        if deal.volume <= 0:
            continue

        nueva_op = {
            "ticket": deal.ticket,
            "symbol": deal.symbol,
            "type": deal.type,
            "volume": deal.volume,
            "price": deal.price,
            "profit": deal.profit,
            "usuario": usuario,
            "fecha": datetime.fromtimestamp(deal.time).strftime('%Y-%m-%d %H:%M:%S')
        }

        nuevas_op.append(nueva_op)

    if nuevas_op:
        historial.extend(nuevas_op)
        with open("historial.json", "w") as file:
            json.dump(historial, file, indent=4)
        print(f"✅ {len(nuevas_op)} operaciones guardadas.")
    else:
        print("ℹ️ No hay operaciones nuevas.")

# ✅ NUEVA FUNCIÓN para ejecutar operaciones en MT5
def ejecutar_operacion(simbolo, tipo, volumen):
    tipo_operacion = mt5.ORDER_TYPE_BUY if tipo.lower() == "buy" else mt5.ORDER_TYPE_SELL

    tick = mt5.symbol_info_tick(simbolo)
    if not tick:
        print("❌ No se pudo obtener información del símbolo")
        return False

    precio = tick.ask if tipo_operacion == mt5.ORDER_TYPE_BUY else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": simbolo,
        "volume": volumen,
        "type": tipo_operacion,
        "price": precio,
        "deviation": 10,
        "magic": 234000,
        "comment": "Operación manual desde app",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    resultado = mt5.order_send(request)

    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Error al ejecutar operación: {resultado.comment}")
        return False

    print(f"✅ Operación ejecutada con éxito: Ticket #{resultado.order}")
    return True
