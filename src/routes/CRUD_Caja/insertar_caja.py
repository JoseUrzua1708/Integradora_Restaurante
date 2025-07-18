import mysql.connector
from mysql.connector import Error
from datetime import datetime

def mostrar_sucursales_activas(cursor):
    """Muestra las sucursales activas disponibles con formato mejorado"""
    try:
        cursor.execute("SELECT ID, Nombre, Direccion FROM Sucursales WHERE Estatus = 'Activa' ORDER BY Nombre")
        sucursales = cursor.fetchall()
        
        if not sucursales:
            print("\n⚠ No hay sucursales activas disponibles")
            return None
        
        print("\n╔══════════════════════════════╗")
        print("║      SUCURSALES ACTIVAS      ║")
        print("╠═════╦═════════════════════════╣")
        print("║ ID  ║ Nombre (Dirección)      ║")
        print("╠═════╬═════════════════════════╣")
        
        for id, nombre, direccion in sucursales:
            print(f"║ {id:<3} ║ {nombre:<15} ({direccion[:10]}...) ║")
        
        print("╚═════╩═════════════════════════╝")
        return sucursales
    
    except Error as e:
        print(f"\n❌ Error al obtener sucursales: {e}")
        return None

def mostrar_empleados_activos(cursor, sucursal_id=None):
    """Muestra empleados activos con formato de tabla, opcionalmente filtrados por sucursal"""
    try:
        query = """
            SELECT E.ID, E.Nombre, E.Apellido_P, P.Nombre as Puesto 
            FROM Empleados E
            JOIN Puestos P ON E.Puesto_ID = P.ID
            WHERE E.Estatus = 'Activo'
        """
        params = ()
        
        if sucursal_id:
            query += " AND E.Sucursal_ID = %s"
            params = (sucursal_id,)
        
        query += " ORDER BY E.Apellido_P, E.Nombre"
        cursor.execute(query, params)
        empleados = cursor.fetchall()
        
        if not empleados:
            print("\n⚠ No hay empleados activos disponibles" + 
                  (f" en esta sucursal" if sucursal_id else ""))
            return None
        
        print("\n╔══════════════════════════════════╗")
        print("║         EMPLEADOS ACTIVOS        ║")
        print("╠═════╦════════════════╦═══════════╣")
        print("║ ID  ║ Nombre         ║ Puesto    ║")
        print("╠═════╬════════════════╬═══════════╣")
        
        for id, nombre, apellido, puesto in empleados:
            nombre_completo = f"{nombre} {apellido}"
            print(f"║ {id:<3} ║ {nombre_completo:<14} ║ {puesto:<9} ║")
        
        print("╚═════╩════════════════╩═══════════╝")
        return empleados
    
    except Error as e:
        print(f"\n❌ Error al obtener empleados: {e}")
        return None

def validar_decimal(valor, campo, max_valor=None):
    """Valida que el valor sea un número decimal positivo"""
    try:
        valor = float(valor)
        if valor < 0:
            raise ValueError(f"{campo} no puede ser negativo")
        if max_valor is not None and valor > max_valor:
            raise ValueError(f"{campo} no puede exceder {max_valor}")
        return round(valor, 2)  # Redondear a 2 decimales
    except ValueError as ve:
        raise ValueError(f"{campo} debe ser un número válido: {ve}")

def verificar_caja_abierta(cursor, sucursal_id):
    """Verifica si ya existe una caja abierta en la sucursal"""
    try:
        cursor.execute("""
            SELECT ID FROM Caja 
            WHERE Sucursal_ID = %s AND Estatus = 'Abierta'
            LIMIT 1
        """, (sucursal_id,))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"\n❌ Error al verificar caja abierta: {e}")
        return False

def main():
    try:
        # Establecer conexión con manejo mejorado de errores
        conexion = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Jose1708$",
            database="administracion",
            autocommit=False  # Mejor control manual de transacciones
        )

        if not conexion.is_connected():
            print("❌ No se pudo conectar a la base de datos")
            return

        print("\n" + "="*50)
        print("   SISTEMA DE APERTURA DE CAJA   ".center(50))
        print("="*50)

        cursor = conexion.cursor(dictionary=True)  # Usar diccionarios para mayor claridad

        # 1. Mostrar y seleccionar sucursal
        sucursales = mostrar_sucursales_activas(cursor)
        if not sucursales:
            return

        while True:
            sucursal_id = input("\n🔹 Seleccione el ID de la sucursal (0 para salir): ").strip()
            
            if sucursal_id == "0":
                print("Operación cancelada por el usuario")
                return
                
            if not sucursal_id.isdigit() or not any(int(sucursal_id) == s[0] for s in sucursales):
                print("⚠ Error: ID de sucursal no válido. Intente nuevamente.")
                continue
                
            sucursal_id = int(sucursal_id)
            break

        # Verificar si ya hay una caja abierta en esta sucursal
        if verificar_caja_abierta(cursor, sucursal_id):
            print("\n⚠ Ya existe una caja abierta en esta sucursal. No se puede abrir otra.")
            return

        # 2. Mostrar y seleccionar empleado (solo de la sucursal seleccionada)
        empleados = mostrar_empleados_activos(cursor, sucursal_id)
        if not empleados:
            return

        while True:
            empleado_id = input("\n🔹 Seleccione el ID del empleado responsable (0 para cancelar): ").strip()
            
            if empleado_id == "0":
                print("Operación cancelada por el usuario")
                return
                
            if not empleado_id.isdigit() or not any(int(empleado_id) == e[0] for e in empleados):
                print("⚠ Error: ID de empleado no válido o no pertenece a esta sucursal. Intente nuevamente.")
                continue
                
            empleado_id = int(empleado_id)
            break

        # 3. Obtener datos de apertura de caja con validación mejorada
        while True:
            monto_inicial = input("\n💰 Ingrese el monto inicial de la caja (máximo $50,000): ").strip()
            try:
                monto_inicial = validar_decimal(monto_inicial, "Monto inicial", 50000)
                break
            except ValueError as ve:
                print(f"⚠ Error: {ve}")

        notas = input("\n📝 Ingrese notas adicionales (opcional, máximo 100 caracteres): ").strip()
        notas = None if notas == "" else notas[:100]  # Limitar a 100 caracteres

        # 4. Insertar registro de caja con transacción
        try:
            sentencia = """INSERT INTO Caja (
                Sucursal_ID, Empleado_ID, Fecha_Apertura, Monto_Inicial, Estatus, Notas
            ) VALUES (%s, %s, NOW(), %s, 'Abierta', %s)"""
            
            valores = (sucursal_id, empleado_id, monto_inicial, notas)

            cursor.execute(sentencia, valores)
            conexion.commit()
            
            # Obtener detalles de la caja creada
            caja_id = cursor.lastrowid
            cursor.execute("""
                SELECT C.ID, S.Nombre as Sucursal, 
                       CONCAT(E.Nombre, ' ', E.Apellido_P) as Empleado,
                       C.Fecha_Apertura, C.Monto_Inicial
                FROM Caja C
                JOIN Sucursales S ON C.Sucursal_ID = S.ID
                JOIN Empleados E ON C.Empleado_ID = E.ID
                WHERE C.ID = %s
            """, (caja_id,))
            caja_info = cursor.fetchone()

            print("\n" + "="*50)
            print("   APERTURA DE CAJA EXITOSA   ".center(50))
            print("="*50)
            print(f"\n🔹 ID de Caja: {caja_info['ID']}")
            print(f"🏦 Sucursal: {caja_info['Sucursal']}")
            print(f"👤 Empleado: {caja_info['Empleado']}")
            print(f"📅 Fecha/Hora: {caja_info['Fecha_Apertura'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💰 Monto Inicial: ${caja_info['Monto_Inicial']:,.2f}")
            print("\n" + "="*50)

        except Error as e:
            conexion.rollback()
            print(f"\n❌ Error al abrir la caja: {e}")
            return

    except Error as ex:
        print("\n❌ Error en la conexión de la BD:", ex)
        if 'conexion' in locals() and conexion.is_connected():
            conexion.rollback()

    except KeyboardInterrupt:
        print("\n\n⚠ Operación cancelada por el usuario")
        if 'conexion' in locals() and conexion.is_connected():
            conexion.rollback()

    except Exception as e:
        print("\n❌ Error inesperado:", e)
        if 'conexion' in locals() and conexion.is_connected():
            conexion.rollback()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()
            print("\n🔌 Conexión a la base de datos cerrada")