import mysql.connector
from mysql.connector import Error
from datetime import datetime

class insertar_rol:
    """Clase para insertar roles con validación mejorada"""
    def __init__(self):
        self.insertar_rol()

    def insertar_rol(self):
        def mostrar_sucursales(cursor):
            """Muestra las sucursales disponibles"""
            cursor.execute("SELECT ID, Nombre FROM Sucursales WHERE Estatus = 'Activa'")
            sucursales = cursor.fetchall()
            
            print("\nSucursales disponibles:")
            for id, nombre in sucursales:
                print(f"{id}: {nombre}")
            
            return sucursales

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

                # 1. Solicitar datos básicos del rol
                nombre = input("Nombre del rol (max 25 caracteres): ").strip()
                if len(nombre) > 25:
                    print("Error: El nombre no puede exceder 25 caracteres")
                    exit()

                descripcion = input("Descripción (opcional): ").strip()
                descripcion = None if descripcion == "" else descripcion

                # 2. Mostrar sucursales disponibles (opcional)
                sucursales = mostrar_sucursales(cursor)
                sucursal_id = input("\nSeleccione el ID de la sucursal asociada (deje vacío si no aplica): ").strip()
                
                if sucursal_id:
                    if not sucursal_id.isdigit() or not any(int(sucursal_id) == s[0] for s in sucursales):
                        print("Error: ID de sucursal no válido")
                        exit()
                    sucursal_id = int(sucursal_id)
                else:
                    sucursal_id = None

                # 3. Insertar el nuevo rol
                sentencia = """INSERT INTO Roles (
                    Nombre, Descripcion, Sucursal_ID
                ) VALUES (%s, %s, %s)"""
                
                datos = (nombre, descripcion, sucursal_id)

                cursor.execute(sentencia, datos)
                conexion.commit()
                print("\n✅ Rol registrado correctamente")

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