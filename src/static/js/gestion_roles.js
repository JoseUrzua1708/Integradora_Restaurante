// Manejar eventos cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Configurar event listeners para los selects de acción
    document.querySelectorAll('.accion-rol').forEach(select => {
        select.addEventListener('change', function() {
            const opcion = this.value;
            const id = this.dataset.id;
            const nombre = this.dataset.nombre;
            const descripcion = this.dataset.descripcion;
            const sucursal_id = this.dataset.sucursalId;
            
            if (opcion === "Editar") {
                modalEditar(id, nombre, descripcion, sucursal_id);
            } else if (opcion === "Eliminar") {
                modalEliminar(id);
            }
            
            // Resetear el select a la opción por defecto
            this.selectedIndex = 0;
        });
    });

    // Configurar el envío del formulario de edición
    const formEditar = document.getElementById('form-editar');
    if (formEditar) {
        formEditar.addEventListener('submit', function(e) {
            e.preventDefault();
            enviarFormularioEdicion(this);
        });
    }

    // Configurar evento para cerrar modales al hacer clic fuera
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById("modal-editarRol")) {
            cerrarEditar();
        } else if (event.target === document.getElementById("modal-eliminarRol")) {
            cerrarEliminar();
        }
    });
});

// Función para abrir modal de edición
function modalEditar(id, nombre, descripcion, sucursal_id) {
    const modal = document.getElementById('modal-editarRol');
    
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nombre').value = nombre;
    document.getElementById('edit-descripcion').value = descripcion;
    
    // Seleccionar la sucursal actual
    const selectSucursal = document.getElementById('edit-sucursal');
    if (selectSucursal && sucursal_id) {
        selectSucursal.value = sucursal_id;
    }
    
    document.getElementById('form-editar').action = `/actualizar/${id}`;
    modal.style.display = 'block';
    
    // Animación de aparición
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

// Función para enviar el formulario de edición
async function enviarFormularioEdicion(form) {
    const formData = new FormData(form);
    const id = formData.get('id');
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        const result = await response.json();
        
        if (response.ok && result.success) {
            window.location.reload();
        } else {
            if (result.errors) {
                alert(result.errors.join('\n'));
            } else {
                alert('Error al actualizar el rol');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
}

// Función para cerrar modal de edición
function cerrarEditar() {
    const modal = document.getElementById('modal-editarRol');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// Función para abrir modal de eliminación
function modalEliminar(id) {
    document.getElementById('delete-id').value = id;
    document.getElementById('form-eliminar').action = `/eliminar/${id}`;
    document.getElementById('modal-eliminarRol').style.display = 'block';
}

// Función para cerrar modal de eliminación
function cerrarEliminar() {
    document.getElementById('modal-eliminarRol').style.display = 'none';
}