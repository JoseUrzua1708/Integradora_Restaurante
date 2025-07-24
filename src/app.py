from flask import Flask, render_template, request, redirect, jsonify, flash
import mysql.connector
from datetime import datetime
from contextlib import closing
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database configuration
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
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        app.logger.error(f"Database connection error: {err}")
        raise

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/formulario_restaurante')
def formulario_restaurante():
    return render_template('formulario_restaurante.html')

@app.route('/formulario_sucursales')
def formulario_sucursales():
    return render_template('formulario_sucursales.html')

@app.route('/formulario_empleado')
def formulario_empleado():
    try:
        with closing(get_db_connection()) as conn, closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute("SELECT ID, Nombre FROM Sucursales WHERE Estatus = 'Activa'")
            sucursales = cursor.fetchall()
            
            cursor.execute("SELECT ID, Nombre FROM Roles")
            roles = cursor.fetchall()
            
            return render_template("formulario_empleado.html", 
                                sucursales=sucursales, 
                                roles=roles)
    except Exception as e:
        app.logger.error(f"Error in formulario_empleado: {str(e)}")
        flash("Error al cargar el formulario de empleado", "error")
        return redirect('/')

@app.route('/gestion_reservaciones')
def gestion_reservaciones():
    try:
        with closing(get_db_connection()) as conn, closing(conn.cursor(dictionary=True)) as cursor:
            # Load options for selects
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

            # History
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
        app.logger.error(f"Error in gestion_reservaciones: {str(e)}")
        flash("Error al cargar la gestión de reservaciones", "error")
        return redirect('/')

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        tipo = request.form.get('tipo')
        cliente = request.form.get('cliente')
        personas = request.form.get('personas')
        fecha = request.form.get('fecha')
        notas = request.form.get('notas', '')

        if not all([tipo, cliente, personas, fecha]):
            flash("Todos los campos obligatorios deben ser completados", "error")
            return redirect('/gestion_reservaciones')

        with closing(get_db_connection()) as conn, closing(conn.cursor()) as cursor:
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
            return redirect('/gestion_reservaciones')

    except Exception as e:
        app.logger.error(f"Error in guardar: {str(e)}")
        flash("Error al guardar la reservación", "error")
        return redirect('/gestion_reservaciones')

if __name__ == '__main__':
    app.run(debug=True, port=2001)