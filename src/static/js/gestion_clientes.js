document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let currentPage = 1;
    const rowsPerPage = 10;
    let allClients = [];
    let filteredClients = [];
    let sortColumn = 'id';
    let sortDirection = 'asc';

    // Inicialización
    initTable();
    setupEventListeners();

    function initTable() {
        // Obtener todos los clientes de la tabla
        const rows = document.querySelectorAll('#clientesBody tr');
        allClients = Array.from(rows).map(row => {
            return {
                id: row.getAttribute('data-id'),
                cells: Array.from(row.cells).map(cell => cell.textContent.trim()),
                element: row
            };
        });
        
        filteredClients = [...allClients];
        updateTable();
    }

    function setupEventListeners() {
        // Búsqueda
        const searchButton = document.getElementById('searchButton');
        const searchInput = document.getElementById('searchInput');
        
        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') performSearch();
        });

        // Ordenación
        document.querySelectorAll('#clientesTable th[data-column]').forEach(header => {
            header.addEventListener('click', () => {
                const column = header.getAttribute('data-column');
                
                // Cambiar dirección si es la misma columna
                if (sortColumn === column) {
                    sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
                } else {
                    sortColumn = column;
                    sortDirection = 'asc';
                }
                
                // Actualizar iconos
                document.querySelectorAll('.sort-icon').forEach(icon => {
                    icon.className = 'fas fa-sort sort-icon';
                });
                
                const icon = header.querySelector('.sort-icon');
                icon.className = `fas fa-sort-${sortDirection === 'asc' ? 'up' : 'down'} sort-icon`;
                
                sortClients();
                updateTable();
            });
        });

        // Paginación
        document.getElementById('prevPage').addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                updateTable();
            }
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            const totalPages = Math.ceil(filteredClients.length / rowsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                updateTable();
            }
        });

        // Modales
        setupModal('addClientModal');
        setupModal('editClientModal');
        setupModal('deleteClientModal');

        // Botones de acción en filas
        document.querySelectorAll('.action-icon').forEach(icon => {
            icon.addEventListener('click', function() {
                const row = this.closest('tr');
                const clientId = row.getAttribute('data-id');
                
                if (this.classList.contains('fa-edit')) {
                    openEditModal(clientId);
                } else if (this.classList.contains('fa-eye')) {
                    viewClientDetails(clientId);
                } else if (this.classList.contains('fa-user-slash') || this.classList.contains('fa-user-check')) {
                    toggleClientStatus(clientId);
                } else if (this.classList.contains('fa-trash')) {
                    openDeleteModal(clientId);
                }
            });
        });
    }

    function performSearch() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        
        if (searchTerm.trim() === '') {
            filteredClients = [...allClients];
        } else {
            filteredClients = allClients.filter(client => {
                return client.cells.some(cell => cell.toLowerCase().includes(searchTerm));
            });
        }
        
        currentPage = 1;
        updateTable();
    }

    function sortClients() {
        const columnIndex = Array.from(document.querySelectorAll('#clientesTable th[data-column]'))
            .findIndex(th => th.getAttribute('data-column') === sortColumn);
        
        filteredClients.sort((a, b) => {
            let valueA = a.cells[columnIndex];
            let valueB = b.cells[columnIndex];
            
            // Convertir a número si es ID
            if (sortColumn === 'id') {
                valueA = parseInt(valueA);
                valueB = parseInt(valueB);
                return sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
            }
            
            // Ordenar fechas
            if (sortColumn.includes('fecha')) {
                valueA = new Date(valueA);
                valueB = new Date(valueB);
                return sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
            }
            
            // Ordenar texto
            return sortDirection === 'asc' 
                ? valueA.localeCompare(valueB) 
                : valueB.localeCompare(valueA);
        });
    }

    function updateTable() {
        const startIndex = (currentPage - 1) * rowsPerPage;
        const endIndex = startIndex + rowsPerPage;
        const paginatedClients = filteredClients.slice(startIndex, endIndex);
        
        // Ocultar todas las filas
        allClients.forEach(client => {
            client.element.style.display = 'none';
        });
        
        // Mostrar solo las filas de la página actual
        paginatedClients.forEach(client => {
            client.element.style.display = '';
        });
        
        // Actualizar información de paginación
        document.getElementById('paginationInfo').textContent = 
            `Mostrando ${filteredClients.length > 0 ? startIndex + 1 : 0}-${Math.min(endIndex, filteredClients.length)} de ${filteredClients.length} clientes`;
        
        document.getElementById('currentPage').textContent = currentPage;
        
        // Habilitar/deshabilitar botones de paginación
        document.getElementById('prevPage').disabled = currentPage === 1;
        document.getElementById('nextPage').disabled = endIndex >= filteredClients.length;
    }

    function setupModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;
        
        // Botón para abrir modal (si existe)
        const openButton = document.querySelector(`[data-target="#${modalId}"]`);
        if (openButton) {
            openButton.addEventListener('click', () => {
                modal.style.display = 'block';
            });
        }
        
        // Botones para cerrar modal
        modal.querySelectorAll('.close-btn').forEach(button => {
            button.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        });
        
        // Cerrar al hacer clic fuera del modal
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    function openEditModal(clientId) {
        // Aquí deberías hacer una petición para obtener los datos del cliente
        // o extraerlos de la fila de la tabla
        console.log(`Editar cliente con ID: ${clientId}`);
        
        // Ejemplo de cómo podrías llenar el modal:
        // const clientRow = document.querySelector(`tr[data-id="${clientId}"]`);
        // document.getElementById('editNombre').value = clientRow.cells[1].textContent;
        // ... etc
        
        const modal = document.getElementById('editClientModal');
        modal.style.display = 'block';
    }

    function viewClientDetails(clientId) {
        console.log(`Ver detalles del cliente con ID: ${clientId}`);
        // Aquí podrías abrir un modal con más detalles o redirigir a una página
    }

    function toggleClientStatus(clientId) {
        console.log(`Cambiar estatus del cliente con ID: ${clientId}`);
        // Confirmación y luego hacer petición AJAX o recargar la página
        if (confirm('¿Está seguro de cambiar el estatus de este cliente?')) {
            // Aquí iría la lógica para cambiar el estatus
            location.reload(); // Recargar para ver cambios (temporal)
        }
    }

    function openDeleteModal(clientId) {
        console.log(`Eliminar cliente con ID: ${clientId}`);
        const modal = document.getElementById('deleteClientModal');
        modal.style.display = 'block';
        
        // Configurar el botón de eliminar
        const deleteButton = document.getElementById('deleteClientButton');
        deleteButton.onclick = function() {
            // Aquí iría la lógica para eliminar el cliente
            console.log(`Cliente ${clientId} eliminado`);
            modal.style.display = 'none';
            location.reload(); // Recargar para ver cambios (temporal)
        };
    }

    // Configurar el formulario de agregar cliente
    document.getElementById('addClientButton').addEventListener('click', function() {
        // Validar formulario
        const form = document.getElementById('addClientForm');
        let isValid = true;
        
        // Validación simple (podrías hacerla más completa)
        form.querySelectorAll('[required]').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#e74c3c';
            }
        });
        
        if (isValid) {
            console.log('Agregar nuevo cliente:', {
                nombre: document.getElementById('nombre').value,
                apellido_p: document.getElementById('apellido_p').value,
                // ... otros campos
            });
            
            // Aquí iría la petición AJAX o envío del formulario
            alert('Cliente agregado con éxito (simulación)');
            document.getElementById('addClientModal').style.display = 'none';
            form.reset();
            // location.reload(); // Recargar para ver cambios
        } else {
            alert('Por favor complete todos los campos requeridos');
        }
    });
});