import MetaTrader5 as mt5
import time
import random

# 📌 CONFIGURACIÓN MT5
MT5_ACCOUNT = 530204016
MT5_PASSWORD = "3NN@$@M@Jz"
MT5_SERVER = "FTMO-Server3"

# 📌 CONFIGURACIÓN DE ORDEN
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
           "GBPJPY", "EURJPY", "EURAUD", "EURCAD", "GBPCAD", "GBPCHF", "AUDJPY", "NZDCAD"]

LOT_SIZE = 0.02
SL_POINTS = 500
TP_POINTS = 1000
MAX_TRADES = 1
INTERVALO_OPERACION = 60

# 📌 CONECTAR A MT5
if not mt5.initialize():
    print("❌ Error al iniciar MT5:", mt5.last_error())
    exit()

if not mt5.login(MT5_ACCOUNT, password=MT5_PASSWORD, server=MT5_SERVER):
    print("❌ Error al hacer login:", mt5.last_error())
    mt5.shutdown()
    exit()

print(f"✅ Conectado a la cuenta {MT5_ACCOUNT} en {MT5_SERVER}")

# 📌 FUNCIÓN PARA ABRIR UNA ORDEN EN MT5
def abrir_orden(symbol, tipo):
    sl = SL_POINTS if tipo == "BUY" else -SL_POINTS
    tp = TP_POINTS if tipo == "BUY" else -TP_POINTS

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ No se pudo obtener tick para {symbol}")
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": LOT_SIZE,
        "type": mt5.ORDER_TYPE_BUY if tipo == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": tick.ask if tipo == "BUY" else tick.bid,
        "sl": tick.ask - sl if tipo == "BUY" else tick.bid + sl,
        "tp": tick.ask + tp if tipo == "BUY" else tick.bid - tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "AutoTrade FTMO",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ Orden {tipo} abierta en {symbol}")
    else:
        print(f"❌ Error al abrir orden {tipo} en {symbol}: {result.comment}")

# 📌 FUNCIÓN PRINCIPAL DEL BOT
def bot_trading():
    while True:
        for symbol in SYMBOLS:
            posiciones = mt5.positions_get(symbol=symbol)
            if posiciones and len(posiciones) >= MAX_TRADES:
                continue

            tipo_operacion = random.choice(["BUY", "SELL"])
            abrir_orden(symbol, tipo_operacion)

        time.sleep(INTERVALO_OPERACION)

# 📌 INICIAR EL BOT
print("🚀 Iniciando bot de trading automático sin confluencias...")
bot_trading()
