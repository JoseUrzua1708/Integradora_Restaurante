from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import mysql.connector
from datetime import datetime
from contextlib import closing
import os
from dotenv import load_dotenv
import logging
from datetime import time


###############################################################################
# Cargar variables de entorno
###############################################################################
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

###############################################################################
# Configuración de la base de datos (conexión a la base de datos)
###############################################################################
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Jose1708$'),
    'database': os.getenv('DB_NAME', 'administracion'),
    'pool_name': 'restaurante_pool',
    'pool_size': 5,
    'pool_reset_session': True
}

def get_db_connection():
    """Obtiene una conexión a la base de datos con manejo de errores"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        app.logger.error(f"Database connection error: {err}")
        flash(f"Error de conexión a la base de datos: {err}", "error")
        raise

###############################################################################
# Inicio de la aplicación
###############################################################################

@app.route('/')
def inicio():
    """Página principal del sistema"""
    return render_template('inicio.html')

################################################################################
# Gestión de restaurantes
################################################################################
@app.route('/gestion_restaurante')
def gestion_restaurante():
    """Muestra todos los restaurantes"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Configuracion_Restaurante")
        restaurantes = cursor.fetchall()
        return render_template('Gestion_Restaurante.html', data=restaurantes)
    except Exception as e:
        app.logger.error(f"Error en gestion_restaurante: {str(e)}")
        flash("Error al cargar los restaurantes", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Formulario de restaurante
################################################################################ 

@app.route('/formulario-restaurante', methods=['GET', 'POST'])
def formulario_restaurante():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            datos = {
                'nombre': request.form['Nombre_Restaurante'],
                'direccion': request.form['Direccion'],
                'telefono': request.form['telefono_completo'],  # Usamos el teléfono completo
                'correo': request.form['Correo_Contacto'],
                'apertura': request.form['Horario_Apertura'],
                'cierre': request.form['Horario_Cierre'],
                'moneda': request.form['tipo_moneda'],  # Usamos el código de moneda
                'impuesto': float(request.form['Impuesto']),
                'tiempo_reserva': int(request.form['Tiempo_Reserva_Min']),
                'politica': request.form['Politica_Cancelacion']
            }

            # Validación básica
            if not all(datos.values()):
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for('formulario_restaurante'))

            # Convertir horarios a objetos time para validación
            hora_apertura = time.fromisoformat(datos['apertura'])
            hora_cierre = time.fromisoformat(datos['cierre'])
            
            if hora_apertura >= hora_cierre:
                flash("El horario de cierre debe ser posterior al de apertura", "error")
                return redirect(url_for('formulario_restaurante'))

            # Conexión a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO Configuracion_Restaurante 
                (Nombre_Restaurante, Direccion, Telefono, Correo_Contacto, 
                 Horario_Apertura, Horario_Cierre, Moneda, Impuesto, 
                 Tiempo_Reserva_Min, Politica_Cancelacion)
                VALUES (%(nombre)s, %(direccion)s, %(telefono)s, %(correo)s, 
                        %(apertura)s, %(cierre)s, %(moneda)s, %(impuesto)s, 
                        %(tiempo_reserva)s, %(politica)s)
            """
            cursor.execute(query, datos)
            conn.commit()
            
            flash("Restaurante agregado exitosamente", "success")
            return redirect(url_for('gestion_restaurante'))
            
        except ValueError as e:
            flash(f"Error en los datos proporcionados: {str(e)}", "error")
            return redirect(url_for('formulario_restaurante'))
            
        except Exception as e:
            logging.error(f"Error al insertar restaurante: {str(e)}")
            flash("Error técnico al agregar el restaurante", "error")
            return redirect(url_for('formulario_restaurante'))
            
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()
    
    # Método GET - Mostrar formulario
    return render_template('formulario_restaurante.html')

################################################################################
# Eliminar restaurante
################################################################################

@app.route('/eliminar/<int:id>')
def eliminar_restaurante(id):
    """Elimina un restaurante por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Configuracion_Restaurante WHERE ID = %s", (id,))
        conn.commit()
        flash("Restaurante eliminado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al eliminar restaurante ID {id}: {str(e)}")
        flash("Error al eliminar el restaurante", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_restaurante'))

################################################################################
# Actualizar restaurante
################################################################################

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_restaurante(id):
    """Actualiza un restaurante existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'nombre': request.form['Nombre_Restaurante'],
            'direccion': request.form['Direccion'],
            'telefono': request.form['Telefono'],
            'correo': request.form['Correo_Contacto'],
            'apertura': request.form['Horario_Apertura'],
            'cierre': request.form['Horario_Cierre'],
            'moneda': request.form['Moneda'],
            'impuesto': request.form['Impuesto'],
            'tiempo_reserva': request.form['Tiempo_Reserva_Min'],
            'politica': request.form['Politica_Cancelacion']
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Configuracion_Restaurante SET 
                Nombre_Restaurante = %(nombre)s,
                Direccion = %(direccion)s,
                Telefono = %(telefono)s,
                Correo_Contacto = %(correo)s,
                Horario_Apertura = %(apertura)s,
                Horario_Cierre = %(cierre)s,
                Moneda = %(moneda)s,
                Impuesto = %(impuesto)s,
                Tiempo_Reserva_Min = %(tiempo_reserva)s,
                Politica_Cancelacion = %(politica)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
        conn.commit()
        flash("Restaurante actualizado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al actualizar restaurante ID {id}: {str(e)}")
        flash("Error al actualizar el restaurante", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_restaurante'))

################################################################################
# Gestión de sucursales
################################################################################

@app.route('/formulario_sucursales')
def formulario_sucursales():
    """Muestra el formulario para agregar sucursales"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID, Nombre FROM Ciudades")
        ciudades = cursor.fetchall()
        return render_template('formulario_sucursales.html', ciudades=ciudades)
    except Exception as e:
        app.logger.error(f"Error en formulario_sucursales: {str(e)}")
        flash("Error al cargar el formulario de sucursales", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Gestión de empleados
@app.route('/formulario_empleado')
def formulario_empleado():
    """Muestra el formulario para agregar empleados"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT ID, Nombre FROM Sucursales WHERE Estatus = 'Activa'")
        sucursales = cursor.fetchall()
        
        cursor.execute("SELECT ID, Nombre FROM Roles")
        roles = cursor.fetchall()
        
        return render_template("formulario_empleado.html", 
                            sucursales=sucursales, 
                            roles=roles)
    except Exception as e:
        app.logger.error(f"Error en formulario_empleado: {str(e)}")
        flash("Error al cargar el formulario de empleado", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Gestión de reservaciones
@app.route('/gestion_reservaciones')
def gestion_reservaciones():
    """Muestra la gestión de reservaciones"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Cargar opciones para los selects
        cursor.execute("SELECT ID, CONCAT(Nombre, ' ', Apellido_P) AS Nombre FROM Clientes")
        clientes = cursor.fetchall()

        cursor.execute("SELECT ID, CONCAT(Nombre, ' ', Apellido_P) AS Nombre FROM Empleados")
        empleados = cursor.fetchall()

        cursor.execute("SELECT ID, Numero_Mesa FROM Mesas")
        mesas = cursor.fetchall()

        cursor.execute("SELECT ID, Nombre FROM Eventos")
        eventos = cursor.fetchall()

        cursor.execute("SELECT ID, Nombre FROM Sucursales")
        sucursales = cursor.fetchall()

        # Historial
        cursor.execute("""
            SELECT R.ID, C.Nombre, M.Numero_Mesa, R.Numero_Personas, R.Fecha_Hora 
            FROM Reservaciones R 
            JOIN Clientes C ON R.Cliente_ID = C.ID 
            JOIN Mesas M ON R.Mesa_ID = M.ID
            ORDER BY R.Fecha_Hora DESC
        """)
        reservas_mesas = cursor.fetchall()

        cursor.execute("""
            SELECT E.ID, C.Nombre, EV.Nombre AS Evento, E.Numero_Personas, E.Fecha_Reserva 
            FROM Eventos_Reservaciones E 
            JOIN Clientes C ON E.Cliente_ID = C.ID 
            JOIN Eventos EV ON E.Evento_ID = EV.ID
            ORDER BY E.Fecha_Reserva DESC
        """)
        reservas_eventos = cursor.fetchall()

        return render_template("gestion_reservaciones.html", 
                            clientes=clientes, 
                            empleados=empleados, 
                            mesas=mesas, 
                            eventos=eventos, 
                            sucursales=sucursales, 
                            reservas_mesas=reservas_mesas, 
                            reservas_eventos=reservas_eventos)
    except Exception as e:
        app.logger.error(f"Error en gestion_reservaciones: {str(e)}")
        flash("Error al cargar la gestión de reservaciones", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route('/guardar_reserva', methods=['POST'])
def guardar_reserva():
    """Guarda una nueva reservación"""
    conn = None
    cursor = None
    try:
        tipo = request.form.get('tipo')
        cliente = request.form.get('cliente')
        personas = request.form.get('personas')
        fecha = request.form.get('fecha')
        notas = request.form.get('notas', '')

        if not all([tipo, cliente, personas, fecha]):
            flash("Todos los campos obligatorios deben ser completados", "error")
            return redirect(url_for('gestion_reservaciones'))

        conn = get_db_connection()
        cursor = conn.cursor()

        if tipo == "mesa":
            sucursal = request.form.get('sucursal')
            mesa = request.form.get('mesa')
            empleado = request.form.get('empleado')

            cursor.execute("""
                INSERT INTO Reservaciones 
                (Cliente_ID, Sucursal_ID, Mesa_ID, Fecha_Hora, Numero_Personas, Notas, Empleado_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (cliente, sucursal, mesa, fecha, personas, notas, empleado))
        else:
            evento = request.form.get('evento')
            monto = request.form.get('monto', 0)

            cursor.execute("""
                INSERT INTO Eventos_Reservaciones 
                (Evento_ID, Cliente_ID, Numero_Personas, Monto_Pagado, Notas)
                VALUES (%s, %s, %s, %s, %s)
            """, (evento, cliente, personas, monto, notas))

        conn.commit()
        flash("Reservación guardada exitosamente", "success")
        return redirect(url_for('gestion_reservaciones'))
    except Exception as e:
        app.logger.error(f"Error al guardar reserva: {str(e)}")
        flash("Error al guardar la reservación", "error")
        return redirect(url_for('gestion_reservaciones'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=2001)