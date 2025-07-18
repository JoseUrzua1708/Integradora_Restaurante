import mysql.connector
from mysql.connector import Error

def validar_usuario(tipo_usuario, usuario_id):
    try:
        if tipo_usuario == "Empleado":
            tabla = "Empleados"
        else:
            tabla = "Clientes"
        cursor.execute(f"SELECT ID FROM {tabla} WHERE ID = {usuario_id}")
        return cursor.fetchone() is not None
    except:
        return False

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
        
        # Validar Tipo_Usuario
        while True:
            Tipo_Usuario = input("Inserta el tipo de usuario (Empleado/Cliente): ").capitalize()
            if Tipo_Usuario in ['Empleado', 'Cliente']:
                break
            print("Error: Tipo de usuario no válido. Debe ser 'Empleado' o 'Cliente'")
        
        # Validar Usuario_ID
        while True:
            Usuario_ID = input(f"Inserta el ID del {Tipo_Usuario.lower()}: ")
            if validar_usuario(Tipo_Usuario, Usuario_ID):
                break
            print(f"Error: No existe un {Tipo_Usuario.lower()} con ese ID")
        
        # Resto de los datos
        Accion = input("Inserta la acción realizada: ")
        Detalles = input("Inserta detalles adicionales (opcional, presiona Enter para omitir): ") or None
        
        # Validar Estatus
        while True:
            Estatus = input("Inserta el estatus (Exitoso/Fallido): ").capitalize()
            if Estatus in ['Exitoso', 'Fallido']:
                break
            print("Error: Estatus no válido. Debe ser 'Exitoso' o 'Fallido'")
        
        # Construir la sentencia SQL con parámetros seguros
        sentencia = """
        INSERT INTO Logs_Acceso 
        (Usuario_ID, Tipo_Usuario, Accion, Detalles, Estatus) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(sentencia, (
            Usuario_ID, Tipo_Usuario, Accion, Detalles, Estatus
        ))
        
        conexion.commit()
        print("Registro de acceso insertado correctamente. ID:", cursor.lastrowid)

except Error as ex:
    print("Error en la conexión de la BD: ", ex)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("La conexión se ha cerrado")