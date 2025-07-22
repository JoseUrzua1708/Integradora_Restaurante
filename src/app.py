from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pokemon445588",
    database="administracion"
)

@app.route('/')
def gestion_reservaciones():
    cursor = conexion.cursor()

    # Cargar opciones para selects
    cursor.execute("SELECT ID, CONCAT(Nombre, ' ', Apellido_P) FROM Clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT ID, CONCAT(Nombre, ' ', Apellido_P) FROM Empleados")
    empleados = cursor.fetchall()

    cursor.execute("SELECT ID, Numero_Mesa FROM Mesas")
    mesas = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre FROM Eventos")
    eventos = cursor.fetchall()

    cursor.execute("SELECT ID, Nombre FROM Sucursales")
    sucursales = cursor.fetchall()

    # Historial
    cursor.execute("SELECT R.ID, C.Nombre, M.Numero_Mesa, R.Numero_Personas, R.Fecha_Hora FROM Reservaciones R JOIN Clientes C ON R.Cliente_ID = C.ID JOIN Mesas M ON R.Mesa_ID = M.ID")
    reservas_mesas = cursor.fetchall()

    cursor.execute("SELECT E.ID, C.Nombre, EV.Nombre, E.Numero_Personas, E.Fecha_Reserva FROM Eventos_Reservaciones E JOIN Clientes C ON E.Cliente_ID = C.ID JOIN Eventos EV ON E.Evento_ID = EV.ID")
    reservas_eventos = cursor.fetchall()

    cursor.close()
    return render_template("gestion_reservaciones.html", clientes=clientes, empleados=empleados, mesas=mesas, eventos=eventos, sucursales=sucursales, reservas_mesas=reservas_mesas, reservas_eventos=reservas_eventos)

@app.route('/guardar', methods=['POST'])
def guardar():
    tipo = request.form['tipo']
    cliente = request.form['cliente']
    personas = request.form['personas']
    fecha = request.form['fecha']
    notas = request.form['notas']

    cursor = conexion.cursor()

    if tipo == "mesa":
        sucursal = request.form['sucursal']
        mesa = request.form['mesa']
        empleado = request.form['empleado']

        cursor.execute("""
            INSERT INTO Reservaciones (Cliente_ID, Sucursal_ID, Mesa_ID, Fecha_Hora, Numero_Personas, Notas, Empleado_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cliente, sucursal, mesa, fecha, personas, notas, empleado))
    else:
        evento = request.form['evento']
        monto = request.form['monto']

        cursor.execute("""
            INSERT INTO Eventos_Reservaciones (Evento_ID, Cliente_ID, Numero_Personas, Monto_Pagado, Notas)
            VALUES (%s, %s, %s, %s, %s)
        """, (evento, cliente, personas, monto, notas))

    conexion.commit()
    cursor.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=2001)
