def conectar_a_mt5():
    print("🔵 SESIÓN ACTUAL:")
    print("Usuario:", session.get("mt5_usuario"))
    print("Servidor:", session.get("mt5_servidor"))
    print("Password:", "*" * len(session.get("mt5_password", "")))

    if not all(k in session for k in ['mt5_usuario', 'mt5_password', 'mt5_servidor']):
        print("⚠️ Faltan datos en sesión")
        return False

    mt5.shutdown()  # ✅ Cierra sesión anterior antes de reconectar

    if not mt5.initialize(
        login=int(session['mt5_usuario']),
        server=session['mt5_servidor'],
        password=session['mt5_password']
    ):
        print("❌ MT5 ERROR:", mt5.last_error())
        return False

    return True
