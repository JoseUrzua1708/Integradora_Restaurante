import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

class Actualizar_Sucursal:
    """Clase para actualizar sucursales con validación mejorada"""
    
    STATUS_VALIDOS = ['Activa', 'Inactiva', 'En Mantenimiento']
    
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.actualizar_sucursal()

    def conectar_db(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                database="administracion",
                autocommit=False
            )
            return self.conexion.is_connected()
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def validar_telefono(self, telefono):
        """Valida que el teléfono tenga 10 dígitos"""
        if not re.match(r'^\d{10}$', telefono):
            raise ValueError("El teléfono debe tener 10 dígitos")
        return telefono

    def validar_hora(self, hora_str):
        """Valida formatos de hora HH:MM o HH:MM:SS"""
        try:
            hora_str = hora_str.strip().upper()
            
            # Formato 24 horas
            if 'AM' not in hora_str and 'PM' not in hora_str:
                partes = hora_str.split(':')
                if len(partes) == 2:  # Si es HH:MM
                    hora_str += ":00"
                datetime.strptime(hora_str, '%H:%M:%S')
                return hora_str
            
            # Formato 12 horas
            formato = '%I:%M%p' if len(hora_str.split(':')) == 2 else '%I:%M:%S%p'
            hora_obj = datetime.strptime(hora_str, formato)
            return hora_obj.strftime('%H:%M:%S')
            
        except ValueError:
            raise ValueError("Formato de hora no válido. Use HH:MM o HH:MM:SS")

    def validar_fecha(self, fecha_str):
        """Valida formato de fecha YYYY-MM-DD"""
        if not fecha_str.strip():
            return None
            
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Use YYYY-MM-DD")

    def mostrar_sucursales(self):
        """Muestra las sucursales disponibles para actualizar"""
        try:
            self.cursor.execute("SELECT ID, Nombre FROM Sucursales ORDER BY ID")
            sucursales = self.cursor.fetchall()
            
            if not sucursales:
                print("No hay sucursales registradas")
                return False
                
            print("\nSUCURSALES DISPONIBLES:")
            for id, nombre in sucursales:
                print(f"ID: {id} - {nombre}")
            return True
            
        except Error as e:
            print(f"Error al obtener sucursales: {e}")
            return False

    def obtener_datos_actuales(self, sucursal_id):
        """Obtiene los datos actuales de una sucursal"""
        try:
            self.cursor.execute("SELECT * FROM Sucursales WHERE ID = %s", (sucursal_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error al obtener datos: {e}")
            return None

    def actualizar_sucursal(self):
        """Actualiza una sucursal con validación de datos"""
        try:
            if not self.conectar_db():
                return

            self.cursor = self.conexion.cursor(dictionary=True)
            
            # Mostrar sucursales disponibles
            if not self.mostrar_sucursales():
                return

            # Obtener ID de sucursal a actualizar
            sucursal_id = input("\nIngrese el ID de la sucursal a actualizar: ")
            if not sucursal_id.isdigit():
                print("❌ El ID debe ser un número")
                return

            # Obtener datos actuales
            datos_actuales = self.obtener_datos_actuales(sucursal_id)
            if not datos_actuales:
                print("❌ No se encontró la sucursal")
                return

            print("\nDATOS ACTUALES:")
            print(f"1. Nombre: {datos_actuales['Nombre']}")
            print(f"2. Dirección: {datos_actuales['Direccion']}")
            print(f"3. Teléfono: {datos_actuales['Telefono']}")
            print(f"4. Responsable ID: {datos_actuales['Responsable_ID']}")
            print(f"5. Horario Apertura: {datos_actuales['Horario_Apertura']}")
            print(f"6. Horario Cierre: {datos_actuales['Horario_Cierre']}")
            print(f"7. Estatus: {datos_actuales['Estatus']}")
            print(f"8. Fecha Apertura: {datos_actuales['Fecha_Apertura']}")

            # Obtener nuevos datos
            print("\nIngrese los nuevos valores (deje vacío para mantener el actual)")

            nombre = input(f"Nuevo nombre [{datos_actuales['Nombre']}]: ") or datos_actuales['Nombre']
            direccion = input(f"Nueva dirección [{datos_actuales['Direccion']}]: ") or datos_actuales['Direccion']
            
            telefono = datos_actuales['Telefono']
            while True:
                nuevo_tel = input(f"Nuevo teléfono [{telefono}]: ") or telefono
                try:
                    telefono = self.validar_telefono(nuevo_tel)
                    break
                except ValueError as ve:
                    print(f"Error: {ve}")

            responsable_id = input(f"Nuevo ID responsable [{datos_actuales['Responsable_ID']}]: ") or datos_actuales['Responsable_ID']
            
            horario_apertura = datos_actuales['Horario_Apertura']
            while True:
                nuevo_ha = input(f"Nuevo horario apertura [{horario_apertura}]: ") or horario_apertura
                try:
                    horario_apertura = self.validar_hora(nuevo_ha)
                    break
                except ValueError as ve:
                    print(f"Error: {ve}")

            horario_cierre = datos_actuales['Horario_Cierre']
            while True:
                nuevo_hc = input(f"Nuevo horario cierre [{horario_cierre}]: ") or horario_cierre
                try:
                    horario_cierre = self.validar_hora(nuevo_hc)
                    break
                except ValueError as ve:
                    print(f"Error: {ve}")

            estatus = datos_actuales['Estatus']
            while True:
                nuevo_estatus = input(f"Nuevo estatus ({', '.join(self.STATUS_VALIDOS)}) [{estatus}]: ") or estatus
                if nuevo_estatus in self.STATUS_VALIDOS:
                    estatus = nuevo_estatus
                    break
                print(f"Error: Estatus debe ser uno de: {', '.join(self.STATUS_VALIDOS)}")

            fecha_apertura = datos_actuales['Fecha_Apertura']
            while True:
                nueva_fecha = input(f"Nueva fecha apertura (YYYY-MM-DD) [{fecha_apertura}]: ") or fecha_apertura
                try:
                    fecha_apertura = self.validar_fecha(nueva_fecha)
                    break
                except ValueError as ve:
                    print(f"Error: {ve}")

            # Confirmar cambios
            print("\n¿Confirmar actualización?")
            print(f"ID Sucursal: {sucursal_id}")
            print(f"Nombre: {nombre}")
            print(f"Dirección: {direccion}")
            print(f"Teléfono: {telefono}")
            confirmar = input("\n¿Actualizar sucursal? (S/N): ").upper()

            if confirmar != 'S':
                print("❌ Actualización cancelada")
                return

            # Ejecutar actualización
            query = """UPDATE Sucursales SET 
                Nombre = %s, 
                Direccion = %s, 
                Telefono = %s, 
                Responsable_ID = %s, 
                Horario_Apertura = %s, 
                Horario_Cierre = %s, 
                Estatus = %s, 
                Fecha_Apertura = %s 
                WHERE ID = %s"""
                
            params = (
                nombre, direccion, telefono, 
                responsable_id if responsable_id else None,
                horario_apertura, horario_cierre, 
                estatus, fecha_apertura,
                sucursal_id
            )

            self.cursor.execute(query, params)
            self.conexion.commit()
            print("✅ Sucursal actualizada exitosamente")

        except Error as ex:
            print(f"❌ Error en la base de datos: {ex}")
            if self.conexion.is_connected():
                self.conexion.rollback()

        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            if self.conexion.is_connected():
                self.conexion.rollback()

        finally:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'conexion') and self.conexion and self.conexion.is_connected():
                self.conexion.close()
                print("🔌 Conexión cerrada")