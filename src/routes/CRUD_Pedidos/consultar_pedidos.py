import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Jose1708$",
        db="administracion"
    )

    if conexion.is_connected():
        print("Conexión exitosa")
        
        cursor = conexion.cursor()
        
        cursor.execute("SELECT database();")
        baseDatos = cursor.fetchone()
        print("La base de datos es:", baseDatos)
        
        cursor.execute("SELECT * FROM Pedidos;")
        registros = cursor.fetchall()
        
        print(f"Total de registros: {cursor.rowcount}")
        
        for fila in registros:
            print(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], fila[12], fila[13], fila[14], fila[15], fila[16], fila[17], fila[18])

except Error as ex:
    print(f"Error en la conexión de la BD: {ex}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("La conexión se ha cerrado")