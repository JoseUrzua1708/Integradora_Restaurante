function filtrarTabla() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('almacenTable');
    const trs = table.getElementsByTagName('tr');

    // Recorremos las filas (empezando desde 1 para saltar el header)
    for (let i = 1; i < trs.length; i++) {
        const tr = trs[i];
        const tds = tr.getElementsByTagName('td');
        let textoFila = '';

        // Concatenar texto de todas las celdas para búsqueda
        for (let j = 0; j < tds.length - 1; j++) {  // menos la última columna de acciones
            textoFila += tds[j].textContent.toLowerCase() + ' ';
        }

        // Mostrar fila si contiene el texto buscado, ocultar si no
        if (textoFila.indexOf(filter) > -1) {
            tr.style.display = '';
        } else {
            tr.style.display = 'none';
        }
    }
}
