import mysql.connector

# ⚠️ Usa los datos actuales correctos de Railway
conexion = mysql.connector.connect(
    host="ballast.proxy.rlwy.net",
    port=47866,
    user="root",
    password="tu_clave_actual_de_root",
    database="railway"
)

cursor = conexion.cursor()

# ⚠️ Cambia 'flujo' y la contraseña por algo tuyo si quieres
sql = """
CREATE USER 'flujo'@'%' IDENTIFIED BY 'Sebas301985$!';
GRANT ALL PRIVILEGES ON railway.* TO 'flujo'@'%';
FLUSH PRIVILEGES;
"""

try:
    cursor.execute(sql, multi=True)
    conexion.commit()
    print("✅ Usuario creado correctamente.")
except mysql.connector.Error as err:
    print(f"❌ Error al crear usuario: {err}")

cursor.close()
conexion.close()
