import mysql.connector
from mysql.connector import Error
from datetime import datetime

def mostrar_clientes(cursor):
    cursor.execute("SELECT ID, Nombre, Apellido_P FROM Clientes WHERE Estatus = 'Activo'")
    clientes = cursor.fetchall()
    print("\nClientes disponibles:")
    for cli in clientes:
        print(f"ID: {cli[0]}, Nombre: {cli[1]} {cli[2]}")
    return clientes

def mostrar_sucursales(cursor):
    cursor.execute("SELECT ID, Nombre FROM Sucursales WHERE Estatus = 'Activa'")
    sucursales = cursor.fetchall()
    print("\nSucursales disponibles:")
    for suc in sucursales:
        print(f"ID: {suc[0]}, Nombre: {suc[1]}")
    return sucursales

def mostrar_mesas_disponibles(cursor, sucursal_id):
    cursor.execute(f"""
        SELECT ID, Numero_Mesa, Capacidad 
        FROM Mesas 
        WHERE Sucursal_ID = {sucursal_id} 
        AND Estatus = 'Disponible'
    """)
    mesas = cursor.fetchall()
    if not mesas:
        print("\nNo hay mesas disponibles en esta sucursal.")
        return None
    print("\nMesas disponibles:")
    for mesa in mesas:
        print(f"ID: {mesa[0]}, Mesa: {mesa[1]}, Capacidad: {mesa[2]}")
    return mesas

def mostrar_empleados(cursor, sucursal_id):
    cursor.execute(f"""
        SELECT ID, Nombre, Apellido_P 
        FROM Empleados 
        WHERE Sucursal_ID = {sucursal_id} 
        AND Estatus = 'Activo'
    """)
    empleados = cursor.fetchall()
    print("\nEmpleados disponibles:")
    for emp in empleados:
        print(f"ID: {emp[0]}, Nombre: {emp[1]} {emp[2]}")
    return empleados

def generar_codigo_pedido(sucursal_id):
    # Código más corto: P + ID sucursal + hora y minuto
    timestamp = datetime.now().strftime("%H%M")
    return f"P{sucursal_id}-{timestamp}"

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Jose1708$",
        db="administracion"
    )

    if conexion.is_connected():
        print("\nConexión exitosa")
        cursor = conexion.cursor()
        
        # 1. Seleccionar sucursal
        sucursales = mostrar_sucursales(cursor)
        sucursal_id = int(input("\nIngrese el ID de la sucursal: "))
        
        # 2. Seleccionar cliente (opcional)
        clientes = mostrar_clientes(cursor)
        cliente_input = input("Ingrese el ID del cliente (deje vacío si no aplica): ")
        cliente_id = int(cliente_input) if cliente_input.strip() else None
        
        # 3. Seleccionar tipo de pedido
        tipo_pedido = input("\nTipo de pedido (Presencial/Domicilio/Recoger): ").capitalize()
        while tipo_pedido not in ['Presencial', 'Domicilio', 'Recoger']:
            print("Tipo no válido. Intente nuevamente.")
            tipo_pedido = input("Tipo de pedido (Presencial/Domicilio/Recoger): ").capitalize()
            
        mesa_id = None
        if tipo_pedido == 'Presencial':
            mesas = mostrar_mesas_disponibles(cursor, sucursal_id)
            if mesas:
                while True:
                    try:
                        mesa_id = int(input("\nIngrese el ID de la mesa: "))
                        # Verificar que la mesa existe
                        cursor.execute(f"SELECT ID FROM Mesas WHERE ID = {mesa_id} AND Sucursal_ID = {sucursal_id}")
                        if not cursor.fetchone():
                            print("Error: El ID de mesa no existe o no pertenece a esta sucursal")
                            continue
                        break
                    except ValueError:
                        print("Por favor ingrese un número válido")
        
        # 4. Seleccionar empleado
        empleados = mostrar_empleados(cursor, sucursal_id)
        empleado_id = int(input("\nIngrese el ID del empleado que registra el pedido: "))
        
        # 5. Datos adicionales
        notas = input("\nNotas adicionales (opcional): ")
        
        direccion_entrega = None
        telefono_contacto = None
        if tipo_pedido == 'Domicilio':
            direccion_entrega = input("Dirección de entrega: ")
            telefono_contacto = input("Teléfono de contacto: ")
        
        tiempo_input = input("Tiempo estimado en minutos (opcional): ")
        tiempo_estimado = int(tiempo_input) if tiempo_input.strip() else None
        
        # 6. Generar código de pedido
        codigo_pedido = generar_codigo_pedido(sucursal_id)
        print(f"\nCódigo de pedido generado: {codigo_pedido}")
        
        # 7. Insertar pedido
        sql = """INSERT INTO Pedidos (
                Cliente_ID, Sucursal_ID, Mesa_ID, Empleado_ID, Tipo,
                Notas, Direccion_Entrega, Telefono_Contacto,
                Tiempo_Estimado, Codigo_Pedido, Fecha_Hora
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
        
        valores = (
            cliente_id,
            sucursal_id,
            mesa_id if tipo_pedido == 'Presencial' else None,
            empleado_id,
            tipo_pedido,
            notas if notas.strip() else None,
            direccion_entrega,
            telefono_contacto,
            tiempo_estimado,
            codigo_pedido
        )
        
        cursor.execute(sql, valores)
        conexion.commit()
        print(f"\nPedido registrado exitosamente! Código: {codigo_pedido}")

except Error as ex:
    print("\nError en la base de datos: ", ex)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("\nLa conexión se ha cerrado")