import mysql.connector
from mysql.connector import Error

def get_connection():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="12345",
            database="administracion"
        )

        if connection.is_connected():
            print("Conexion exitosa")
            info_server = connection.get_server_info()
            print("Informacion del servidor: ", info_server)
            return connection
        
    except Error as e:
        print("Error al conectar con la base de datos: ", e)
        return None