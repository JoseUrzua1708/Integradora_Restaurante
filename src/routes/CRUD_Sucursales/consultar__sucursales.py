import mysql.connector
from mysql.connector import Error
from tabulate import tabulate  # Necesitarás instalar este paquete: pip install tabulate

class Consultar_Sucursal:
    """Clase para consultar sucursales con presentación elegante"""
    
    def __init__(self):
        self.consultar_sucursales()

    def conectar_db(self):
        """Establece conexión con la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                database="administracion"
            )
            return conexion if conexion.is_connected() else None
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def consultar_sucursales(self):
        """Consulta y muestra las sucursales en formato tabular"""
        conexion = None
        cursor = None
        
        try:
            conexion = self.conectar_db()
            if not conexion:
                return

            cursor = conexion.cursor(dictionary=True)
            
            # Obtener información de la base de datos
            cursor.execute("SELECT database()")
            base_datos = cursor.fetchone()["database()"]
            
            # Consulta principal
            cursor.execute("""
                SELECT 
                    ID, Nombre, Direccion, Telefono, 
                    Responsable_ID, 
                    TIME_FORMAT(Horario_Apertura, '%H:%i') AS Apertura,
                    TIME_FORMAT(Horario_Cierre, '%H:%i') AS Cierre,
                    Estatus, 
                    IFNULL(DATE_FORMAT(Fecha_Apertura, '%d/%m/%Y'), 'No especificada') AS Inauguración,
                    DATE_FORMAT(Fecha_Registro, '%d/%m/%Y %H:%i') AS Registro
                FROM Sucursales
                ORDER BY Nombre
            """)
            
            registros = cursor.fetchall()
            
            # Mostrar encabezado
            print("\n" + "═" * 80)
            print(f"📋 SUCURSALES - BASE DE DATOS: {base_datos}".center(80))
            print("═" * 80)
            print(f"📊 Total de registros: {len(registros)}")
            print("─" * 80)
            
            if not registros:
                print("No hay sucursales registradas")
                return
            
            # Preparar datos para tabla
            headers = [
                "ID", "Nombre", "Dirección", "Teléfono", 
                "Responsable", "Horarios", "Estatus",
                "Inauguración", "Registro"
            ]
            
            tabla_datos = []
            for fila in registros:
                tabla_datos.append([
                    fila["ID"],
                    fila["Nombre"],
                    fila["Direccion"][:30] + "..." if len(fila["Direccion"]) > 30 else fila["Direccion"],
                    fila["Telefono"],
                    fila["Responsable_ID"] or "No asignado",
                    f"{fila['Apertura']} - {fila['Cierre']}",
                    fila["Estatus"],
                    fila["Inauguración"],
                    fila["Registro"]
                ])
            
            # Mostrar tabla
            print(tabulate(tabla_datos, headers=headers, tablefmt="grid"))
            print("═" * 80)
            
        except Error as ex:
            print(f"❌ Error en la base de datos: {ex}")
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
                print("🔌 Conexión cerrada\n")
