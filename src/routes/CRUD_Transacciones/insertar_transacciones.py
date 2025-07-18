import mysql.connector
from mysql.connector import Error
from datetime import datetime

def mostrar_cajas_abiertas(cursor):
    cursor.execute("""
        SELECT c.ID, s.Nombre AS Sucursal, e.Nombre AS Empleado, c.Monto_Inicial 
        FROM Caja c
        JOIN Sucursales s ON c.Sucursal_ID = s.ID
        JOIN Empleados e ON c.Empleado_ID = e.ID
        WHERE c.Estatus = 'Abierta'
    """)
    cajas = cursor.fetchall()
    print("\nCajas disponibles (abiertas):")
    for caja in cajas:
        print(f"ID: {caja[0]}, Sucursal: {caja[1]}, Empleado: {caja[2]}, Monto Inicial: {caja[3]}")
    return cajas

def mostrar_pedidos_pendientes_pago(cursor):
    cursor.execute("""
        SELECT p.ID, p.Codigo_Pedido, p.Total, c.Nombre AS Cliente
        FROM Pedidos p
        LEFT JOIN Clientes c ON p.Cliente_ID = c.ID
        WHERE p.Estatus IN ('Listo', 'Entregado') AND p.Total > 0
    """)
    pedidos = cursor.fetchall()
    print("\nPedidos pendientes de pago:")
    for pedido in pedidos:
        print(f"ID: {pedido[0]}, Código: {pedido[1]}, Total: {pedido[2]}, Cliente: {pedido[3]}")
    return pedidos

def mostrar_empleados_activos(cursor):
    cursor.execute("""
        SELECT ID, Nombre, Apellido_P 
        FROM Empleados 
        WHERE Estatus = 'Activo'
    """)
    empleados = cursor.fetchall()
    print("\nEmpleados activos:")
    for emp in empleados:
        print(f"ID: {emp[0]}, Nombre: {emp[1]} {emp[2]}")
    return empleados

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
        
        # 1. Seleccionar caja abierta
        cajas = mostrar_cajas_abiertas(cursor)
        if not cajas:
            print("\nNo hay cajas abiertas. No se pueden registrar transacciones.")
            exit()
            
        caja_id = int(input("\nIngrese el ID de la caja: "))
        
        # 2. Seleccionar tipo de transacción
        tipo_transaccion = input("\nTipo de transacción (Ingreso/Egreso/Apertura/Cierre): ").capitalize()
        while tipo_transaccion not in ['Ingreso', 'Egreso', 'Apertura', 'Cierre']:
            print("Tipo no válido. Intente nuevamente.")
            tipo_transaccion = input("Tipo de transacción (Ingreso/Egreso/Apertura/Cierre): ").capitalize()
        
        # 3. Manejar datos según el tipo de transacción
        pedido_id = None
        if tipo_transaccion == 'Ingreso':
            pedidos = mostrar_pedidos_pendientes_pago(cursor)
            if pedidos:
                pedido_id = input("Ingrese el ID del pedido (deje vacío si no aplica): ")
                pedido_id = int(pedido_id) if pedido_id else None
        
        # 4. Ingresar monto
        monto = float(input("\nMonto de la transacción: "))
        
        # 5. Seleccionar método de pago (solo para ingresos/egresos)
        metodo_pago = None
        if tipo_transaccion in ['Ingreso', 'Egreso']:
            print("\nMétodos de pago disponibles:")
            print("1. Efectivo")
            print("2. Tarjeta Crédito")
            print("3. Tarjeta Débito")
            print("4. Transferencia")
            print("5. Vale")
            print("6. Otro")
            
            opcion = int(input("Seleccione el método de pago (1-6): "))
            metodos = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Vale', 'Otro']
            metodo_pago = metodos[opcion-1] if 1 <= opcion <= 6 else 'Otro'
        
        # 6. Seleccionar empleado
        empleados = mostrar_empleados_activos(cursor)
        empleado_id = int(input("\nIngrese el ID del empleado que realiza la transacción: "))
        
        # 7. Datos adicionales
        descripcion = input("\nDescripción (opcional): ")
        referencia = input("Referencia (opcional): ")
        
        # 8. Insertar la transacción
        sql = """INSERT INTO Transacciones (
                Caja_ID, Pedido_ID, Tipo, Monto, Metodo_Pago,
                Descripcion, Empleado_ID, Referencia
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        valores = (
            caja_id,
            pedido_id if tipo_transaccion == 'Ingreso' else None,
            tipo_transaccion,
            monto,
            metodo_pago if tipo_transaccion in ['Ingreso', 'Egreso'] else None,
            descripcion if descripcion else None,
            empleado_id,
            referencia if referencia else None
        )
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        # Actualizar estado del pedido si es un ingreso por pedido
        if tipo_transaccion == 'Ingreso' and pedido_id:
            cursor.execute(f"UPDATE Pedidos SET Estatus = 'Pagado' WHERE ID = {pedido_id}")
            conexion.commit()
        
        print("\nTransacción registrada exitosamente!")

except Error as ex:
    print("Error en la conexión de la BD: ", ex)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("La conexión se ha cerrado")