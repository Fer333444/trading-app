# guardar_historial.py
import json
import sqlite3
import mysql.connector
from datetime import datetime

def guardar_historial(operacion):
    # 1. Guardar en archivo JSON
    try:
        with open("historial.json", "r") as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []

    historial.append(operacion)

    with open("historial.json", "w") as f:
        json.dump(historial, f, indent=4)

    # 2. Guardar en base de datos local SQLite
    conn = sqlite3.connect("historial.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simbolo TEXT,
            tipo TEXT,
            lote REAL,
            precio_apertura REAL,
            sl REAL,
            tp REAL,
            fecha TEXT
        )
    """)
    c.execute("""
        INSERT INTO operaciones (simbolo, tipo, lote, precio_apertura, sl, tp, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        operacion["simbolo"], operacion["tipo"], operacion["lote"],
        operacion["precio_apertura"], operacion["sl"], operacion["tp"], operacion["fecha"]
    ))
    conn.commit()
    conn.close()

    # 3. Guardar en base de datos online MySQL (cambia con tus datos)
    try:
        mydb = mysql.connector.connect(
            host="tu_host",
            user="tu_usuario",
            password="tu_password",
            database="tu_basededatos"
        )
        cursor = mydb.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operaciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simbolo VARCHAR(10),
                tipo VARCHAR(10),
                lote FLOAT,
                precio_apertura FLOAT,
                sl FLOAT,
                tp FLOAT,
                fecha VARCHAR(50)
            )
        """)
        cursor.execute("""
            INSERT INTO operaciones (simbolo, tipo, lote, precio_apertura, sl, tp, fecha)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            operacion["simbolo"], operacion["tipo"], operacion["lote"],
            operacion["precio_apertura"], operacion["sl"], operacion["tp"], operacion["fecha"]
        ))
        mydb.commit()
        cursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("[MySQL] Error:", err)
