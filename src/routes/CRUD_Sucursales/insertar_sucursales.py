import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

class Agregar_Sucursal:
    """Clase para agregar sucursales con validación mejorada y manejo de conexión"""
    
    STATUS_VALIDOS = ['Activa', 'Inactiva', 'En Mantenimiento']
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.agregar_sucursal()

    def conectar_db(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                database="administracion",
                autocommit=False
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return True
            return False
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return False

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

    def agregar_sucursal(self):
        """Agrega una nueva sucursal con validación de datos"""
        try:
            if not self.conectar_db():
                return

            print("\n" + "="*50)
            print("   REGISTRO DE NUEVA SUCURSAL   ".center(50))
            print("="*50 + "\n")

            # Obtener y validar todos los datos
            nombre = input("Nombre de la sucursal (max 50 caracteres): ")
            if len(nombre) > 50:
                print("❌ Error: El nombre no puede exceder 50 caracteres")
                return

            direccion = input("Dirección de la sucursal: ")
            if not direccion:
                print("❌ Error: La dirección no puede estar vacía")
                return
            
            telefono = input("Teléfono (10 dígitos): ")
            if not re.match(r'^\d{10}$', telefono):
                print("❌ Error: El teléfono debe tener exactamente 10 dígitos")
                return

            responsable_id = input("ID del responsable (opcional, presione Enter para omitir): ")
            if responsable_id == "":
                responsable_id = None
            elif not responsable_id.isdigit():
                print("❌ Error: El ID del responsable debe ser un número")
                return
            
            horario_apertura = input("Horario de Apertura (HH:MM o HH:MM:SS): ")
            try:
                horario_apertura = self.validar_hora(horario_apertura)
            except ValueError as ve:
                print(f"❌ Error: {ve}")
                return
            
            horario_cierre = input("Horario de Cierre (HH:MM o HH:MM:SS): ")
            try:
                horario_cierre = self.validar_hora(horario_cierre)
            except ValueError as ve:
                print(f"❌ Error: {ve}")
                return
            
            print(f"\nOpciones de estatus: {', '.join(self.STATUS_VALIDOS)}")
            estatus = input("Estatus [Activa]: ").strip().title()
            if estatus == "":
                estatus = "Activa"
            elif estatus not in self.STATUS_VALIDOS:
                print(f"❌ Error: Estatus no válido. Use: {', '.join(self.STATUS_VALIDOS)}")
                return
            
            fecha_apertura = input("Fecha de Apertura (YYYY-MM-DD) [opcional]: ")
            try:
                fecha_apertura = self.validar_fecha(fecha_apertura)
            except ValueError as ve:
                print(f"❌ Error: {ve}")
                return

            # Confirmar antes de insertar
            print("\nResumen de datos a insertar:")
            print(f"Nombre: {nombre}")
            print(f"Dirección: {direccion}")
            print(f"Teléfono: {telefono}")
            print(f"Responsable ID: {responsable_id or 'No asignado'}")
            print(f"Horario: {horario_apertura} - {horario_cierre}")
            print(f"Estatus: {estatus}")
            print(f"Fecha Apertura: {fecha_apertura or 'No especificada'}")
            
            confirmar = input("\n¿Confirmar inserción? (S/N): ").upper()
            if confirmar != 'S':
                print("❌ Inserción cancelada")
                return

            # Insertar datos
            sentencia = """INSERT INTO Sucursales
                  (Nombre, Direccion, Telefono, Responsable_ID, 
                   Horario_Apertura, Horario_Cierre, Estatus, Fecha_Apertura) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                  
            datos = (
                nombre, direccion, telefono, 
                responsable_id, 
                horario_apertura, horario_cierre, 
                estatus, fecha_apertura
            )
            
            self.cursor.execute(sentencia, datos)
            self.connection.commit()
            
            # Obtener ID de la nueva sucursal
            sucursal_id = self.cursor.lastrowid
            print(f"\n✅ Sucursal registrada exitosamente. ID: {sucursal_id}")

        except Error as ex:
            print("\n❌ Error en la base de datos:", ex)
            if self.connection and self.connection.is_connected():
                self.connection.rollback()

        except Exception as e:
            print("\n❌ Error inesperado:", e)
            if self.connection and self.connection.is_connected():
                self.connection.rollback()

        finally:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
                self.connection.close()
                print("🔌 Conexión cerrada")