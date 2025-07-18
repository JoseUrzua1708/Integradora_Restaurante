import mysql.connector
from mysql.connector import Error
from datetime import datetime

def mostrar_opciones(cursor, tabla, campo_id, campo_nombre, mensaje):
    """Muestra opciones disponibles de una tabla relacionada"""
    cursor.execute(f"SELECT {campo_id}, {campo_nombre} FROM {tabla}")
    resultados = cursor.fetchall()
    
    print(f"\n{mensaje}:")
    for id, nombre in resultados:
        print(f"{id}: {nombre}")
    
    return resultados

def validar_fecha(fecha_str):
    """Valida el formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

try:
    # Establecer conexión
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

        # 1. Mostrar roles disponibles
        roles = mostrar_opciones(cursor, "Roles", "ID", "Nombre", "Roles disponibles")
        rol_id = input("\nSeleccione el ID del rol del empleado: ")
        if not any(int(rol_id) == r[0] for r in roles):
            print("Error: ID de rol no válido")
            exit()

        # 2. Mostrar sucursales disponibles (opcional)
        sucursales = mostrar_opciones(cursor, "Sucursales", "ID", "Nombre", "Sucursales disponibles")
        sucursal_id = input("\nSeleccione el ID de la sucursal (deje vacío si no aplica): ")
        if sucursal_id and not any(int(sucursal_id) == s[0] for s in sucursales):
            print("Error: ID de sucursal no válido")
            exit()
        sucursal_id = None if sucursal_id == "" else sucursal_id

        # 3. Datos personales del empleado
        print("\nDatos personales del empleado:")
        nombre = input("Nombre (max 25 caracteres): ").strip()
        if len(nombre) > 25:
            print("Error: El nombre no puede exceder 25 caracteres")
            exit()

        apellido_p = input("Apellido paterno (max 20 caracteres): ").strip()
        if len(apellido_p) > 20:
            print("Error: El apellido paterno no puede exceder 20 caracteres")
            exit()

        apellido_m = input("Apellido materno (max 20 caracteres, opcional): ").strip()
        if apellido_m and len(apellido_m) > 20:
            print("Error: El apellido materno no puede exceder 20 caracteres")
            exit()
        apellido_m = None if apellido_m == "" else apellido_m

        # 4. Datos de contacto y credenciales
        correo = input("Correo electrónico (max 30 caracteres): ").strip()
        if len(correo) > 30:
            print("Error: El correo no puede exceder 30 caracteres")
            exit()

        contraseña = input("Contraseña (max 12 caracteres): ").strip()
        if len(contraseña) > 12:
            print("Error: La contraseña no puede exceder 12 caracteres")
            exit()

        telefono = input("Teléfono (10 dígitos, opcional): ").strip()
        if telefono and (not telefono.isdigit() or len(telefono) != 10):
            print("Error: El teléfono debe tener exactamente 10 dígitos")
            exit()
        telefono = None if telefono == "" else telefono

        # 5. Datos de identificación
        rfc = input("RFC (13 caracteres, opcional): ").strip().upper()
        if rfc and len(rfc) != 13:
            print("Error: El RFC debe tener exactamente 13 caracteres")
            exit()
        rfc = None if rfc == "" else rfc

        curp = input("CURP (18 caracteres, opcional): ").strip().upper()
        if curp and len(curp) != 18:
            print("Error: La CURP debe tener exactamente 18 caracteres")
            exit()
        curp = None if curp == "" else curp

        # 6. Dirección y datos personales
        direccion = input("Dirección (opcional): ").strip()
        direccion = None if direccion == "" else direccion

        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD, opcional): ").strip()
        if fecha_nacimiento and not validar_fecha(fecha_nacimiento):
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD")
            exit()
        fecha_nacimiento = None if fecha_nacimiento == "" else fecha_nacimiento

        # 7. Datos de género y estatus
        genero = input("Género (Masculino/Femenino/Otro, opcional): ").strip().capitalize()
        if genero and genero not in ('Masculino', 'Femenino', 'Otro'):
            print("Error: Género no válido")
            exit()
        genero = None if genero == "" else genero

        print("\nEstatus disponibles: Activo, Inactivo, Suspendido, Vacaciones")
        estatus = input("Estatus del empleado [Activo]: ").strip().capitalize()
        if estatus == "":
            estatus = "Activo"
        elif estatus not in ('Activo', 'Inactivo', 'Suspendido', 'Vacaciones'):
            print("Error: Estatus no válido")
            exit()

        # 8. Datos laborales
        salario = input("Salario (opcional): ").strip()
        if salario:
            try:
                salario = float(salario)
            except ValueError:
                print("Error: El salario debe ser un número")
                exit()
        else:
            salario = None

        print("\nTipos de contrato disponibles: Tiempo Completo, Medio Tiempo, Temporal, Por Horas")
        tipo_contrato = input("Tipo de contrato (opcional): ").strip().title()
        if tipo_contrato and tipo_contrato not in ('Tiempo Completo', 'Medio Tiempo', 'Temporal', 'Por Horas'):
            print("Error: Tipo de contrato no válido")
            exit()
        tipo_contrato = None if tipo_contrato == "" else tipo_contrato

        fecha_contratacion = input("Fecha de contratación (YYYY-MM-DD, opcional): ").strip()
        if fecha_contratacion and not validar_fecha(fecha_contratacion):
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD")
            exit()
        fecha_contratacion = None if fecha_contratacion == "" else fecha_contratacion

        fecha_terminacion = input("Fecha de terminación (YYYY-MM-DD, opcional): ").strip()
        if fecha_terminacion and not validar_fecha(fecha_terminacion):
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD")
            exit()
        fecha_terminacion = None if fecha_terminacion == "" else fecha_terminacion

        # 9. Insertar empleado (USANDO EL NOMBRE EXACTO DE LA COLUMNA CON Ñ)
        sentencia = """INSERT INTO Empleados (
            Rol_ID, Sucursal_ID, Nombre, Apellido_P, Apellido_M, Correo, `Contraseña`,
            Telefono, RFC, CURP, Direccion, Fecha_Nacimiento, Genero, Estatus,
            Salario, Tipo_Contrato, Fecha_Contratacion, Fecha_Terminacion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        datos = (
            rol_id, sucursal_id, nombre, apellido_p, apellido_m, correo, contraseña,
            telefono, rfc, curp, direccion, fecha_nacimiento, genero, estatus,
            salario, tipo_contrato, fecha_contratacion, fecha_terminacion
        )

        cursor.execute(sentencia, datos)
        conexion.commit()
        print("\n✅ Empleado registrado correctamente")

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