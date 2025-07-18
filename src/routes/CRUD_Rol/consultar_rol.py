import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
from datetime import datetime

class Consultar_Rol:
    """Clase para consultar roles con información de sucursales relacionadas"""
    
    BORDER_STYLE = "═" * 100
    HEADER_STYLE = "─" * 100
    
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.ejecutar_consulta()

    def conectar_db(self):
        """Establece conexión segura con la base de datos"""
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Jose1708$",
                database="administracion",
                autocommit=True
            )
            return self.conexion.is_connected()
        except Error as e:
            print(f"\n🔴 ERROR DE CONEXIÓN: {str(e).upper()}")
            return False

    def obtener_metadatos(self):
        """Obtiene información sobre la base de datos y tabla"""
        try:
            self.cursor.execute("SELECT database()")
            db_name = self.cursor.fetchone()["database()"]
            
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total, 
                    MAX(Fecha_Actualizacion) as ultima_actualizacion,
                    COUNT(DISTINCT Sucursal_ID) as sucursales_asignadas
                FROM Roles
            """)
            meta = self.cursor.fetchone()
            
            return {
                "base_datos": db_name,
                "total_registros": meta["total"],
                "ultima_actualizacion": meta["ultima_actualizacion"].strftime("%d/%m/%Y %H:%M") if meta["ultima_actualizacion"] else "Nunca",
                "sucursales_asignadas": meta["sucursales_asignadas"]
            }
        except Error:
            return None

    def formatear_texto(self, texto, max_len=25):
        """Formatea texto largo para visualización"""
        if not texto:
            return "Sin datos"
        texto = texto.strip()
        return (texto[:max_len] + "...") if len(texto) > max_len else texto

    def ejecutar_consulta(self):
        """Ejecuta y muestra la consulta de roles con sucursales"""
        try:
            if not self.conectar_db():
                return

            self.cursor = self.conexion.cursor(dictionary=True)
            meta = self.obtener_metadatos()
            
            # Consulta optimizada con JOIN a Sucursales
            self.cursor.execute("""
                SELECT 
                    r.ID, 
                    r.Nombre, 
                    r.Descripcion,
                    DATE_FORMAT(r.Fecha_Creacion, '%d/%m/%Y') as Fecha_Creacion,
                    DATE_FORMAT(r.Fecha_Actualizacion, '%d/%m/%Y %H:%i') as Fecha_Actualizacion,
                    r.Estatus,
                    r.Sucursal_ID,
                    s.Nombre as Sucursal_Nombre,
                    (SELECT COUNT(*) FROM Usuarios WHERE Rol_ID = r.ID) as Usuarios_Asociados
                FROM Roles r
                LEFT JOIN Sucursales s ON r.Sucursal_ID = s.ID
                ORDER BY 
                    CASE WHEN r.Estatus = 'Activo' THEN 0 ELSE 1 END,
                    r.Nombre
            """)
            
            roles = self.cursor.fetchall()
            
            # Encabezado informativo
            print(f"\n{self.BORDER_STYLE}")
            print(f"🏛️  SISTEMA DE GESTIÓN DE ROLES - RELACIÓN CON SUCURSALES".center(100))
            print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(100))
            print(f"{self.BORDER_STYLE}")
            
            if meta:
                print(f"📦 BASE DE DATOS: {meta['base_datos']}")
                print(f"📊 TOTAL DE ROLES: {meta['total_registros']} | SUCURSALES ASIGNADAS: {meta['sucursales_asignadas']}")
                print(f"🔄 ÚLTIMA ACTUALIZACIÓN: {meta['ultima_actualizacion']}")
                print(f"{self.HEADER_STYLE}")

            if not roles:
                print("\n⚠️ NO SE ENCONTRARON ROLES REGISTRADOS")
                print(f"{self.BORDER_STYLE}\n")
                return
            
            # Preparar datos para visualización
            tabla = []
            for rol in roles:
                sucursal = f"{rol['Sucursal_Nombre']} (ID: {rol['Sucursal_ID']})" if rol['Sucursal_ID'] else "Sin sucursal"
                
                tabla.append([
                    rol["ID"],
                    rol["Nombre"],
                    self.formatear_texto(rol["Descripcion"]),
                    rol["Fecha_Creacion"],
                    rol["Fecha_Actualizacion"] or "Sin cambios",
                    "🟢 ACTIVO" if rol["Estatus"] == "Activo" else "🔴 INACTIVO",
                    sucursal,
                    f"👥 {rol['Usuarios_Asociados']}" if rol['Usuarios_Asociados'] > 0 else "👤 0"
                ])
            
            # Mostrar tabla
            print(tabulate(
                tabla,
                headers=[
                    "ID", "NOMBRE", "DESCRIPCIÓN", 
                    "CREACIÓN", "ACTUALIZACIÓN", 
                    "ESTATUS", "SUCURSAL", "USUARIOS"
                ],
                tablefmt="fancy_grid",
                stralign="center",
                numalign="center"
            ))
            
            # Resumen estadístico
            print(f"{self.HEADER_STYLE}")
            print(f"ℹ️  RESUMEN ESTADÍSTICO:".ljust(30) + 
                  f"Roles activos: {sum(1 for r in roles if r['Estatus'] == 'Activo')}".ljust(30) +
                  f"Roles con sucursal: {sum(1 for r in roles if r['Sucursal_ID'] is not None)}".ljust(30))
            print(f"{self.BORDER_STYLE}\n")
            
        except Error as e:
            print(f"\n🔴 ERROR EN LA CONSULTA: {str(e).upper()}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conexion and self.conexion.is_connected():
                self.conexion.close()
                print("🔷 CONEXIÓN CERRADA CORRECTAMENTE\n")