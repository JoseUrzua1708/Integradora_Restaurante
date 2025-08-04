document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('empleadosTable');
    const tbody = document.getElementById('empleadosBody');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const prevPage = document.getElementById('prevPage');
    const nextPage = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const paginationInfo = document.getElementById('paginationInfo');

    const editEmployeeModal = document.getElementById('editEmployeeModal');
    const editEmployeeForm = document.getElementById('editEmployeeForm');
    const cancelEditBtn = document.getElementById('cancelEditBtn');

    const deleteConfirmModal = document.getElementById('deleteConfirmModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    
    let currentPageNum = 1;
    const rowsPerPage = 10;
    let allEmployeeRows = Array.from(tbody.querySelectorAll('tr.employee-row')); // Solo las filas principales de empleados
    let filteredEmployeeRows = allEmployeeRows;
    let currentEmpleadoIdToEdit = null; // Para el modal de edición
    let empleadoIdToDelete = null; // Para el modal de eliminación

    // --- Funciones de Utilidad ---

    function getAssociatedDetailsRow(employeeRow) {
        // Asumiendo que la fila de detalles sigue inmediatamente a la fila de empleado
        const employeeId = employeeRow.dataset.id;
        return tbody.querySelector(`#details-row-${employeeId}`);
    }

    // Actualiza el tbody, manejando las filas de detalles asociadas
    function updateTableDisplay() {
        // Oculta todas las filas de detalles antes de rellenar el tbody
        tbody.querySelectorAll('.details-row').forEach(row => row.style.display = 'none');

        const startIdx = (currentPageNum - 1) * rowsPerPage;
        const endIdx = startIdx + rowsPerPage;
        const paginatedRows = filteredEmployeeRows.slice(startIdx, endIdx);

        tbody.innerHTML = ''; // Limpia el tbody

        paginatedRows.forEach(employeeRow => {
            tbody.appendChild(employeeRow);
            const detailsRow = getAssociatedDetailsRow(employeeRow);
            if (detailsRow) {
                tbody.appendChild(detailsRow);
                // Si la fila estaba expandida antes de la paginación/ordenamiento, la re-expande
                if (employeeRow.classList.contains('expanded')) {
                    detailsRow.style.display = 'table-row';
                }
            }
        });

        const totalPages = Math.ceil(filteredEmployeeRows.length / rowsPerPage);
        currentPageSpan.textContent = currentPageNum;
        prevPage.disabled = currentPageNum === 1;
        nextPage.disabled = currentPageNum === totalPages || totalPages === 0;

        const startCount = filteredEmployeeRows.length > 0 ? startIdx + 1 : 0;
        const endCount = Math.min(endIdx, filteredEmployeeRows.length);
        paginationInfo.textContent = `Mostrando ${startCount}-${endCount} de ${filteredEmployeeRows.length} empleados`;
    }

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();

        if (searchTerm === '') {
            filteredEmployeeRows = allEmployeeRows;
        } else {
            filteredEmployeeRows = allEmployeeRows.filter(row => {
                const rowText = row.textContent.toLowerCase();
                return rowText.includes(searchTerm);
            });
        }

        currentPageNum = 1;
        updateTableDisplay();
    }

    function sortTable(columnIndex, sortDirection) {
        const rows = Array.from(filteredEmployeeRows);

        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex].textContent.trim().toLowerCase();
            const bValue = b.cells[columnIndex].textContent.trim().toLowerCase();

            // Para columnas de texto (Sucursal, Rol, Nombre Completo, Tipo Contrato, Estatus)
            return sortDirection === 'asc'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        });

        filteredEmployeeRows = rows;
        updateTableDisplay();
    }

    // --- Event Listeners Generales (Búsqueda, Paginación, Ordenamiento) ---

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    prevPage.addEventListener('click', function() {
        if (currentPageNum > 1) {
            currentPageNum--;
            updateTableDisplay();
        }
    });

    nextPage.addEventListener('click', function() {
        const totalPages = Math.ceil(filteredEmployeeRows.length / rowsPerPage);
        if (currentPageNum < totalPages) {
            currentPageNum++;
            updateTableDisplay();
        }
    });

    table.querySelectorAll('th[data-column]').forEach(header => {
        header.addEventListener('click', function() {
            const columnIndex = Array.from(header.parentNode.children).indexOf(header);
            const currentSort = header.getAttribute('data-sort') || 'none';
            const newSort = currentSort === 'asc' ? 'desc' : 'asc';

            table.querySelectorAll('th[data-column]').forEach(h => {
                h.removeAttribute('data-sort');
                h.querySelector('.sort-icon').className = 'sort-icon fas fa-sort';
            });

            header.setAttribute('data-sort', newSort);
            const icon = header.querySelector('.sort-icon');
            icon.className = newSort === 'asc'
                ? 'sort-icon fas fa-sort-up'
                : 'sort-icon fas fa-sort-down';

            sortTable(columnIndex, newSort);
        });
    });

    // --- Lógica para el Dropdown de Acciones y Click en Fila ---
    tbody.addEventListener('click', function(event) {
        // Cierra cualquier dropdown abierto si se hace clic fuera de él
        if (!event.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown.show').forEach(dropdown => {
                dropdown.classList.remove('show');
            });
        }

        const dropdownBtn = event.target.closest('.btn-dropdown');
        if (dropdownBtn) {
            const dropdown = dropdownBtn.closest('.dropdown');
            dropdown.classList.toggle('show');
            event.stopPropagation(); // Evita que el clic se propague a la fila
        }
    });

    // --- Lógica para "Ver Detalles" (Expandir/Contraer Fila) ---
    tbody.addEventListener('click', function(event) {
        const viewDetailsBtn = event.target.closest('.view-details-btn');
        if (viewDetailsBtn) {
            event.preventDefault();
            const employeeId = viewDetailsBtn.dataset.id;
            const employeeRow = tbody.querySelector(`.employee-row[data-id="${employeeId}"]`);
            const detailsRow = tbody.querySelector(`#details-row-${employeeId}`);

            if (employeeRow && detailsRow) {
                // Alternar la visibilidad de la fila de detalles
                if (detailsRow.style.display === 'table-row') {
                    detailsRow.style.display = 'none';
                    employeeRow.classList.remove('expanded');
                } else {
                    // Ocultar cualquier otra fila de detalles expandida antes de mostrar la actual
                    tbody.querySelectorAll('.details-row').forEach(row => row.style.display = 'none');
                    tbody.querySelectorAll('.employee-row').forEach(row => row.classList.remove('expanded'));

                    detailsRow.style.display = 'table-row';
                    employeeRow.classList.add('expanded');
                }
            }
        }
    });

    // --- Lógica para el Modal de Edición ---
    // Abrir modal de edición
    tbody.addEventListener('click', async function(event) {
        const editBtn = event.target.closest('.edit-btn');
        if (editBtn) {
            event.preventDefault();
            currentEmpleadoIdToEdit = editBtn.dataset.id;
            
            // Fetch the employee data from the server
            try {
                // Usamos fetch para obtener los datos del empleado.
                // Asegúrate de que Flask tiene una ruta /empleados/<id>/data que retorna JSON
                const response = await fetch(`/empleados/${currentEmpleadoIdToEdit}/data`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const empleadoData = await response.json();
                
                // Rellenar el formulario del modal con los datos del empleado
                document.getElementById('edit_Sucursal_ID').value = empleadoData.Sucursal_ID || '';
                document.getElementById('edit_Rol_ID').value = empleadoData.Rol_ID || '';
                document.getElementById('edit_Nombre').value = empleadoData.Nombre || '';
                document.getElementById('edit_Apellido_p').value = empleadoData.Apellido_P || '';
                document.getElementById('edit_Apellido_M').value = empleadoData.Apellido_M || '';
                document.getElementById('edit_Correo').value = empleadoData.Correo || '';
                document.getElementById('edit_Telefono').value = empleadoData.Telefono || '';
                document.getElementById('edit_Fecha_Nacimiento').value = empleadoData.Fecha_Nacimiento || '';
                document.getElementById('edit_Genero').value = empleadoData.Genero || '';
                document.getElementById('edit_Estatus').value = empleadoData.Estatus || 'Activo';
                document.getElementById('edit_Salario').value = empleadoData.Salario || '0.00';
                document.getElementById('edit_Tipo_Contrato').value = empleadoData.Tipo_Contrato || '';
                document.getElementById('edit_Fecha_Contratacion').value = empleadoData.Fecha_Contratacion || '';
                document.getElementById('edit_Fecha_Terminacion').value = empleadoData.Fecha_Terminacion || '';

                editEmployeeModal.style.display = 'flex'; // Muestra el modal
            } catch (error) {
                console.error('Error al obtener datos del empleado para edición:', error);
                alert('No se pudieron cargar los datos del empleado para editar.');
            }
        }
    });

    // Cerrar modal de edición
    editEmployeeModal.querySelector('.close-button').addEventListener('click', function() {
        editEmployeeModal.style.display = 'none';
    });
    cancelEditBtn.addEventListener('click', function() {
        editEmployeeModal.style.display = 'none';
    });
    window.addEventListener('click', function(event) {
        if (event.target === editEmployeeModal) {
            editEmployeeModal.style.display = 'none';
        }
    });

    // Enviar formulario de edición (usando Fetch API)
    editEmployeeForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita el envío tradicional del formulario

        const formData = new FormData(editEmployeeForm);
        const jsonData = {};
        for (const [key, value] of formData.entries()) {
            jsonData[key] = value;
        }

        try {
            const response = await fetch(`/empleados/editar/${currentEmpleadoIdToEdit}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message); // Muestra mensaje de éxito
                editEmployeeModal.style.display = 'none'; // Cierra el modal
                // Recargar los datos de la tabla o actualizar la fila específica
                // Para simplificar, recargaremos la página (más robusto si hay muchos cambios)
                // En un proyecto real, podrías querer actualizar solo la fila afectada
                window.location.reload(); 
            } else {
                alert(`Error: ${result.message || 'No se pudo actualizar el empleado.'}`);
            }
        } catch (error) {
            console.error('Error al enviar el formulario de edición:', error);
            alert('Ocurrió un error al intentar actualizar el empleado.');
        }
    });


    // --- Lógica para el Modal de Confirmación de Eliminación ---
    // Abrir modal de eliminación
    tbody.addEventListener('click', function(event) {
        const deleteBtn = event.target.closest('.delete-btn');
        if (deleteBtn) {
            event.preventDefault();
            empleadoIdToDelete = deleteBtn.dataset.id;
            deleteConfirmModal.style.display = 'flex';
        }
    });

    // Cerrar modal de eliminación
    deleteConfirmModal.querySelector('.close-button').addEventListener('click', function() {
        deleteConfirmModal.style.display = 'none';
    });
    cancelDeleteBtn.addEventListener('click', function() {
        deleteConfirmModal.style.display = 'none';
    });
    window.addEventListener('click', function(event) {
        if (event.target === deleteConfirmModal && event.target !== editEmployeeModal) { // Asegura que no sea el modal de edición
            deleteConfirmModal.style.display = 'none';
        }
    });

    // Confirmar eliminación
    confirmDeleteBtn.addEventListener('click', async function() {
        if (empleadoIdToDelete) {
            try {
                const response = await fetch(`/empleados/eliminar/${empleadoIdToDelete}`, {
                    method: 'DELETE' // Usar método DELETE para eliminación RESTful
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    deleteConfirmModal.style.display = 'none';
                    // Eliminar la fila de la tabla sin recargar la página
                    const rowToRemove = tbody.querySelector(`.employee-row[data-id="${empleadoIdToDelete}"]`);
                    const detailsRowToRemove = tbody.querySelector(`#details-row-${empleadoIdToDelete}`);
                    if (rowToRemove) {
                        rowToRemove.remove();
                    }
                    if (detailsRowToRemove) {
                        detailsRowToRemove.remove();
                    }
                    // Re-capturar todas las filas y re-actualizar la paginación
                    allEmployeeRows = Array.from(tbody.querySelectorAll('tr.employee-row'));
                    performSearch(); // Para re-aplicar filtros y re-actualizar la paginación
                } else {
                    alert(`Error: ${result.message || 'No se pudo eliminar el empleado.'}`);
                }
            } catch (error) {
                console.error('Error al eliminar empleado:', error);
                alert('Ocurrió un error al intentar eliminar el empleado.');
            }
        }
    });

    // Inicializar la visualización de la tabla
    updateTableDisplay();
});