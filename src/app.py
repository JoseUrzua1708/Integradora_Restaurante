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
        cursor.execute("SELECT ID, Nombre, Descripcion, Fecha_Creacion, Fecha_Actualizacion  FROM Roles")
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
        cursor.execute("SELECT ID, Nombre, Descripcion, Fecha_Creacion, Fecha_Actualizacion FROM Roles")
        roles = cursor.fetchall() 
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        return render_template('formulario_roles.html', fecha_actual=fecha_actual, roles=roles)
    except Exception as e:
        app.logger.error(f"Error en formulario_roles: {str(e)}")
        flash("Error al cargar el formulario de roles", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route('/guardar_rol', methods=['POST'])
def guardar_rol():
    """Guarda un nuevo rol"""
    conn = None
    cursor = None
    try:
        datos = {
            'Nombre': request.form['Nombre'].strip(),
            'Descripcion': request.form['Descripcion'].strip(),
            'Fecha_Creacion': request.form['Fecha_Creacion'],
            'Fecha_Actualizacion': request.form['Fecha_Actualizacion'],
            
        }

        campos_requeridos = ['Nombre', 'Descripcion', 'Fecha_Creacion', 'Fecha_Actualizacion', ]
        if not all(datos[campo] for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return redirect(url_for('formulario_roles'))

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Roles (
                Nombre, Descripcion, Fecha_Creacion, Fecha_Actualizacion
            ) VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            datos['Nombre'], datos['Descripcion'], datos['Fecha_Creacion'],
            datos['Fecha_Actualizacion']
        )
        cursor.execute(query, params)
        conn.commit()
        flash("Rol registrado exitosamente")
        return redirect(url_for('gestion_roles'))
    except Exception as e:
        app.logger.error(f"Error al guardar rol: {str(e)}")
        flash("Error al guardar el rol", "error")
        return redirect(url_for('formulario_roles'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Eliminar rol
################################################################################

@app.route('/eliminar/<int:id>')
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
            'nombre': request.form['Nombre'].strip(),
            'descripcion': request.form['Descripcion'].strip(),
            'fecha_creacion': request.form['Fecha_Creacion'],
            'fecha_actualizacion': request.form['Fecha_Actualizacion'],
            'sucursal_id': request.form['Sucursal_ID']
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Roles SET 
                Nombre = %(nombre)s,
                Descripcion = %(descripcion)s,
                Fecha_Creacion = %(fecha_creacion)s,
                Fecha_Actualizacion = %(fecha_actualizacion)s,
                Sucursal_ID = %(sucursal_id)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
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
# Gestión de empleados
################################################################################
@app.route('/gestion_empleados')
def gestion_empleados():
    """Muestra la lista de empleados"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID, Nombre, Apellido_p, Apellido_M, Correo, Telefono FROM Empleados")
        empleados = cursor.fetchall()
        return render_template('gestion_empleados.html', empleados=empleados)
    except Exception as e:
        app.logger.error(f"Error en gestion_empleados: {str(e)}")
        flash("Error al cargar los empleados", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# Formulario de empleados
################################################################################
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
        return render_template('formulario_empleado.html', sucursales=sucursales, roles=roles)
    except Exception as e:
        app.logger.error(f"Error en formulario_empleado: {str(e)}")
        flash("Error al cargar el formulario de empleado", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route('/guardar_empleado', methods=['POST'])
def guardar_empleado():
    """Guarda un nuevo empleado"""
    conn = None
    cursor = None
    try:
        datos = {
            'Sucursal_ID': request.form['Sucursal_ID'],
            'Rol_ID': request.form['Rol_ID'],
            'Nombre': request.form['Nombre'].strip(),
            'Apellido_p': request.form['Apellido_p'].strip(),
            'Apellido_M': request.form.get('Apellido_M', '').strip(),
            'Correo': request.form['Correo'].strip(),
            'Telefono': request.form.get('Telefono', '').strip(),
            'Fecha_Nacimiento': request.form['Fecha_Nacimiento'],
            'Genero': request.form['Genero'],
            'Estatus': request.form.get('Estatus', 'Activo'),
            'Salario': float(request.form.get('Salario', 0.0)),
            'Tipo_Contrato': request.form.get('Tipo_Contrato', ''),
            'Fecha_Contratacion': request.form['Fecha_Contratacion'],
            'Fecha_Terminacion': request.form.get('Fecha_Terminacion', None) if request.form.get('Fecha_Terminacion') else None
        }

        # Validación de campos obligatorios
        campos_requeridos = ['Sucursal_ID', 'Rol_ID', 'Nombre', 'Apellido_p', 'Correo', 
                            'Telefono', 'Fecha_Nacimiento', 'Genero', 'Fecha_Contratacion']
        if not all(datos[campo] for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return redirect(url_for('formulario_empleado'))

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Empleados (
                Sucursal_ID, Rol_ID, Nombre, Apellido_p, Apellido_M, Correo, Telefono,
                Fecha_Nacimiento, Genero, Estatus, Salario, Tipo_Contrato,
                Fecha_Contratacion, Fecha_Terminacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            datos['Sucursal_ID'], datos['Rol_ID'], datos['Nombre'], datos['Apellido_p'],
            datos['Apellido_M'], datos['Correo'], datos['Telefono'], datos['Fecha_Nacimiento'],
            datos['Genero'], datos['Estatus'], datos['Salario'], datos['Tipo_Contrato'],
            datos['Fecha_Contratacion'], datos['Fecha_Terminacion']
        )
        cursor.execute(query, params)
        conn.commit()
        flash("Empleado registrado exitosamente", "success")
        return redirect(url_for('gestion_empleados'))
    except Exception as e:
        app.logger.error(f"Error al guardar empleado: {str(e)}")
        flash("Error al guardar el empleado", "error")
        return redirect(url_for('formulario_empleado'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

################################################################################
# eliminar empleado
################################################################################

@app.route('/eliminar/<int:id>')
def eliminar_empleado(id):
    """Elimina un empleado por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Empleados WHERE ID = %s", (id,))
        conn.commit()
        flash("Empleado eliminado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al eliminar empleado ID {id}: {str(e)}")
        flash("Error al eliminar el empleado", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return redirect(url_for('gestion_empleados'))

################################################################################
# actualizar empleado
################################################################################

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_empleado(id):
    """Actualiza un empleado existente"""
    conn = None
    cursor = None
    try:
        datos = {
            'id': id,
            'sucursal_id': request.form['Sucursal_ID'],
            'rol_id': request.form['Rol_ID'],
            'nombre': request.form['Nombre'].strip(),
            'apellido_p': request.form['Apellido_p'].strip(),
            'apellido_m': request.form.get('Apellido_M', '').strip(),
            'correo': request.form['Correo'].strip(),
            'telefono': request.form.get('Telefono', '').strip(),
            'fecha_nacimiento': request.form['Fecha_Nacimiento'],
            'genero': request.form['Genero'],
            'estatus': request.form.get('Estatus', 'Activo'),
            'salario': float(request.form.get('Salario', 0.0)),
            'tipo_contrato': request.form.get('Tipo_Contrato', ''),
            'fecha_contratacion': request.form['Fecha_Contratacion'],
            'fecha_terminacion': request.form.get('Fecha_Terminacion', None) if request.form.get('Fecha_Terminacion') else None
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Empleados SET 
                Sucursal_ID = %(sucursal_id)s,
                Rol_ID = %(rol_id)s,
                Nombre = %(nombre)s,
                Apellido_p = %(apellido_p)s,
                Apellido_M = %(apellido_m)s,
                Correo = %(correo)s,
                Telefono = %(telefono)s,
                Fecha_Nacimiento = %(fecha_nacimiento)s,
                Genero = %(genero)s,
                Estatus = %(estatus)s,
                Salario = %(salario)s,
                Tipo_Contrato = %(tipo_contrato)s,
                Fecha_Contratacion = %(fecha_contratacion)s,
                Fecha_Terminacion = %(fecha_terminacion)s
            WHERE ID = %(id)s
        """
        cursor.execute(query, datos)
        conn.commit()
        flash("Empleado actualizado exitosamente", "success")
    except Exception as e:
        app.logger.error(f"Error al actualizar empleado ID {id}: {str(e)}")
        flash("Error al actualizar el empleado", "error")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()        
    return redirect(url_for('gestion_empleados'))

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
    """Muestra la lista de clientes"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        return render_template('gestion_clientes.html', clientes=clientes)
    except Exception as e:
        app.logger.error(f"Error en gestion_clientes: {e}")
        flash("Error al cargar los clientes", "error")
        return redirect(url_for('inicio'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

################################################################################
# Formulario de clientes (nuevo o editar)
################################################################################
@app.route('/formulario_clientes', methods=['GET'])
@app.route('/formulario_clientes/<int:id>', methods=['GET'])
def formulario_cliente(id=None):
    """Muestra el formulario para registrar o editar un cliente"""
    cliente = None
    if id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes WHERE ID = %s", (id,))
            cliente = cursor.fetchone()
        except Exception as e:
            app.logger.error(f"Error al obtener cliente: {e}")
            flash("Error al cargar el cliente", "error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return render_template('formulario_cliente.html', cliente=cliente)

################################################################################
# Guardar cliente (crear o actualizar)
################################################################################
@app.route('/guardar_cliente', methods=['POST'])
def guardar_cliente():
    conn = None
    cursor = None
    try:
        id_cliente = request.form.get('id')

        datos = {
            'nombre': request.form['nombre'].strip(),
            'apellido_p': request.form['apellido_p'].strip(),
            'apellido_m': request.form.get('apellido_m', '').strip(),
            'correo': request.form['correo'].strip(),
            'telefono': request.form.get('telefono', '').strip(),
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'genero': request.form['genero'],
            'preferencias': request.form['preferencias'],
            'restricciones': request.form['restricciones'],
            'estatus': request.form.get('estatus', 'Activo'),
            'sucursal': request.form.get('sucursal', '')
        }

        campos_requeridos = ['nombre', 'apellido_p', 'correo', 'telefono', 'fecha_nacimiento', 'genero',
                             'preferencias', 'restricciones', 'estatus']
        if not all(datos[campo] for campo in campos_requeridos):
            flash("Todos los campos obligatorios deben completarse", "error")
            return redirect(url_for('formulario_cliente'))

        conn = get_db_connection()
        cursor = conn.cursor()

        if id_cliente:
            datos['id'] = id_cliente
            query = """
                UPDATE Clientes SET 
                    Nombre = %(nombre)s,
                    Apellido_P = %(apellido_p)s,
                    Apellido_M = %(apellido_m)s,
                    Correo = %(correo)s,
                    Telefono = %(telefono)s,
                    Fecha_Nacimiento = %(fecha_nacimiento)s,
                    Genero = %(genero)s,
                    Preferencias = %(preferencias)s,
                    Restricciones_Alimenticias = %(restricciones)s,
                    Estatus = %(estatus)s,
                    Sucursal_ID = %(sucursal)s
                WHERE ID = %(id)s
            """
            cursor.execute(query, datos)
            flash("Cliente actualizado exitosamente", "success")
        else:
            query = """
                INSERT INTO Clientes (
                    Nombre, Apellido_P, Apellido_M, Correo, Telefono, Fecha_Nacimiento, Genero, Preferencias, 
                    Restricciones_Alimenticias, Estatus, Sucursal_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                datos['nombre'], datos['apellido_p'], datos['apellido_m'], datos['correo'],
                datos['telefono'], datos['fecha_nacimiento'], datos['genero'], datos['preferencias'],
                datos['restricciones'], datos['estatus'], datos['sucursal']
            ))
            flash("Cliente registrado exitosamente", "success")

        conn.commit()
        return redirect(url_for('gestion_clientes'))

    except Exception as e:
        logging.error(f"Error en guardar_cliente: {str(e)}")
        flash("Error técnico al guardar el cliente", "error")
        return redirect(url_for('formulario_cliente'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

################################################################################
# Eliminar cliente
################################################################################
@app.route('/eliminar/<int:id>')
def eliminar_cliente(id):
    """Elimina un cliente por ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes WHERE ID = %s", (id,))
        conn.commit()
        flash("Cliente eliminado exitosamente", "success")
    except Exception as e:
        logging.error(f"Error al eliminar cliente: {str(e)}")
        flash("Error técnico al eliminar el cliente", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return redirect(url_for('gestion_clientes'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)