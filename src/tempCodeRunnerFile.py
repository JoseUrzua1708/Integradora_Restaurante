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

        return render_template('configuracion_almacen.html', data=categorias, subcategorias=subcategorias)

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
