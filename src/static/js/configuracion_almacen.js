function manejarOpcion(opcion, id, nombre, descripcion, estatus) {
  if (opcion === "editar") {
    abrirModalEditar(id, nombre, descripcion, estatus);
  } else if (opcion === "eliminar") {
    abrirModalEliminar(id);
  }
}


function abrirModalEditar(id, nombre, descripcion, estatus) {
  document.getElementById('edit-id').value = id;
  document.getElementById('edit-nombre').value = nombre;
  document.getElementById('edit-descripcion').value = descripcion;
  document.getElementById('edit-estatus').value = estatus;
  document.getElementById('modal-editar').style.display = 'block';
}

function cerrarModalEditar() {
  document.getElementById('modal-editar').style.display = 'none';
}

window.onclick = function(event) {
  const modal = document.getElementById('modal-editar');
  if (event.target === modal) {
    cerrarModalEditar();
  }
};

function abrirModalEliminar(id) {
  document.getElementById('delete-id').value = id;
  document.getElementById('form-eliminar').action = `/eliminar_categoria_almacen/${id}`;
  document.getElementById('modal-eliminar').style.display = 'block';
}

function cerrarModalEliminar() {
  document.getElementById('modal-eliminar').style.display = 'none';
}

