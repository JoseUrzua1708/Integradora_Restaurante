import mysql.connector
from mysql.connector import Error

def validar_id(tabla, id):
    try:
        cursor.execute(f"SELECT ID FROM {tabla} WHERE ID = {id}")
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
        
        # Validar Cliente_ID
        while True:
            Cliente_ID = input("Inserta el ID del cliente: ")
            if validar_id("Clientes", Cliente_ID):
                break
            print("Error: El ID de cliente no existe. Intente nuevamente.")
        
        # Validar Empleado_ID
        while True:
            Empleado_ID = input("Inserta el ID del empleado: ")
            if validar_id("Empleados", Empleado_ID):
                break
            print("Error: El ID de empleado no existe. Intente nuevamente.")
        
        # Resto de los datos
        Asunto = input("Inserta el asunto del ticket: ")
        Descripcion = input("Inserta la descripción del problema: ")
        
        # Validar Estatus
        estatus_validos = ['Abierto', 'En proceso', 'Resuelto', 'Cerrado']
        while True:
            Estatus = input(f"Inserta el estatus ({'/'.join(estatus_validos)}): ")
            if Estatus in estatus_validos:
                break
            print("Error: Estatus no válido.")
        
        # Validar Prioridad
        prioridades_validas = ['Baja', 'Media', 'Alta', 'Crítica']
        while True:
            Prioridad = input(f"Inserta la prioridad ({'/'.join(prioridades_validas)}): ")
            if Prioridad in prioridades_validas:
                break
            print("Error: Prioridad no válida.")
        
        # Datos opcionales
        Solucion = input("Inserta la solución (opcional, presiona Enter para omitir): ") or None
        Tiempo_Resolucion = input("Inserta el tiempo de resolución en minutos (opcional, presiona Enter para omitir): ") or None
        
        # Validar Categoría
        categorias_validas = ['Sistema', 'Pedido', 'Pago', 'Reserva', 'Otro']
        while True:
            Categoria = input(f"Inserta la categoría ({'/'.join(categorias_validas)}): ")
            if Categoria in categorias_validas:
                break
            print("Error: Categoría no válida.")
        
        # Construir la sentencia SQL con parámetros seguros
        sentencia = """
        INSERT INTO Tickets_Soporte 
        (Cliente_ID, Empleado_ID, Asunto, Descripcion, Estatus, Prioridad, Solucion, Tiempo_Resolucion, Categoria) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sentencia, (
            Cliente_ID, Empleado_ID, Asunto, Descripcion, Estatus, 
            Prioridad, Solucion, Tiempo_Resolucion, Categoria
        ))
        
        conexion.commit()
        print("Ticket de soporte insertado correctamente. ID:", cursor.lastrowid)

except Error as ex:
    print("Error en la conexión de la BD: ", ex)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("La conexión se ha cerrado")