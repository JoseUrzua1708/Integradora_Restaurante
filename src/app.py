from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, abort
import mysql.connector
from datetime import datetime, date
from contextlib import closing
import os
from dotenv import load_dotenv
import logging
from datetime import time
import re
from mysql.connector import Error
import pymysql



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
    'password': os.getenv('DB_PASSWORD', '12345'),
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

@app.route('/formulario_restaurante', methods=['GET', 'POST'])
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
@app.route('/gestion_sucursales')
def gestion_sucursales():
    """Muestra la lista de sucursales"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID, Nombre, Direccion, Telefono, Responsable_ID as Responsable, Estatus FROM Sucursales")
        sucursales = cursor.fetchall()
        return render_template('gestion_sucursales.html', sucursales=sucursales)
    except Exception as e:
        app.logger.error(f"Error en gestion_sucursales: {str(e)}")
        flash("Error al cargar las sucursales", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Formulario de sucursales
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
        
        # Obtener lista de responsables disponibles
        cursor.execute("SELECT ID, Nombre FROM Configuracion_Restaurante WHERE Rol = 'Responsable'")
        responsables = cursor.fetchall()
        
        return render_template('formulario_sucursales.html', 
                            ciudades=ciudades, 
                            responsables=responsables)
    except Exception as e:
        app.logger.error(f"Error en formulario_sucursales: {str(e)}")
        flash("Error al cargar el formulario de sucursales", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route('/guardar_sucursal', methods=['POST'])
def guardar_sucursal():
    """Guarda una nueva sucursal"""
    conn = None
    cursor = None
    try:
        datos = {
            'Nombre': request.form['Nombre'].strip(),
            'Direccion': request.form['Direccion'].strip(),
            'Telefono': request.form['Telefono'].strip(),
            'Responsable_ID': int(request.form['Responsable']),
            'Horario_Apertura': request.form['Horario_Apertura'],
            'Horario_Cierre': request.form['Horario_Cierre'],
            'Estatus': request.form['Estatus'],
            'Fecha_Apertura': request.form['Fecha_Apertura']
        }

        campos_requeridos = ['Nombre', 'Direccion', 'Telefono', 'Responsable_ID',
                            'Horario_Apertura', 'Horario_Cierre', 'Estatus', 'Fecha_Apertura']        
        if not all(datos.get(campo) for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return redirect(url_for('formulario_sucursales'))

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Sucursales (
                Nombre, Direccion, Telefono, Responsable_ID, Horario_Apertura,
                Horario_Cierre, Estatus, Fecha_Apertura
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            datos['Nombre'], datos['Direccion'], datos['Telefono'], datos['Responsable_ID'],
            datos['Horario_Apertura'], datos['Horario_Cierre'], datos['Estatus'], datos['Fecha_Apertura']
        )
        cursor.execute(query, params)
        conn.commit()
        flash("Sucursal registrada exitosamente", "success")
        return redirect(url_for('gestion_sucursales'))
    except ValueError:
        flash("El responsable seleccionado no es válido", "error")
        return redirect(url_for('formulario_sucursales'))
    except Exception as e:
        app.logger.error(f"Error al guardar sucursal: {str(e)}")
        flash("Error al guardar la sucursal", "error")
        return redirect(url_for('formulario_sucursales'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################        
# Eliminar sucursal
################################################################################

@app.route('/eliminar/<int:id>')
def eliminar_sucursal(id):
    """Elimina una sucursal por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Sucursales WHERE ID = %s", (id,))
        conn.commit()
        flash("Sucursal eliminada exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al eliminar sucursal ID {id}: {str(e)}")
        flash("Error al eliminar la sucursal", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_sucursales'))  

################################################################################
# Actualizar sucursal
################################################################################

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_sucursal(id):
    """Actualiza una sucursal existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'nombre': request.form['Nombre'].strip(),
            'direccion': request.form['Direccion'].strip(),
            'telefono': request.form['Telefono'].strip(),
            'responsable_id': int(request.form['Responsable']),
            'horario_apertura': request.form['Horario_Apertura'],
            'horario_cierre': request.form['Horario_Cierre'],
            'estatus': request.form['Estatus'],
            'fecha_apertura': request.form['Fecha_Apertura']
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Sucursales SET 
                Nombre = %(nombre)s,
                Direccion = %(direccion)s,
                Telefono = %(telefono)s,
                Responsable_ID = %(responsable_id)s,
                Horario_Apertura = %(horario_apertura)s,
                Horario_Cierre = %(horario_cierre)s,
                Estatus = %(estatus)s,
                Fecha_Apertura = %(fecha_apertura)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
        conn.commit()
        flash("Sucursal actualizada exitosamente", "success")
    except ValueError:
        flash("El responsable seleccionado no es válido", "error")
    except Exception as e:
        app.logger.error(f"Error al actualizar sucursal ID {id}: {str(e)}")
        flash("Error al actualizar la sucursal", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_sucursales'))

################################################################################
# Gestión de roles
################################################################################
@app.route('/gestion_roles')
def gestion_roles():
    """Muestra la lista de roles"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Obtener roles con información de sucursal (LEFT JOIN por si Sucursal_ID es NULL) 
        cursor.execute("""
            SELECT r.ID, r.Nombre, r.Descripcion, r.Sucursal_ID, r.Fecha_Creacion,
                r.Fecha_Actualizacion, s.Nombre as Sucursal
            FROM Roles r
            LEFT JOIN Sucursales s ON r.Sucursal_ID = s.ID
            ORDER BY r.Fecha_Actualizacion DESC
        """)
        roles = cursor.fetchall()
        return render_template('gestion_roles.html', roles=roles)
    except Exception as e:
        app.logger.error(f"Error en gestion_roles: {str(e)}")
        flash("Error al cargar los roles", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Formulario de roles
################################################################################
@app.route('/formulario_roles')
def formulario_roles():
    """Muestra el formulario para agregar roles"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener la lista de roles
        cursor.execute("SELECT ID, Nombre, Descripcion, Sucursal_ID, Fecha_Creacion, Fecha_Actualizacion FROM Roles")
        roles = cursor.fetchall()
        
        # Obtener la lista de sucursales para el dropdown
        cursor.execute("SELECT ID, Nombre FROM Sucursales")
        sucursales = cursor.fetchall()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        
        return render_template(
            'formulario_roles.html',
            fecha_actual=fecha_actual,
            roles=roles,
            sucursales=sucursales  # Pasar las sucursales a la plantilla
        )
        
    except Exception as e:
        app.logger.error(f"Error en formulario_roles: {str(e)}")
        flash("Error al cargar el formulario de roles", "error")
        return redirect(url_for('inicio'))
        
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Guardar de roles
################################################################################
@app.route('/guardar_rol', methods=['POST'])
def guardar_rol():
    """Guarda un nuevo rol con ID automático""" 
    conn = None
    cursor = None
    try:
        # Obtener y limpiar datos
        datos = {
            'Nombre': request.form['Nombre'].strip(),
            'Descripcion': request.form['Descripcion'].strip(),
            'Sucursal_ID': request.form.get('Sucursal_ID')  # Using get() in case it's missing
        }

        # Validación de campos
        if not all([datos['Nombre'], datos['Descripcion']]):
            flash("Nombre y Descripción son campos obligatorios", "error")
            return redirect(url_for('formulario_roles'))
            
        if len(datos['Nombre']) > 25:
            flash("El nombre del rol no puede superar los 25 caracteres", "error")
            return redirect(url_for('formulario_roles'))
            
        # Validar caracteres permitidos en el nombre
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$', datos['Nombre']):
            flash("El nombre solo puede contener letras, números y espacios", "error")
            return redirect(url_for('formulario_roles'))

        # Validate Sucursal_ID is provided and is a number
        if not datos['Sucursal_ID'] or not datos['Sucursal_ID'].isdigit():
            flash("Debe seleccionar una sucursal válida", "error")
            return redirect(url_for('formulario_roles'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # seleccionar la sucursal para el rol
        cursor.execute("SELECT Nombre FROM Sucursales WHERE ID = %s", (datos['Sucursal_ID'],))

        sucursal = cursor.fetchone()
        if not sucursal:
            flash("La sucursal seleccionada no existe", "error")
            return redirect(url_for('formulario_roles'))
        datos['Sucursal_ID'] = int(datos['Sucursal_ID'])  # Convert to integer for SQL
        datos['Sucursal'] = sucursal[0]  # Store the name of the selected branch
        # Insertar el nuevo rol en la base de datos
        
        try:
            query = """INSERT INTO Roles (
                Nombre, Descripcion, Sucursal_ID
                ) VALUES (%s, %s, %s)
            """
            cursor.execute(query, (
                datos['Nombre'], 
                datos['Descripcion'],
                datos['Sucursal_ID']
            ))
            
            # Obtener el ID generado automáticamente
            nuevo_id = cursor.lastrowid
            
            conn.commit()
            flash(f"Rol registrado exitosamente con ID: {nuevo_id}", "success")
            return redirect(url_for('gestion_roles'))
            
        except pymysql.err.IntegrityError as e:
            conn.rollback()
            if 'Duplicate entry' in str(e):
                flash("Ya existe un rol con ese nombre", "error")
            elif 'foreign key constraint fails' in str(e):
                flash("La sucursal seleccionada no existe", "error")
            else:
                flash("Error de base de datos al guardar el rol", "error")
            return redirect(url_for('formulario_roles'))
            
    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al guardar rol: {str(e)}", exc_info=True)
        flash("Error inesperado al procesar la solicitud", "error")
        return redirect(url_for('formulario_roles'))
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Eliminar rol
################################################################################

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_rol(id):
    """Elimina un rol por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Roles WHERE ID = %s", (id,))
        conn.commit()
        flash("Rol eliminado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al eliminar rol ID {id}: {str(e)}")
        flash("Error al eliminar el rol", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_roles'))

################################################################################
# actualizar rol
################################################################################
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_rol(id):
    """Actualiza un rol existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'Nombre': request.form['Nombre'].strip(),
            'Descripcion': request.form['Descripcion'].strip(),
            'Sucursal_ID': request.form.get('Sucursal_ID')  # Using get() in case it's missing
        }

        # Validación de campos
        if not all([datos['Nombre'], datos['Descripcion']]):
            flash("Nombre y Descripción son campos obligatorios", "error")
            return redirect(url_for('formulario_roles'))

        if len(datos['Nombre']) > 25:
            flash("El nombre del rol no puede superar los 25 caracteres", "error")
            return redirect(url_for('formulario_roles'))

        # Validar caracteres permitidos en el nombre
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$', datos['Nombre']):
            flash("El nombre solo puede contener letras, números y espacios", "error")
            return redirect(url_for('formulario_roles'))

        # Validate Sucursal_ID is provided and is a number
        if not datos['Sucursal_ID'] or not datos['Sucursal_ID'].isdigit():
            flash("Debe seleccionar una sucursal válida", "error")
            return redirect(url_for('formulario_roles'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # seleccionar la sucursal para el rol
        cursor.execute("SELECT Nombre FROM Sucursales WHERE ID = %s", (datos['Sucursal_ID'],))

        sucursal = cursor.fetchone()
        if not sucursal:
            flash("La sucursal seleccionada no existe", "error")
            return redirect(url_for('formulario_roles'))
        
        datos['Sucursal_ID'] = int(datos['Sucursal_ID'])  # Convert to integer for SQL
        datos['Sucursal'] = sucursal[0]  # Store the name of the selected branch
        
        # Actualizar el rol en la base de datos
        query = """
            UPDATE Roles SET 
                Nombre = %s, 
                Descripcion = %s, 
                Sucursal_ID = %s 
            WHERE ID = %s
        """
        
        cursor.execute(query, (
            datos['Nombre'], 
            datos['Descripcion'],
            datos['Sucursal_ID'],
            datos['id']
        ))
        conn.commit()
        flash("Rol actualizado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al actualizar rol ID {id}: {str(e)}")
        flash("Error al actualizar el rol", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_roles'))

################################################################################
# Gestión de empleados---no quitar---
################################################################################
@app.route('/gestion_empleados')
def gestion_empleados():
    """Muestra la lista completa de empleados sin paginación ni búsqueda"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT e.*, r.Nombre AS Rol_Nombre, s.Nombre AS Sucursal_Nombre
            FROM Empleados e
            LEFT JOIN Roles r ON e.Rol_ID = r.ID
            LEFT JOIN Sucursales s ON e.Sucursal_ID = s.ID
            ORDER BY e.Fecha_Registro DESC
        """
        cursor.execute(query)
        empleados = cursor.fetchall()

        return render_template('gestion_empleados.html', empleados=empleados)

    except Exception as e:
        app.logger.error(f"Error en gestion_empleados: {e}")
        flash("Error al cargar los empleados", "error")
        return redirect(url_for('inicio'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


################################################################################
# Formulario de empleados ----no quitar-----
################################################################################
@app.route('/formulario_empleado/<int:id>', methods=['GET'])
@app.route('/formulario_empleado', methods=['GET'])
def formulario_empleado(id=None):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        empleado = None
        if id:
            cursor.execute("SELECT * FROM Empleados WHERE ID = %s", (id,))
            empleado = cursor.fetchone()
            if not empleado:
                flash("Empleado no encontrado", "error")
                return redirect(url_for('gestion_empleados'))

        # Obtener sucursales activas
        cursor.execute("SELECT ID, Nombre FROM sucursales WHERE Estatus = 'Activa'")
        sucursales = cursor.fetchall()

        # Obtener todos los roles 
        cursor.execute("SELECT ID, Nombre FROM Roles")
        roles = cursor.fetchall()

        return render_template(
            'formulario_empleado.html',
            empleado=empleado,
            generos=['Masculino', 'Femenino', 'Otro', 'Prefiero no decir'],
            estatus_options=['Activo', 'Inactivo', 'Suspendido'],
            tipos_contrato=['Tiempo completo', 'Medio tiempo', 'Temporal', 'Indefinido'],
            sucursales=sucursales,
            roles=roles
        )

    except Exception as e:
        app.logger.error(f"Error en formulario_empleado: {e}")
        flash("Error al cargar el formulario", "error")
        return redirect(url_for('gestion_empleados'))

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


################################################################################
# Cambiar estado del empleado
################################################################################
@app.route('/cambiar_estado_empleado/<int:id>/<string:estado>')
def cambiar_estado_empleado(id, estado):
    """Cambia el estado de un empleado"""
    conn = None
    cursor = None
    try:
        if estado not in ['Activo', 'Inactivo', 'Suspendido']:
            flash("Estado no válido", "error")
            return redirect(url_for('gestion_empleados'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar existencia
        cursor.execute("SELECT ID FROM Empleados WHERE ID = %s", (id,))
        if not cursor.fetchone():
            flash("Empleado no encontrado", "error")
            return redirect(url_for('gestion_empleados'))

        cursor.execute(
            "UPDATE Empleados SET Estatus = %s WHERE ID = %s",
            (estado, id)
        )
        conn.commit()

        flash(f"Estado cambiado a {estado}", "success")
        return redirect(url_for('gestion_empleados'))

    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al cambiar estado del empleado ID {id}: {str(e)}")
        flash("Error al cambiar estado del empleado", "error")
        return redirect(url_for('gestion_empleados'))

    finally:
        if cursor: cursor.close()
        if conn: conn.close()




@app.route('/guardar_empleado', methods=['POST'])
def guardar_empleado():
    conn = None
    cursor = None
    try:
        datos = {
            'id': request.form.get('id'),
            'nombre': request.form['nombre'].strip(),
            'apellido_p': request.form['apellido_p'].strip(),
            'apellido_m': request.form.get('apellido_m', '').strip(),
            'correo': request.form['correo'].strip().lower(),
            'telefono': request.form.get('telefono', '').strip(),
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'genero': request.form['genero'],
            'rfc': request.form.get('rfc', '').strip().upper(),
            'curp': request.form.get('curp', '').strip().upper(),
            'direccion': request.form.get('direccion', '').strip(),
            'estatus': request.form.get('estatus', 'Activo'),
            'salario': request.form.get('salario'),
            'tipo_contrato': request.form.get('tipo_contrato'),
            'fecha_contratacion': request.form.get('fecha_contratacion'),
            'rol_id': request.form.get('rol_id'),
            'sucursal_id': request.form.get('sucursal_id'),
        }

        errors = []
        if len(datos['nombre']) > 25:
            errors.append("Nombre no puede exceder 25 caracteres")
        if not datos['correo']:
            errors.append("Correo electrónico es obligatorio")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", datos['correo']):
            errors.append("Correo electrónico no es válido")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for('formulario_empleado', id=datos['id']))

        conn = get_db_connection()
        cursor = conn.cursor()

        if datos['id']:  # Actualización
            cursor.execute(
                "SELECT ID FROM Empleados WHERE Correo = %s AND ID != %s",
                (datos['correo'], datos['id'])
            )
            if cursor.fetchone():
                flash("El correo ya está registrado", "error")
                return redirect(url_for('formulario_empleado', id=datos['id']))

            query = """
                UPDATE Empleados SET
                    Nombre = %s, Apellido_P = %s, Apellido_M = %s, Correo = %s, Telefono = %s,
                    Fecha_Nacimiento = %s, Genero = %s, RFC = %s, CURP = %s, Direccion = %s,
                    Estatus = %s, Salario = %s, Tipo_Contrato = %s, Fecha_Contratacion = %s,
                    Rol_ID = %s, Sucursal_ID = %s, Ultima_Actualizacion = NOW()
                WHERE ID = %s
            """
            cursor.execute(query, (
                datos['nombre'], datos['apellido_p'], datos['apellido_m'],
                datos['correo'], datos['telefono'], datos['fecha_nacimiento'],
                datos['genero'], datos['rfc'], datos['curp'], datos['direccion'],
                datos['estatus'], datos['salario'], datos['tipo_contrato'],
                datos['fecha_contratacion'], datos['rol_id'], datos['sucursal_id'], datos['id']
            ))
            mensaje = "Empleado actualizado exitosamente"
        else:  # Inserción
            cursor.execute("SELECT ID FROM Empleados WHERE Correo = %s", (datos['correo'],))
            if cursor.fetchone():
                flash("El correo ya está registrado", "error")
                return redirect(url_for('formulario_empleado'))

            query = """
                INSERT INTO Empleados (
                    Nombre, Apellido_P, Apellido_M, Correo, Telefono, Fecha_Nacimiento, Genero,
                    RFC, CURP, Direccion, Estatus, Salario, Tipo_Contrato, Fecha_Contratacion,
                    Rol_ID, Sucursal_ID, Fecha_Registro
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (
                datos['nombre'], datos['apellido_p'], datos['apellido_m'],
                datos['correo'], datos['telefono'], datos['fecha_nacimiento'],
                datos['genero'], datos['rfc'], datos['curp'], datos['direccion'],
                datos['estatus'], datos['salario'], datos['tipo_contrato'],
                datos['fecha_contratacion'], datos['rol_id'], datos['sucursal_id']
            ))
            mensaje = "Empleado registrado exitosamente"

        conn.commit()
        flash(mensaje, "success")
        return redirect(url_for('gestion_empleados'))

    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al guardar empleado: {str(e)}")
        flash("Error técnico al guardar el empleado", "error")
        return redirect(url_for('formulario_empleado', id=request.form.get('id')))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()




################################################################################
# eliminar empleado
################################################################################

@app.route('/eliminar_empleado/<int:id>')
def eliminar_empleado(id):
    """Elimina un empleado"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar existencia
        cursor.execute("SELECT ID FROM Empleados WHERE ID = %s", (id,))
        if not cursor.fetchone():
            flash("Empleado no encontrado", "error")
            return redirect(url_for('gestion_empleados'))
        
        cursor.execute("DELETE FROM Empleados WHERE ID = %s", (id,))
        conn.commit()
        
        flash("Empleado eliminado", "success")
        return redirect(url_for('gestion_empleados'))
    
    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al eliminar empleado: {str(e)}")
        flash("Error al eliminar empleado", "error")
        return redirect(url_for('gestion_empleados'))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()




################################################################################
# gestion de proveedores
################################################################################
@app.route('/gestion_proveedores')
def gestion_proveedores():
    """Muestra la lista de proveedores"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()
        return render_template('gestion_proveedores.html', proveedores=proveedores)
    except Error as e:
        app.logger.error(f"Error en gestion_proveedores: {e}")
        flash("Error al cargar los proveedores", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Formulario de proveedores
################################################################################

@app.route('/formulario_proveedor')
def formulario_proveedor():
    """Muestra el formulario para agregar un nuevo proveedor"""
    tipos_proveedor = [
        'Carnes y Aves', 'Pescados y Mariscos', 'Frutas y Verduras',
        'Lácteos y Huevos', 'Panadería y Repostería', 'Alimentos Secos y Enlatados',
        'Especias y Condimentos', 'Aceites y Vinagres', 'Vinos y Licores',
        'Cervezas', 'Bebidas no Alcohólicas', 'Café y Té', 'Equipo de Cocina',
        'Maquinaria para Restaurante', 'Mobiliario', 'Vajilla y Cristalería',
        'Servicios de Limpieza', 'Servicios de Seguridad', 'Menaje Desechable'
    ]
    return render_template('formulario_proveedor.html', tipos_proveedor=tipos_proveedor)



@app.route('/guardar_proveedor', methods=['POST'])
def guardar_proveedor():
    """Procesa el formulario y guarda el nuevo proveedor"""
    conn = None
    cursor = None
    try:
        # Obtener datos del formulario
        datos = {
            'Nombre_Empresa': request.form['Nombre_Empresa'].strip().upper(),
            'Contacto_Principal': request.form['Contacto_Principal'].strip(),
            'Telefono': request.form['Telefono'].strip(),
            'Correo_Electronico': request.form['Correo_Electronico'].strip().lower(),
            'Direccion': request.form['Direccion'].strip(),
            'Tipo_Proveedor': request.form['Tipo_Proveedor'],
            'RFC': request.form.get('RFC', '').strip().upper(),
            'Plazo_Entrega': request.form.get('Plazo_Entrega', '7'),
            'Terminos_Pago': request.form.get('Terminos_Pago', '30 días').strip(),
            'Cuenta_Bancaria': request.form.get('Cuenta_Bancaria', '').strip(),
            'Banco': request.form.get('Banco', '').strip(),
            'Estatus': request.form.get('Estatus', 'Activo'),
            'Notas': request.form.get('Notas', '').strip(),
            'Fecha_Registro': request.form.get('Fecha_Registro', '')
        }

        # Validación de campos obligatorios
        campos_requeridos = ['Nombre_Empresa', 'Contacto_Principal', 'Telefono', 
                            'Correo_Electronico', 'Direccion', 'Tipo_Proveedor']
        if not all(datos[campo] for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return render_template('formulario_proveedor.html', datos=datos, tipos_proveedor=tipos_proveedor)

        # Conexión y consulta SQL
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO Proveedores (
                Nombre_Empresa,
                Contacto_Principal,
                Telefono,
                Correo_Electronico,
                Direccion,
                Tipo_Proveedor,
                RFC,
                Plazo_Entrega,
                Terminos_Pago,
                Cuenta_Bancaria,
                Banco,
                Estatus,
                Notas,
                Fecha_Creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """

        params = (
            datos['Nombre_Empresa'],
            datos['Contacto_Principal'],
            datos['Telefono'],
            datos['Correo_Electronico'],
            datos['Direccion'],
            datos['Tipo_Proveedor'],
            datos['RFC'],
            datos['Plazo_Entrega'],
            datos['Terminos_Pago'],
            datos['Cuenta_Bancaria'],
            datos['Banco'],
            datos['Estatus'],
            datos['Notas']
        )


        
        cursor.execute(query, params)
        conn.commit()
        
        flash("Proveedor registrado exitosamente", "success")
        return redirect(url_for('gestion_proveedores'))
        
    except Error as e:
        if conn: conn.rollback()
        flash(f"Error de base de datos: {e.msg}", "error")
        app.logger.error(f"Error SQL: {e}")
        # Recargar tipos de proveedor para mostrar el formulario nuevamente
        tipos_proveedor = [
            'Carnes y Aves', 'Pescados y Mariscos', 'Frutas y Verduras',
            'Lácteos y Huevos', 'Panadería y Repostería', 'Alimentos Secos y Enlatados',
            'Especias y Condimentos', 'Aceites y Vinagres', 'Vinos y Licores',
            'Cervezas', 'Bebidas no Alcohólicas', 'Café y Té', 'Equipo de Cocina',
            'Maquinaria para Restaurante', 'Mobiliario', 'Vajilla y Cristalería',
            'Servicios de Limpieza', 'Servicios de Seguridad', 'Menaje Desechable'
        ]        
        return render_template('formulario_proveedor.html', datos=request.form, tipos_proveedor=tipos_proveedor)
        
    except Exception as e:
        if conn: conn.rollback()
        flash("Error inesperado al registrar el proveedor", "error")
        app.logger.error(f"Error en guardar_proveedor: {str(e)}")
        return render_template('formulario_proveedor.html', datos=request.form, tipos_proveedor=tipos_proveedor)
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Eliminar proveedor
################################################################################
@app.route('/eliminar/<int:id>')
def eliminar_proveedor(id):
    """Elimina un proveedor por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Proveedores WHERE ID = %s", (id,))
        conn.commit()
        flash("Proveedor eliminado exitosamente", "success")
    except Error as e:
        app.logger.error(f"Error al eliminar proveedor ID {id}: {str(e)}")
        flash("Error al eliminar el proveedor", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_proveedores'))

################################################################################
# Actualizar proveedor
################################################################################
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_proveedor(id):
    """Actualiza un proveedor existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'nombre_empresa': request.form['Nombre_Empresa'].strip().upper(),
            'contacto_principal': request.form['Contacto_Principal'].strip(),
            'telefono': request.form['Telefono'].strip(),
            'correo_electronico': request.form['Correo_Electronico'].strip().lower(),
            'direccion': request.form['Direccion'].strip(),
            'tipo_proveedor': request.form['Tipo_Proveedor'],
            'rfc': request.form.get('RFC', '').strip().upper(),
            'plazo_entrega': request.form.get('Plazo_Entrega', '7'),
            'terminos_pago': request.form.get('Terminos_Pago', '30 días').strip(),
            'cuenta_bancaria': request.form.get('Cuenta_Bancaria', '').strip(),
            'banco': request.form.get('Banco', '').strip(),
            'estatus': request.form.get('Estatus', 'Activo'),
            'notas': request.form.get('Notas', '').strip(),
            'fecha_registro': request.form.get('Fecha_Registro', '')
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Proveedores SET 
                Nombre_Empresa = %(nombre_empresa)s,
                Contacto_Principal = %(contacto_principal)s,
                Telefono = %(telefono)s,
                Correo_Electronico = %(correo_electronico)s,
                Direccion = %(direccion)s,
                Tipo_Proveedor = %(tipo_proveedor)s,
                RFC = %(rfc)s,
                Plazo_Entrega = %(plazo_entrega)s,
                Terminos_Pago = %(terminos_pago)s,
                Cuenta_Bancaria = %(cuenta_bancaria)s,
                Banco = %(banco)s,
                Estatus = %(estatus)s,
                Notas = %(notas)s,
                Fecha_Creacion = %(fecha_registro)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
        conn.commit()
        flash("Proveedor actualizado exitosamente", "success")
    except Error as e:
        app.logger.error(f"Error al actualizar proveedor ID {id}: {str(e)}")
        flash("Error al actualizar el proveedor", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_proveedores'))

################################################################################
# Gesión de inventario
################################################################################
@app.route('/gestion_inventario')
def gestion_inventario():
    """Muestra la lista de inventario"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Inventario")
        inventario = cursor.fetchall()
        return render_template('gestion_inventario.html', inventario=inventario)
    except Error as e:
        app.logger.error(f"Error en gestion_inventario: {e}")
        flash("Error al cargar el inventario", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Formulario de inventario
################################################################################

@app.route('/formulario_inventario')
def formulario_inventario():
    """Muestra el formulario para agregar un nuevo proveedor"""
    tipos_proveedor = [
        'Carnes y Aves', 'Pescados y Mariscos', 'Frutas y Verduras',
        'Lácteos y Huevos', 'Panadería y Repostería', 'Alimentos Secos y Enlatados',
        'Especias y Condimentos', 'Aceites y Vinagres', 'Vinos y Licores',
        'Cervezas', 'Bebidas no Alcohólicas', 'Café y Té', 'Equipo de Cocina',
        'Maquinaria para Restaurante', 'Mobiliario', 'Vajilla y Cristalería',
        'Servicios de Limpieza', 'Servicios de Seguridad', 'Menaje Desechable'
    ]
    return render_template('formulario_inventario.html', tipos_proveedor=tipos_proveedor)

@app.route('/guardar_inventario', methods=['POST'])
def guardar_inventario():
    """Procesa el formulario y guarda el nuevo proveedor"""
    conn = None
    cursor = None
    try:
        # Obtener datos del formulario
        datos = {
            'Nombre': request.form['Nombre'].strip(),
            'Cantidad': request.form['Cantidad'],
            'Unidad': request.form['Unidad'].strip(),
            'Precio': request.form['Precio'],
            'Tipo': request.form['Tipo'].strip(),
            'Estatus': request.form['Estatus'].strip(),
            'Notas': request.form['Notas'].strip(),
            'Fecha_Registro': request.form['Fecha_Registro'].strip()
        }

        # Validación de campos obligatorios
        campos_requeridos = ['Nombre', 'Cantidad', 'Unidad', 'Precio', 'Tipo', 'Estatus', 'Notas', 'Fecha_Registro']
        if not all(datos[campo] for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return render_template('formulario_inventario.html', datos=datos, tipos_proveedor=tipos_proveedor)

        # Conexión y consulta SQL
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO Inventario (
                Nombre,
                Cantidad,
                Unidad,
                Precio,
                Tipo,
                Estatus,
                Notas,
                Fecha_Creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """

        params = (
            datos['Nombre'],
            datos['Cantidad'],
            datos['Unidad'],
            datos['Precio'],
            datos['Tipo'],
            datos['Estatus'],
            datos['Notas']
        )


        
        cursor.execute(query, params)
        conn.commit()
        
        flash("Inventario registrado exitosamente", "success")
        return redirect(url_for('gestion_inventario'))        
        
    except Error as e:
        if conn: conn.rollback()
        flash(f"Error de base de datos: {e.msg}", "error")
        app.logger.error(f"Error SQL: {e}")
        # Recargar tipos de proveedor para mostrar el formulario nuevamente
        tipos_proveedor = [
            'Carnes y Aves', 'Pescados y Mariscos', 'Frutas y Verduras',
            'Lácteos y Huevos', 'Panadería y Repostería', 'Alimentos Secos y Enlatados',
            'Especias y Condimentos', 'Aceites y Vinagres', 'Vinos y Licores',
            'Cervezas', 'Bebidas no Alcohólicas', 'Café y Té', 'Equipo de Cocina',
            'Maquinaria para Restaurante', 'Mobiliario', 'Vajilla y Cristalería',
            'Servicios de Limpieza', 'Servicios de Seguridad', 'Menaje Desechable'
        ]        
        return render_template('formulario_inventario.html', datos=request.form, tipos_proveedor=tipos_proveedor)
        
    except Exception as e:
        if conn: conn.rollback()
        flash("Error inesperado al registrar el inventario", "error")
        app.logger.error(f"Error en guardar_inventario: {str(e)}")
        return render_template('formulario_inventario.html', datos=request.form, tipos_proveedor=tipos_proveedor)
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Eliminar inventario
################################################################################
@app.route('/eliminar/<int:id>')
def eliminar_inventario(id):
    """Elimina un inventario por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Inventario WHERE ID = %s", (id,))
        conn.commit()
        flash("Inventario eliminado exitosamente", "success")
    except Error as e:
        app.logger.error(f"Error al eliminar inventario ID {id}: {str(e)}")
        flash("Error al eliminar el inventario", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_inventario'))

################################################################################
# Actualizar inventario
################################################################################
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_inventario(id):
    """Actualiza un inventario existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'nombre': request.form['Nombre'].strip(),
            'cantidad': request.form['Cantidad'],
            'unidad': request.form['Unidad'].strip(),
            'precio': request.form['Precio'],
            'tipo': request.form['Tipo'].strip(),
            'estatus': request.form['Estatus'].strip(),
            'notas': request.form['Notas'].strip(),
            'fecha_registro': request.form['Fecha_Registro'].strip()
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Inventario SET 
                Nombre = %(nombre)s,
                Cantidad = %(cantidad)s,
                Unidad = %(unidad)s,
                Precio = %(precio)s,
                Tipo = %(tipo)s,
                Estatus = %(estatus)s,
                Notas = %(notas)s,
                Fecha_Creacion = %(fecha_registro)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
        conn.commit()
        flash("Inventario actualizado exitosamente", "success")
    except Error as e:
        app.logger.error(f"Error al actualizar inventario ID {id}: {str(e)}")
        flash("Error al actualizar el inventario", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_inventario'))

################################################################################
# Gestión de reservaciones
################################################################################
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
            SELECT R.ID, CONCAT(C.Nombre, ' ', C.Apellido_P) AS Cliente, M.Numero_Mesa, R.Numero_Personas, R.Fecha_Hora 
            FROM Reservaciones R 
            JOIN Clientes C ON R.Cliente_ID = C.ID 
            JOIN Mesas M ON R.Mesa_ID = M.ID
            ORDER BY R.Fecha_Hora DESC
        """)
        reservas_mesas = cursor.fetchall()

        cursor.execute("""
            SELECT E.ID, CONCAT(C.Nombre, ' ', C.Apellido_P) AS Cliente, EV.Nombre AS Evento, E.Numero_Personas, E.Fecha_Reserva 
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
        print(f"Error al cargar gestión de reservaciones: {e}")
        flash("Error al cargar la gestión de reservaciones. Inténtalo más tarde.", "error")
        # Aquí cargamos plantilla principal con listas vacías para evitar error
        return render_template("gestion_reservaciones.html", 
            clientes=[],
            empleados=[],
            mesas=[],
            eventos=[],
            sucursales=[],
            reservas_mesas=[],
            reservas_eventos=[])
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

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

################################################################################
# Gestión de Clientes
################################################################################
@app.route('/gestion_clientes')
def gestion_clientes():
    """Muestra la lista de clientes con paginación y búsqueda"""
    conn = None
    cursor = None
    try:
        # Obtener parámetros
        page = request.args.get('page', 1, type=int)
        per_page = 10
        search_term = request.args.get('search', '').strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Consulta con búsqueda
        query = """
            SELECT * FROM Clientes
            WHERE Nombre LIKE %s OR Apellido_P LIKE %s OR Correo LIKE %s
            ORDER BY Fecha_Registro DESC
            LIMIT %s OFFSET %s
        """
        search_pattern = f"%{search_term}%"
        offset = (page - 1) * per_page
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, per_page, offset))
        clientes = cursor.fetchall()

        # Contar total
        count_query = """
            SELECT COUNT(*) as total 
            FROM Clientes
            WHERE Nombre LIKE %s OR Apellido_P LIKE %s OR Correo LIKE %s
        """
        cursor.execute(count_query, (search_pattern, search_pattern, search_pattern))
        total = cursor.fetchone()['total']

        return render_template(
            'gestion_clientes.html',
            clientes=clientes,
            page=page,
            per_page=per_page,
            total=total,
            search_term=search_term
        )

    except Exception as e:
        app.logger.error(f"Error en gestion_clientes: {e}")
        flash("Error al cargar los clientes", "error")
        return redirect(url_for('inicio'))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Formulario de clientes
################################################################################
@app.route('/formulario_cliente/<int:id>', methods=['GET'])
@app.route('/formulario_cliente', methods=['GET'])
def formulario_cliente(id=None):
    """Muestra el formulario para agregar o editar un cliente"""
    conn = None
    cursor = None
    try:
        cliente = None
        if id:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes WHERE ID = %s", (id,))
            cliente = cursor.fetchone()
            if not cliente:
                flash("Cliente no encontrado", "error")
                return redirect(url_for('gestion_clientes'))

        return render_template(
            'formulario_cliente.html',
            cliente=cliente,
            generos=['Masculino', 'Femenino', 'Otro', 'Prefiero no decir'],
            estatus_options=['Activo', 'Inactivo', 'Bloqueado']
        )

    except Exception as e:
        app.logger.error(f"Error en formulario_cliente: {e}")
        flash("Error al cargar el formulario", "error")
        return redirect(url_for('gestion_clientes'))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Guardar cliente
################################################################################
@app.route('/guardar_cliente', methods=['POST'])
def guardar_cliente():
    conn = None
    cursor = None
    try:
        # Obtener datos del formulario
        datos = {
            'id': request.form.get('id'),
            'nombre': request.form['nombre'].strip(),
            'apellido_p': request.form['apellido_p'].strip(),
            'apellido_m': request.form.get('apellido_m', '').strip(),
            'correo': request.form['correo'].strip().lower(),
            'telefono': request.form.get('telefono', '').strip(),
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'genero': request.form['genero'],
            'preferencias': request.form.get('preferencias', ''),
            'restricciones': request.form.get('restricciones', ''),
            'estatus': request.form.get('estatus', 'Activo')
        }

        # Validaciones
        errors = []
        if len(datos['nombre']) > 25:
            errors.append("Nombre no puede exceder 25 caracteres")
        if len(datos['apellido_p']) > 20:
            errors.append("Apellido paterno no puede exceder 20 caracteres")
        if not datos['fecha_nacimiento']:
            errors.append("Fecha de nacimiento es obligatoria")
        if not datos['correo']:
            errors.append("Correo electrónico es obligatorio")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", datos['correo']):
            errors.append("Correo electrónico no es válido")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for('formulario_cliente', id=datos['id']))

        conn = get_db_connection()
        cursor = conn.cursor()

        if datos['id']:  # Actualización
            # Verificar correo único
            cursor.execute(
                "SELECT ID FROM Clientes WHERE Correo = %s AND ID != %s",
                (datos['correo'], datos['id'])
            )
            if cursor.fetchone():
                flash("El correo ya está registrado", "error")
                return redirect(url_for('formulario_cliente', id=datos['id']))

            query = """
                UPDATE Clientes SET
                    Nombre = %s,
                    Apellido_P = %s,
                    Apellido_M = %s,
                    Correo = %s,
                    Telefono = %s,
                    Fecha_Nacimiento = %s,
                    Genero = %s,
                    Preferencias = %s,
                    Restricciones_Alimenticias = %s,
                    Estatus = %s,
                    Fecha_Ultima_Actualizacion = NOW()
                WHERE ID = %s
            """
            cursor.execute(query, (
                datos['nombre'], datos['apellido_p'], datos['apellido_m'],
                datos['correo'], datos['telefono'], datos['fecha_nacimiento'],
                datos['genero'], datos['preferencias'], datos['restricciones'],
                datos['estatus'], datos['id']
            ))
            mensaje = "Cliente actualizado exitosamente"
        else:  # Inserción
            # Verificar correo único
            cursor.execute("SELECT ID FROM Clientes WHERE Correo = %s", (datos['correo'],))
            if cursor.fetchone():
                flash("El correo ya está registrado", "error")
                return redirect(url_for('formulario_cliente'))

            query = """
                INSERT INTO Clientes (
                    Nombre, Apellido_P, Apellido_M, Correo, Telefono, 
                    Fecha_Nacimiento, Genero, Preferencias, 
                    Restricciones_Alimenticias, Estatus
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                datos['nombre'], datos['apellido_p'], datos['apellido_m'],
                datos['correo'], datos['telefono'], datos['fecha_nacimiento'],
                datos['genero'], datos['preferencias'], datos['restricciones'],
                datos['estatus']
            ))
            mensaje = "Cliente registrado exitosamente"

        conn.commit()
        flash(mensaje, "success")
        return redirect(url_for('gestion_clientes'))

    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al guardar cliente: {str(e)}")
        flash("Error técnico al guardar el cliente", "error")
        return redirect(url_for('formulario_cliente', id=request.form.get('id')))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Cambiar estado del cliente                                               }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
################################################################################
@app.route('/cambiar_estado/<int:id>/<string:estado>')
def cambiar_estado_cliente(id, estado):
    """Cambia el estado de un cliente"""
    conn = None
    cursor = None
    try:
        if estado not in ['Activo', 'Inactivo', 'Bloqueado']:
            flash("Estado no válido", "error")
            return redirect(url_for('gestion_clientes'))

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar existencia
        cursor.execute("SELECT ID FROM Clientes WHERE ID = %s", (id,))
        if not cursor.fetchone():
            flash("Cliente no encontrado", "error")
            return redirect(url_for('gestion_clientes'))

        cursor.execute(
            "UPDATE Clientes SET Estatus = %s WHERE ID = %s",
            (estado, id)
        )
        conn.commit()
        
        flash(f"Estado cambiado a {estado}", "success")
        return redirect(url_for('gestion_clientes'))
    
    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al cambiar estado: {str(e)}")
        flash("Error al cambiar estado", "error")
        return redirect(url_for('gestion_clientes'))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Eliminar cliente
################################################################################
@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    """Elimina un cliente"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar existencia
        cursor.execute("SELECT ID FROM Clientes WHERE ID = %s", (id,))
        if not cursor.fetchone():
            flash("Cliente no encontrado", "error")
            return redirect(url_for('gestion_clientes'))
        
        cursor.execute("DELETE FROM Clientes WHERE ID = %s", (id,))
        conn.commit()
        
        flash("Cliente eliminado", "success")
        return redirect(url_for('gestion_clientes'))
    
    except Exception as e:
        if conn: conn.rollback()
        app.logger.error(f"Error al eliminar: {str(e)}")
        flash("Error al eliminar cliente", "error")
        return redirect(url_for('gestion_clientes'))
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Configuración categoria almacenamiento
################################################################################
@app.route('/categorias_almacen')
def mostrar_categorias_almacen():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener categorías
        sql_categorias = "SELECT ID, Nombre, Descripcion, Estatus, Fecha_Creacion FROM CATEGORIA_ALMACEN ORDER BY Fecha_Creacion DESC"
        cursor.execute(sql_categorias)
        categorias = cursor.fetchall()

        # Obtener subcategorías
        sql_subcategorias = """
            SELECT s.ID, s.Nombre, s.Descripcion, s.Estatus, s.Fecha_Creacion, c.Nombre AS CategoriaNombre
            FROM SUBCATEGORIA_ALMACEN s
            JOIN CATEGORIA_ALMACEN c ON s.CategoriaID = c.ID
            ORDER BY s.Fecha_Creacion DESC
        """
        cursor.execute(sql_subcategorias)
        subcategorias = cursor.fetchall()

        return render_template('configuracion_almacen.html', data=categorias, categorias=categorias, subcategorias=subcategorias)

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        flash("Error al obtener datos de almacenamiento", "error")
        return render_template('configuracion_almacen.html', data=[], subcategorias=[])

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Formulario categoria almacenamiento
################################################################################
@app.route('/formulario_categoria_almacen')
def formulario_categoria_almacen():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template('formulario_categoria_almacen.html', fecha_actual=fecha_actual)

@app.route('/guardar_categoria_almacen', methods=['POST'])
def guardar_categoria_almacen():
    conn = None
    cursor = None
    try:
        nombre = request.form.get('Nombre', '').strip()
        descripcion = request.form.get('Descripcion', '').strip()
        estatus = request.form.get('Estatus', '').strip()

        if not nombre or not estatus:
            flash("Los campos 'Nombre' y 'Estatus' son obligatorios.", "error")
            return redirect(url_for('formulario_categoria_almacen'))

        conn = get_db_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d')
        sql = "INSERT INTO CATEGORIA_ALMACEN (Nombre, Descripcion, Estatus, Fecha_Creacion) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, estatus, fecha))
        conn.commit()
        flash("Categoría de almacén guardada exitosamente", "success")
        return redirect(url_for('mostrar_categorias_almacen'))

    except Exception as e:
        print(f"Error al guardar categoría de almacén: {e}")
        flash("Ocurrió un error al guardar la categoría", "error")
        return redirect(url_for('mostrar_categorias_almacen'))

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

################################################################################
# Editar categoria almacenamiento
################################################################################

@app.route('/editar_categoria_almacen', methods=['POST'])
def editar_categoria_almacen():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        id = request.form['ID']
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        estatus = request.form['Estatus']

        sql = """
        UPDATE CATEGORIA_ALMACEN 
        SET Nombre=%s, Descripcion=%s, Estatus=%s 
        WHERE ID=%s
        """
        cursor.execute(sql, (nombre, descripcion, estatus, id))
        conn.commit()
        flash("Categoría actualizada exitosamente", "success")
    except Exception as e:
        print("Error al editar:", e)
        flash("Error al actualizar la categoría", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_categorias_almacen'))

################################################################################
# eliminar categoria almacenamiento
################################################################################

@app.route('/eliminar_categoria_almacen/<int:id>', methods=['POST'])
def eliminar_categoria_almacen(id):
    """Elimina una categoría de almacenamiento por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CATEGORIA_ALMACEN WHERE ID = %s", (id,))
        conn.commit()
        flash("Categoría eliminada exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al eliminar categoría ID {id}: {str(e)}")
        flash("Error al eliminar la categoría", "error")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return redirect(url_for('mostrar_categorias_almacen'))


################################################################################
# formulario sub categoria almacenamiento
################################################################################



@app.route('/subcategoria_almacen', methods=['GET'])
def formulario_subcategoria_almacen():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener categorías ordenadas por fecha de creación
        cursor.execute("SELECT ID, Nombre FROM CATEGORIA_ALMACEN ORDER BY Fecha_Creacion DESC")
        categorias = cursor.fetchall()

        # Obtener subcategorías
        cursor.execute("""
            SELECT s.ID, s.Nombre, s.Descripcion, s.Estatus, s.Fecha_Creacion, c.Nombre AS CategoriaNombre
            FROM SUBCATEGORIA_ALMACEN s
            JOIN CATEGORIA_ALMACEN c ON s.CategoriaID = c.ID
            ORDER BY s.Fecha_Creacion DESC
        """)
        subcategorias = cursor.fetchall()

        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        return render_template("formulario_subcategoria_almacen.html", 
                               categorias=categorias, 
                               subcategorias=subcategorias,
                               fecha_actual=fecha_actual)

    except Exception as e:
        print("Error al cargar el formulario:", e)
        flash("Error al cargar el formulario de subcategoría", "error")
        return redirect(url_for('mostrar_categorias_almacen'))

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@app.route('/guardar_subcategoria_almacen', methods=['POST'])
def guardar_subcategoria_almacen():
    conn = None
    cursor = None
    try:
        categoria_id = request.form['CategoriaID']
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        estatus = request.form['Estatus']

        conn = get_db_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d')
        sql = """
            INSERT INTO SUBCATEGORIA_ALMACEN (CategoriaID, Nombre, Descripcion, Estatus, Fecha_Creacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (categoria_id, nombre, descripcion, estatus, fecha)
        cursor.execute(sql, valores)
        conn.commit()
        flash("Subcategoría registrada exitosamente", "success")
    
    except Exception as e:
        print("Error al guardar subcategoría:", e)
        flash("Error al registrar la subcategoría", "error")

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return redirect(url_for('mostrar_categorias_almacen'))

@app.route('/editar_subcategoria_almacen', methods=['POST'])
def editar_subcategoria_almacen():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        id = request.form['id']
        categoria_id = request.form['categoria_id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        estatus = request.form['estatus']

        sql = """
        UPDATE SUBCATEGORIA_ALMACEN
        SET CategoriaID=%s, Nombre=%s, Descripcion=%s, Estatus=%s
        WHERE ID=%s
        """
        cursor.execute(sql, (categoria_id, nombre, descripcion, estatus, id))
        conn.commit()
        flash("Subcategoría actualizada exitosamente", "success")
    except Exception as e:
        print("Error al editar subcategoría:", e)
        flash("Error al actualizar la subcategoría", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_categorias_almacen'))

@app.route('/eliminar_subcategoria_almacen/<int:id>', methods=['POST'])
def eliminar_subcategoria_almacen(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SUBCATEGORIA_ALMACEN WHERE ID = %s", (id,))
        conn.commit()
        flash("Subcategoría eliminada exitosamente", "success")
    except Exception as e:
        print(f"Error al eliminar subcategoría ID {id}: {e}")
        flash("Error al eliminar la subcategoría", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_categorias_almacen'))

################################################################################
# Gestion de almacen
################################################################################


# Ruta para mostrar productos almacen
@app.route('/almacen')
def mostrar_almacen():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT a.ID, a.Nombre, a.Descripcion, a.Cantidad, a.Unidad_Medida, a.Costo_Unitario,
               a.Costo_Total, a.Fecha_Entrada, a.Fecha_Caducidad, a.Estatus, a.Fecha_Registro,
               s.Nombre AS Subcategoria, c.Nombre AS Categoria
        FROM Almacen a
        JOIN SUBCATEGORIA_ALMACEN s ON a.SUBCATEGORIA_ALMACEN_ID = s.ID
        JOIN CATEGORIA_ALMACEN c ON s.CategoriaID = c.ID
        ORDER BY a.Fecha_Registro DESC
    """
    cursor.execute(query)
    productos = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre FROM CATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    categorias = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre, CategoriaID FROM SUBCATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    subcategorias = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('gestion_almacen.html', productos=productos, categorias=categorias, subcategorias=subcategorias)


# Ruta para formulario nuevo producto
@app.route('/formulario_almacen')
def formulario_almacen():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID, Nombre FROM CATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    categorias = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre, CategoriaID FROM SUBCATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    subcategorias = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre FROM Proveedores WHERE Estatus='Activo' ORDER BY Nombre")
    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('formulario_almacen.html', categorias=categorias, subcategorias=subcategorias, proveedores=proveedores)


# Ruta para guardar nuevo producto
@app.route('/registrar_almacen', methods=['POST'])
def registrar_almacen():
    try:
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion')
        subcategoria_id = request.form['subcategoria']
        cantidad = float(request.form['cantidad'])
        unidad_medida = request.form['unidad_medida']
        costo_unitario = request.form.get('costo_unitario')
        costo_unitario = float(costo_unitario) if costo_unitario else None
        costo_total = float(request.form['costo_total'])
        fecha_entrada = request.form['fecha_entrada']
        fecha_caducidad = request.form.get('fecha_caducidad') or None
        estatus = request.form['estatus']
        proveedor_id = request.form['proveedor']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Almacen 
            (Nombre, Descripcion, SUBCATEGORIA_ALMACEN_ID, Cantidad, Unidad_Medida,
             Costo_Unitario, Costo_Total, Fecha_Entrada, Fecha_Caducidad, Estatus, Fecha_Registro, proveedor_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s)
        """
        cursor.execute(query, (nombre, descripcion, subcategoria_id, cantidad, unidad_medida,
                               costo_unitario, costo_total, fecha_entrada, fecha_caducidad, estatus, proveedor_id))
        conn.commit()
        flash('Producto registrado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al registrar producto: {e}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_almacen'))


# Ruta para formulario editar producto
@app.route('/editar_almacen/<int:id>')
def editar_almacen(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Almacen WHERE ID = %s", (id,))
    producto = cursor.fetchone()

    cursor.execute("SELECT ID, Nombre FROM CATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    categorias = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre, CategoriaID FROM SUBCATEGORIA_ALMACEN WHERE Estatus='Activo' ORDER BY Nombre")
    subcategorias = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre FROM Proveedores WHERE Estatus='Activo' ORDER BY Nombre")
    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('mostrar_almacen'))

    return render_template('formulario_almacen.html', producto=producto, categorias=categorias,
                           subcategorias=subcategorias, proveedores=proveedores)


# Ruta para actualizar producto
@app.route('/actualizar_almacen/<int:id>', methods=['POST'])
def actualizar_almacen(id):
    try:
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion')
        subcategoria_id = request.form['subcategoria']
        cantidad = float(request.form['cantidad'])
        unidad_medida = request.form['unidad_medida']
        costo_unitario = request.form.get('costo_unitario')
        costo_unitario = float(costo_unitario) if costo_unitario else None
        costo_total = float(request.form['costo_total'])
        fecha_entrada = request.form['fecha_entrada']
        fecha_caducidad = request.form.get('fecha_caducidad') or None
        estatus = request.form['estatus']
        proveedor_id = request.form['proveedor']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Almacen SET Nombre=%s, Descripcion=%s, SUBCATEGORIA_ALMACEN_ID=%s, Cantidad=%s,
             Unidad_Medida=%s, Costo_Unitario=%s, Costo_Total=%s, Fecha_Entrada=%s,
             Fecha_Caducidad=%s, Estatus=%s, proveedor_id=%s WHERE ID=%s
        """
        cursor.execute(query, (nombre, descripcion, subcategoria_id, cantidad, unidad_medida,
                               costo_unitario, costo_total, fecha_entrada, fecha_caducidad, estatus, proveedor_id, id))
        conn.commit()
        flash('Producto actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar producto: {e}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_almacen'))


# Ruta para eliminar producto
@app.route('/eliminar_almacen/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Almacen WHERE ID = %s", (id,))
        conn.commit()
        flash('Producto eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {e}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('mostrar_almacen'))


# Ruta para obtener subcategorías por categoría (JSON para JS)
@app.route('/subcategorias_por_categoria/<int:categoria_id>')
def subcategorias_por_categoria(categoria_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID, Nombre FROM SUBCATEGORIA_ALMACEN WHERE CategoriaID = %s AND Estatus='Activo' ORDER BY Nombre", (categoria_id,))
    subcategorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(subcategorias)




################################################################################
# corer la aplicación
################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=4000)