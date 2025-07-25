// Variables globales
let idAEliminar = null;

// Función para abrir modales de actualización
function abrirModal(id) {
    document.getElementById('modal' + id).style.display = 'block';
}

// Función para cerrar modales
function cerrarModal(id) {
    document.getElementById('modal' + id).style.display = 'none';
}

// Función para manejar la eliminación
function eliminarRestaurante(id) {
    idAEliminar = id;
    document.getElementById('modalConfirmacion').style.display = 'block';
}

// Evento cuando el DOM está cargado
document.addEventListener('DOMContentLoaded', function() {
    // Manejar selección de opciones (Actualizar/Eliminar)
    document.querySelectorAll('.opciones-restaurante').forEach(select => {
        select.addEventListener('change', function() {
            const id = this.getAttribute('data-id');
            if (this.value === 'actualizar') {
                abrirModal(id);
            } else if (this.value === 'eliminar') {
                eliminarRestaurante(id);
            }
            this.value = 'Opciones'; // Resetear el select
        });
    });

    // Manejar botones de cerrar modal
    document.querySelectorAll('.btn-cerrar-modal').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            cerrarModal(id);
        });
    });

    // Confirmar eliminación
    document.getElementById('btnConfirmar').addEventListener('click', function() {
        if (idAEliminar) {
            window.location.href = '/eliminar/' + idAEliminar;
        }
    });

    // Cancelar eliminación
    document.getElementById('btnCancelar').addEventListener('click', function() {
        document.getElementById('modalConfirmacion').style.display = 'none';
        idAEliminar = null;
    });

    // Cerrar modal al hacer clic fuera
    window.onclick = function(event) {
        const modalConfirmacion = document.getElementById('modalConfirmacion');
        if (event.target === modalConfirmacion) {
            modalConfirmacion.style.display = "none";
            idAEliminar = null;
        }
        
        // También puedes agregar el cierre para los otros modales si es necesario
        document.querySelectorAll('.modal').forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    }
});