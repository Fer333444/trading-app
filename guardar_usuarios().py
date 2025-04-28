import mysql.connector
from werkzeug.security import generate_password_hash

def guardar_usuario_mysql(usuario, clave):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mi_base_datos"
        )
        cursor = conexion.cursor()
        clave_hash = generate_password_hash(clave)
        cursor.execute("INSERT INTO usuarios (usuario, clave_hash) VALUES (%s, %s)", (usuario, clave_hash))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("⚠️ Error guardando usuario en MySQL:", e)
        return False
