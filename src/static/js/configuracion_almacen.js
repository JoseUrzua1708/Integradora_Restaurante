// ================= CATEGORÍA =================

function manejarOpcion(opcion, id, nombre, descripcion, estatus) {
  if (opcion === "Editar") {
    abrirModalEditarCategoria(id, nombre, descripcion, estatus);
  } else if (opcion === "Eliminar") {
    abrirModalEliminarCategoria(id);
  }
}

function abrirModalEditarCategoria(id, nombre, descripcion, estatus) {
  document.getElementById('edit-id').value = id;
  document.getElementById('edit-nombre').value = nombre;
  document.getElementById('edit-descripcion').value = descripcion;
  document.getElementById('edit-estatus').value = estatus;
  document.getElementById('modal-editar').style.display = 'block';
}

function cerrarModalEditarCategoria() {
  document.getElementById('modal-editar').style.display = 'none';
}

function abrirModalEliminarCategoria(id) {
  document.getElementById('delete-id').value = id;
  document.getElementById('form-eliminar').action = `/eliminar_categoria_almacen/${id}`;
  document.getElementById('modal-eliminar').style.display = 'block';
}

function cerrarModalEliminarCategoria() {
  document.getElementById('modal-eliminar').style.display = 'none';
}

// ================= SUBCATEGORÍA =================

function manejarOpcionSubcategoria(opcion, id, categoria, nombre, descripcion, estatus) {
  if (opcion === "Editar") {
    abrirModalEditarSubcategoria(id, categoria, nombre, descripcion, estatus);
  } else if (opcion === "Eliminar") {
    abrirModalEliminarSubcategoria(id);
  }
}

function abrirModalEditarSubcategoria(id, nombre, descripcion, estatus, categoriaID) {
  document.getElementById('edit-sub-id').value = id;
  document.getElementById('edit-sub-nombre').value = nombre;
  document.getElementById('edit-sub-descripcion').value = descripcion;
  document.getElementById('edit-sub-estatus').value = estatus;

  const selectCategoria = document.getElementById('edit-sub-categoria');
  for (let i = 0; i < selectCategoria.options.length; i++) {
    if (selectCategoria.options[i].value == categoriaID) {
      selectCategoria.options[i].selected = true;
      break;
    }
  }

  document.getElementById('modalEditarSubcategoria').style.display = 'block';
}


function cerrarModalEditarSubcategoria() {
  document.getElementById("modalEditarSubcategoria").style.display = "none";
}


function abrirModalEliminarSubcategoria(id) {
    document.getElementById("delete-sub-id").value = id;
    document.getElementById("form-eliminar-sub").action = `/eliminar_subcategoria_almacen/${id}`;
    document.getElementById("modalEliminarSubcategoria").style.display = "block";
}


function cerrarModalEliminarSubcategoria() {
  document.getElementById("modalEliminarSubcategoria").style.display = "none";
}


// ================= CIERRE MODAL GLOBAL =================

window.onclick = function(event) {
  if (event.target === document.getElementById("modal-editar")) {
    cerrarModalEditarCategoria();
  } else if (event.target === document.getElementById("modal-eliminar")) {
    cerrarModalEliminarCategoria();
  } else if (event.target === document.getElementById("modalEditarSubcategoria")) {
    cerrarModalEditarSubcategoria();
  } else if (event.target === document.getElementById("modalEliminarSubcategoria")) {
    cerrarModalEliminarSubcategoria();
  }
};
