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
        print("ELIMINAR TRANSACCION")
        cursor = conexion.cursor()
        IdAEliminar = input("Introduce el ID de la Transaccion: ")
        sentencia = """DELETE FROM Transacciones WHERE id= %s"""
        cursor.execute(sentencia, (IdAEliminar,))
        conexion.commit()
        print("Transaccion Eliminada con éxito...")

except Error as ex:
    print("Error en la conexion de la BD: ", ex)

finally:
    if conexion.is_connected():
        conexion.close()
        print("La conexión se ha cerrado")
