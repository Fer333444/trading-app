import MetaTrader5 as mt5

def enviar_orden_mt5(symbol, tipo, volumen, sl, tp):
    info = mt5.symbol_info(symbol)
    if info is None or not info.visible:
        return f"Símbolo no válido o no visible: {symbol}"

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return f"No se pudo obtener el precio para {symbol}"

    if tipo == "buy":
        tipo_operacion = mt5.ORDER_TYPE_BUY
        precio = tick.ask
    elif tipo == "sell":
        tipo_operacion = mt5.ORDER_TYPE_SELL
        precio = tick.bid
    else:
        return f"Tipo de operación no válido: {tipo}"

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volumen,
        "type": tipo_operacion,
        "price": precio,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "Orden enviada desde sistema_riesgo",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    resultado = mt5.order_send(request)

    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        return f"Error al ejecutar orden: {resultado.retcode} - {resultado.comment}"
    else:
        return f"Orden ejecutada correctamente: ticket #{resultado.order}"

