import mysql.connector
from mysql.connector import Error

class eliminar_rol:
    def __init__(self):
        self.eliminar_rol()

    def eliminar_rol(self):
        """Elimina un rol de la base de datos"""

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                db="administracion"
            )

            if conexion.is_connected():
                print("ELIMINA REGISTRO")
                cursor = conexion.cursor()
                IdAEliminar = input("Introduce el ID del rol: ")
                sentencia = """DELETE FROM rol WHERE id= %s"""
                cursor.execute(sentencia, (IdAEliminar,))
                conexion.commit()
                print("Registro ELIMINADO con éxito...")

        except Error as ex:
            print("Error en la conexion de la BD: ", ex)

        finally:
            if conexion.is_connected():
                conexion.close()
                print("La conexión se ha cerrado")