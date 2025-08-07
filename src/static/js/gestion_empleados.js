document.addEventListener('DOMContentLoaded', () => {
  const deleteModal = document.getElementById('deleteModal');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
  const modalCloseBtn = deleteModal.querySelector('.modal-close');

  let empleadoIdToDelete = null;

  // Abrir/cerrar dropdowns
  document.querySelectorAll('.dropdown-toggle').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const dropdown = btn.nextElementSibling;
      // Cerrar otros abiertos
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        if (menu !== dropdown) menu.classList.remove('show');
      });
      dropdown.classList.toggle('show');
    });
  });

  // Cerrar dropdowns al click fuera
  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
      menu.classList.remove('show');
    });
  });

  // Click en botones de acción dentro de la tabla
  document.querySelector('#empleadosTable tbody').addEventListener('click', e => {
    const target = e.target.closest('a');
    if (!target) return;

    e.preventDefault();

    const tr = target.closest('tr');
    const id = target.dataset.id;
    if (!id) return;

    if (target.classList.contains('btn-delete')) {
      empleadoIdToDelete = id;
      openDeleteModal();
    } else if (target.classList.contains('btn-edit')) {
      console.log('Editar empleado ID:', id);
      // Aquí puedes abrir modal edición o redirigir
    } else if (target.classList.contains('btn-view')) {
      console.log('Ver detalles empleado ID:', id);
      // Aquí abrir modal detalles o similar
    }
  });

  // Abrir modal eliminar
  function openDeleteModal() {
    deleteModal.style.display = 'block';
    deleteModal.setAttribute('aria-hidden', 'false');
  }

  // Cerrar modal eliminar
  function closeDeleteModal() {
    deleteModal.style.display = 'none';
    deleteModal.setAttribute('aria-hidden', 'true');
    empleadoIdToDelete = null;
  }

  // Confirmar eliminación
  confirmDeleteBtn.addEventListener('click', () => {
    if (!empleadoIdToDelete) return;
    // Redirigir para eliminar, o usar fetch para AJAX
    window.location.href = `/eliminar_empleado/${empleadoIdToDelete}`;
  });

  // Cancelar eliminación
  cancelDeleteBtn.addEventListener('click', closeDeleteModal);
  modalCloseBtn.addEventListener('click', closeDeleteModal);

  // Cerrar modal con Escape
  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && deleteModal.getAttribute('aria-hidden') === 'false') {
      closeDeleteModal();
    }
  });
});
