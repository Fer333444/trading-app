import MetaTrader5 as mt5

def ejecutar_operacion():
    # Conectar con MT5
    if not mt5.initialize():
        print("❌ Error al conectar con MetaTrader 5")
        return

    # Verificar conexión con la cuenta
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ No se pudo obtener la información de la cuenta. Verifica la conexión con MT5.")
        mt5.shutdown()
        return

    # Obtener balance de la cuenta
    balance_cuenta = account_info.balance
    print(f"✅ Conectado a MT5. Balance de la cuenta: {balance_cuenta} USD")

    # Parámetros de la operación
    par_divisas = "EURUSD"
    riesgo_porcentaje = 1
    stop_loss_pips = 20
    take_profit_pips = 40

    # Valor del pip (debes ajustar esto manualmente si no lo estás calculando)
    valor_pip = 10

    # Calcular el riesgo en dinero
    riesgo_dinero = (riesgo_porcentaje / 100) * balance_cuenta

    # Calcular el tamaño del lote
    if valor_pip > 0:
        lotaje = riesgo_dinero / (stop_loss_pips * valor_pip)
        lotaje = round(lotaje, 2)
    else:
        print("❌ No se pudo calcular el lotaje porque el valor del pip es 0.")
        mt5.shutdown()
        return

    print(f"📊 Tamaño del lote calculado: {lotaje}")

    # Definir la orden
    orden = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": par_divisas,
        "volume": lotaje,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(par_divisas).ask,
        "sl": mt5.symbol_info_tick(par_divisas).ask - stop_loss_pips * mt5.symbol_info(par_divisas).point,
        "tp": mt5.symbol_info_tick(par_divisas).ask + take_profit_pips * mt5.symbol_info(par_divisas).point,
        "deviation": 10,
        "magic": 123456,
        "comment": "Apertura Automática",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    resultado = mt5.order_send(orden)

    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Error al abrir la orden: {resultado.comment}")
    else:
        print(f"✅ Orden ejecutada con éxito. Ticket: {resultado.order}")

    mt5.shutdown()

# 🟢 Ejecutar solo si se corre directamente (no se debe importar en Flask)
if __name__ == "__main__":
    ejecutar_operacion()
