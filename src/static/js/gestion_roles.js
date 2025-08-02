function manejarRol(opcion, id, nombre, descripcion) {
    if (opcion == "Editar") {
        modalEditar(id, nombre, descripcion);
    } else if (opcion == "Eliminar") {
        modalEliminar(id);
    }
}

function modalEditar(id, nombre, descripcion) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nombre').value = nombre;
    document.getElementById('edit-descripcion').value = descripcion;
    document.getElementById('form-editar').action = `/actualizar/${id}`;
    document.getElementById('modal-editarRol').style.display = 'block';
}

function cerrarEditar() {
    document.getElementById('modal-editarRol').style.display = 'none';
}

function modalEliminar(id) {
    document.getElementById('delete-id').value = id;
    document.getElementById('form-eliminar').action = `/eliminar/${id}`;
    document.getElementById('modal-eliminarRol').style.display = 'block';
}

function cerrarEliminar() {
    document.getElementById('modal-eliminarRol').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target === document.getElementById("modal-editarRol")) {
        cerrarEditar();
    } else if (event.target === document.getElementById("modal-eliminarRol")) {
        cerrarEliminar();
    }
}