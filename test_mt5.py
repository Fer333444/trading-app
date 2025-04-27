
# Reemplaza estos datos con los reales de tu cuenta
login = 510065036         # Tu número de cuenta MT5
password = "8j!gSx?FL" # Tu contraseña MT5
server = "FTMO-Server"   # Nombre exacto del servidor (ej: 'MetaQuotes-Demo')

if not mt5.initialize(login=login, password=password, server=server):
    print("❌ Error al conectar:", mt5.last_error())
else:
    print("✅ Conexión exitosa con MetaTrader 5")
    mt5.shutdown()
