document.addEventListener('DOMContentLoaded', () => {
  const deleteModal = document.getElementById('deleteModal');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
  const modalCloseBtn = deleteModal ? deleteModal.querySelector('.modal-close') : null;

  let empleadoIdToDelete = null;

  // Abrir/cerrar dropdowns
  document.querySelectorAll('.dropdown-toggle').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const dropdown = btn.nextElementSibling;
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
  const empleadosTableBody = document.querySelector('#empleadosTable tbody');
  if (empleadosTableBody) {
    empleadosTableBody.addEventListener('click', e => {
      const target = e.target.closest('a');
      if (!target) return;

      e.preventDefault();

      const id = target.dataset.id;
      if (!id) return;

      if (target.classList.contains('btn-delete')) {
        empleadoIdToDelete = id;
        openDeleteModal();
      } else if (target.classList.contains('btn-edit')) {
        console.log('Editar empleado ID:', id);
      } else if (target.classList.contains('btn-view')) {
        console.log('Ver detalles empleado ID:', id);
      }
    });
  }

  function openDeleteModal() {
    if (!deleteModal) return;
    deleteModal.style.display = 'block';
    deleteModal.setAttribute('aria-hidden', 'false');
  }

  function closeDeleteModal() {
    if (!deleteModal) return;
    deleteModal.style.display = 'none';
    deleteModal.setAttribute('aria-hidden', 'true');
    empleadoIdToDelete = null;
  }

  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', () => {
      if (!empleadoIdToDelete) return;
      window.location.href = `/eliminar_empleado/${empleadoIdToDelete}`;
    });
  }

  if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', closeDeleteModal);
  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeDeleteModal);

  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && deleteModal && deleteModal.getAttribute('aria-hidden') === 'false') {
      closeDeleteModal();
    }
  });
});
