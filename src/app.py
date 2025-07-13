from flask import Flask, render_template
from ConexionDB import get_connection

app = Flask(__name__)

@app.route('/')
def hello_world():
    connection = get_connection()  # Intenta conectarse a la DB
    if connection:
        connection_status = "Conexión a la base de datos exitosa."
        connection.close()  # Cierra la conexión
    else:
        connection_status = "Error al conectar a la base de datos."
    
    # Renderiza una plantilla HTML con 2 variables:
    # - message: "Hello World!"
    # - db_status: El estado de la conexión a la DB
    return render_template('inicio.html', message="Hello World!", db_status=connection_status)

if __name__ == '__main__':
    app.run(debug=True, port=3000)