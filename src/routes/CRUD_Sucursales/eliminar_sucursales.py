import mysql.connector
from mysql.connector import Error

class Eliminar_Sucursal:
    def __init__(self):
        self.eliminar_sucursal()

    def eliminar_sucursal(self):
        """Elimina una sucursal de la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                db="administracion"
            )
            if not conexion.is_connected():
                print("❌ Error al conectar a la base de datos")
                return

            print("ELIMINAR SUCURSAL")
            cursor = conexion.cursor()
            IdAEliminar = input("Introduce el ID del la sucursal: ")
            sentencia = """DELETE FROM Sucursales WHERE id= %s"""
            cursor.execute(sentencia, (IdAEliminar,))
            conexion.commit()
            print("Sucursal ELIMINADA con éxito...")

        except Error as ex:
            print("Error en la conexion de la BD: ", ex)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
                print("La conexión se ha cerrado")
