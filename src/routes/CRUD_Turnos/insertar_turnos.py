import mysql.connector
from mysql.connector import Error
from datetime import datetime

def convertir_hora(hora_str):
    """Convierte formato de hora a HH:MM:SS para MySQL"""
    try:
        # Limpiar espacios y convertir a mayúsculas
        hora_str = hora_str.strip().upper()
        
        # Si ya tiene formato HH:MM:SS
        if len(hora_str.split(':')) == 3 and 'AM' not in hora_str and 'PM' not in hora_str:
            datetime.strptime(hora_str, '%H:%M:%S')
            return hora_str
        
        # Convertir formato 12h a 24h
        formato = '%I:%M%p' if len(hora_str.split(':')) == 2 else '%I:%M:%S%p'
        hora_obj = datetime.strptime(hora_str, formato)
        return hora_obj.strftime('%H:%M:%S')
        
    except ValueError:
        raise ValueError("Formato de hora no válido. Use HH:MM o HH:MM:SS (con AM/PM opcional)")

def mostrar_empleados(cursor):
    cursor.execute("SELECT ID, Nombre, Apellido_P, Sucursal_ID FROM Empleados WHERE Estatus = 'Activo'")
    empleados = cursor.fetchall()
    print("\nEmpleados disponibles:")
    for emp in empleados:
        print(f"ID: {emp[0]}, Nombre: {emp[1]} {emp[2]}, Sucursal_ID: {emp[3]}")
    return empleados
    
def mostrar_sucursales(cursor):
    cursor.execute("SELECT ID, Nombre FROM Sucursales WHERE Estatus = 'Activa'")
    sucursales = cursor.fetchall()
    print("\nSucursales disponibles:")
    for suc in sucursales:
        print(f"ID: {suc[0]}, Nombre: {suc[1]}")
    return sucursales

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
        
        # Mostrar empleados disponibles
        empleados = mostrar_empleados(cursor)
        empleado_id = input("\nIngrese el ID del empleado: ")
        
        if not empleado_id.isdigit() or not any(int(empleado_id) == emp[0] for emp in empleados):
            print("Error: ID de empleado no válido")
            exit()
        empleado_id = int(empleado_id)

        # Verificar empleado
        cursor.execute("SELECT Sucursal_ID FROM Empleados WHERE ID = %s AND Estatus = 'Activo'", (empleado_id,))
        empleado = cursor.fetchone()
        if not empleado:
            print("Error: Empleado no encontrado o no está activo")
            exit()

        sucursal_empleado = empleado[0]

        # Mostrar sucursales disponibles
        sucursales = mostrar_sucursales(cursor)
        sucursal_id = input(f"\nIngrese el ID de la Sucursal (el empleado pertenece a {sucursal_empleado}): ") or str(sucursal_empleado)
        
        if not sucursal_id.isdigit() or not any(int(sucursal_id) == suc[0] for suc in sucursales):
            print("Error: ID de sucursal no válido")
            exit()
        sucursal_id = int(sucursal_id)

        # Obtener datos del turno
        fecha = input("Ingresa la fecha del turno (YYYY-MM-DD): ")
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD")
            exit()

        hora_entrada = input("Ingresa la hora de entrada del empleado (HH:MM o HH:MM:SS): ")
        try:
            hora_entrada = convertir_hora(hora_entrada)
        except ValueError as ve:
            print(f"Error: {ve}")
            exit()

        hora_salida = input("Ingresa la hora de salida del empleado (HH:MM o HH:MM:SS) [OPCIONAL]: ")
        if hora_salida:
            try:
                hora_salida = convertir_hora(hora_salida)
            except ValueError as ve:
                print(f"Error: {ve}")
                exit()
        else:
            hora_salida = None

        descanso = input("Ingresa el día de descanso del empleado (YYYY-MM-DD): ")
        try:
            datetime.strptime(descanso, '%Y-%m-%d')
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD")
            exit()

        notas = input("Ingresa notas adicionales [OPCIONAL]: ") or None
        horas_extras = input("Ingresa las horas extras del empleado [OPCIONAL, default 0.00]: ") or "0.00"
        try:
            horas_extras = float(horas_extras)
        except ValueError:
            print("Error: Las horas extras deben ser un número")
            exit()

        # Insertar turno
        sentencia = """INSERT INTO Turnos (
            Sucursal_ID, Empleado_ID, Fecha, Hora_Entrada, Hora_Salida, 
            descanso, Notas, Horas_Extras
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        valores = (
            sucursal_id,
            empleado_id,
            fecha,
            hora_entrada,
            hora_salida,
            descanso,
            notas,
            horas_extras
        )

        cursor.execute(sentencia, valores)
        conexion.commit()
        print("\n✅ Turno registrado correctamente")

except Error as ex:
    print("\n❌ Error en la conexión de la BD:", ex)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

except Exception as e:
    print("\n❌ Error:", e)
    if 'conexion' in locals() and conexion.is_connected():
        conexion.rollback()

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("🔌 La conexión se ha cerrado")