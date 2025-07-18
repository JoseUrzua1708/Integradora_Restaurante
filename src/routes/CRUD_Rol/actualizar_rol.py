import mysql.connector
from mysql.connector import Error
from datetime import datetime

class actualizar_rol:
    """Clase para actualizar roles con validación mejorada"""
    
    def __init__(self):
        self.actualizar_rol()

    def actualizar_rol(self):
        """Actualiza un rol en la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                db="administracion"
            )

            if conexion.is_connected():
                print("Actualizando rol...")
                cursor = conexion.cursor()

                # 1. Mostrar roles existentes
                cursor.execute("SELECT ID, Nombre FROM Roles")
                roles = cursor.fetchall()
                print("\nRoles disponibles:")
                for id, nombre in roles:
                    print(f"{id}: {nombre}")

                # 2. Solicitar ID del rol a actualizar
                rol_id = input("\nIntroduce el ID del rol a actualizar: ")
                if not rol_id.isdigit() or not any(int(rol_id) == r[0] for r in roles):
                    print("Error: ID de rol no válido")
                    exit()
                rol_id = int(rol_id)

                # 3. Solicitar nuevos datos
                nuevo_nombre = input("Nuevo nombre del rol (max 25 caracteres): ").strip()
                if len(nuevo_nombre) > 25:
                    print("Error: El nombre no puede exceder 25 caracteres")
                    exit()

                nueva_descripcion = input("Nueva descripción (opcional): ").strip()
                nueva_descripcion = None if nueva_descripcion == "" else nueva_descripcion

                # 4. Actualizar rol en la base de datos
                sentencia = """UPDATE Roles SET Nombre = %s, Descripcion = %s WHERE ID = %s"""
                datos = (nuevo_nombre, nueva_descripcion, rol_id)

                cursor.execute(sentencia, datos)
                conexion.commit()
                print("\n✅ Rol actualizado correctamente")

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