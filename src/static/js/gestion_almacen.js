function filtrarTabla() {
    const input = document.getElementById('searchInput');
    const filtro = input.value.toLowerCase();
    const tabla = document.getElementById('almacenTable');
    const filas = tabla.getElementsByTagName('tr');

    for (let i = 1; i < filas.length; i++) { // saltar encabezado
        const fila = filas[i];
        const textoFila = fila.textContent.toLowerCase();
        fila.style.display = textoFila.includes(filtro) ? '' : 'none';
    }
}