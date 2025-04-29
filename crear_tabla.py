import mysql.connector

conexion = mysql.connector.connect(
    host="ballast.proxy.rlwy.net",
    port=47866,
    user="flujo",
    password="Sebas301985$!",
    database="railway"
)

cursor = conexion.cursor()

sql = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) UNIQUE NOT NULL,
    clave_hash VARCHAR(255) NOT NULL
);
"""

try:
    cursor.execute(sql)
    conexion.commit()
    print("✅ Tabla 'usuarios' creada correctamente.")
except mysql.connector.Error as err:
    print(f"❌ Error al crear la tabla: {err}")

cursor.close()
conexion.close()
