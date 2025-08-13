document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const config = {
        rowsPerPage: 10,
        currentPage: 1,
        sortColumn: 'id',
        sortDirection: 'asc',
        clients: [],
        filteredClients: []
    };

    // DOM Elements
    const elements = {
        table: document.getElementById('clientesTable'),
        tbody: document.getElementById('clientesBody'),
        searchInput: document.getElementById('searchInput'),
        searchButton: document.getElementById('searchButton'),
        prevPage: document.getElementById('prevPage'),
        nextPage: document.getElementById('nextPage'),
        currentPage: document.getElementById('currentPage'),
        paginationInfo: document.getElementById('paginationInfo'),
        addClientModal: document.getElementById('addClientModal'),
        editClientModal: document.getElementById('editClientModal'),
        deleteClientModal: document.getElementById('deleteClientModal')
    };

    // Initialize the application
    init();

    function init() {
        loadClients();
        setupEventListeners();
    }

    function loadClients() {
        // In a real app, this would be an AJAX call to your Flask endpoint
        const rows = elements.tbody.querySelectorAll('tr');
        config.clients = Array.from(rows).map(row => ({
            id: row.dataset.id,
            cells: Array.from(row.cells).map(cell => cell.textContent.trim()),
            element: row,
            status: row.querySelector('.status').textContent.trim()
        }));
        
        config.filteredClients = [...config.clients];
        updateTable();
    }

    function setupEventListeners() {
        // Search functionality
        elements.searchButton.addEventListener('click', performSearch);
        elements.searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') performSearch();
        });

        // Sorting
        document.querySelectorAll('#clientesTable th[data-column]').forEach(header => {
            header.addEventListener('click', () => {
                const column = header.dataset.column;
                
                if (config.sortColumn === column) {
                    config.sortDirection = config.sortDirection === 'asc' ? 'desc' : 'asc';
                } else {
                    config.sortColumn = column;
                    config.sortDirection = 'asc';
                }
                
                updateSortIcons(header);
                sortClients();
                updateTable();
            });
        });

        // Pagination
        elements.prevPage.addEventListener('click', () => {
            if (config.currentPage > 1) {
                config.currentPage--;
                updateTable();
            }
        });

        elements.nextPage.addEventListener('click', () => {
            const totalPages = Math.ceil(config.filteredClients.length / config.rowsPerPage);
            if (config.currentPage < totalPages) {
                config.currentPage++;
                updateTable();
            }
        });

        // Action buttons
        elements.tbody.addEventListener('click', (e) => {
            const icon = e.target.closest('.action-icon');
            if (!icon) return;
            
            const row = e.target.closest('tr');
            const clientId = row.dataset.id;
            
            if (icon.classList.contains('fa-edit')) {
                openEditModal(clientId, row);
            } else if (icon.classList.contains('fa-eye')) {
                viewDetails(clientId);
            } else if (icon.classList.contains('fa-user-slash') || icon.classList.contains('fa-user-check')) {
                toggleStatus(clientId, row);
            } else if (icon.classList.contains('fa-trash')) {
                openDeleteModal(clientId);
            }
        });

        // Modal controls
        setupModal(elements.addClientModal);
        setupModal(elements.editClientModal);
        setupModal(elements.deleteClientModal);
    }

    function performSearch() {
        const term = elements.searchInput.value.toLowerCase();
        
        if (term.trim() === '') {
            config.filteredClients = [...config.clients];
        } else {
            config.filteredClients = config.clients.filter(client => {
                return client.cells.some(cell => cell.toLowerCase().includes(term));
            });
        }
        
        config.currentPage = 1;
        sortClients();
        updateTable();
    }

    function updateSortIcons(activeHeader) {
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.className = 'fas fa-sort sort-icon';
        });
        
        const activeIcon = activeHeader.querySelector('.sort-icon');
        activeIcon.className = `fas fa-sort-${config.sortDirection === 'asc' ? 'up' : 'down'} sort-icon`;
    }

    function sortClients() {
        const columnIndex = Array.from(document.querySelectorAll('#clientesTable th[data-column]'))
            .findIndex(th => th.dataset.column === config.sortColumn);
        
        config.filteredClients.sort((a, b) => {
            let valueA = a.cells[columnIndex];
            let valueB = b.cells[columnIndex];
            
            // Numeric sorting for ID
            if (config.sortColumn === 'id') {
                valueA = parseInt(valueA);
                valueB = parseInt(valueB);
                return config.sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
            }
            
            // Date sorting
            if (config.sortColumn.includes('fecha')) {
                valueA = new Date(valueA);
                valueB = new Date(valueB);
                return config.sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
            }
            
            // Text sorting
            return config.sortDirection === 'asc' 
                ? valueA.localeCompare(valueB) 
                : valueB.localeCompare(valueA);
        });
    }

    function updateTable() {
        const startIndex = (config.currentPage - 1) * config.rowsPerPage;
        const endIndex = startIndex + config.rowsPerPage;
        const paginatedClients = config.filteredClients.slice(startIndex, endIndex);
        
        // Hide all rows first
        config.clients.forEach(client => {
            client.element.style.display = 'none';
        });
        
        // Show only current page rows
        paginatedClients.forEach(client => {
            client.element.style.display = '';
        });
        
        // Update pagination info
        elements.paginationInfo.textContent = 
            `Mostrando ${startIndex + 1}-${Math.min(endIndex, config.filteredClients.length)} de ${config.filteredClients.length} clientes`;
        
        elements.currentPage.textContent = config.currentPage;
        
        // Update pagination buttons
        elements.prevPage.disabled = config.currentPage === 1;
        elements.nextPage.disabled = endIndex >= config.filteredClients.length;
    }

    function setupModal(modal) {
        if (!modal) return;
        
        // Close modal buttons
        modal.querySelectorAll('.close-btn, .btn-cancelar').forEach(btn => {
            btn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        });
        
        // Close when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    function openEditModal(clientId, row) {
        // In a real app, you would fetch the client data or extract from row
        console.log('Editing client:', clientId);
        
        // Example of populating the edit form:
        // const cells = row.cells;
        // document.getElementById('editNombre').value = cells[1].textContent;
        // ...
        
        elements.editClientModal.style.display = 'block';
    }

    function viewDetails(clientId) {
        console.log('Viewing details for client:', clientId);
        // Could open a detailed view modal or redirect to a details page
    }

    function toggleStatus(clientId, row) {
        const newStatus = row.querySelector('.status').textContent.trim() === 'Activo' ? 'Inactivo' : 'Activo';
        
        if (confirm(`¿Está seguro de cambiar el estado a ${newStatus}?`)) {
            // In a real app, make an AJAX call to your Flask endpoint
            console.log(`Changing status for client ${clientId} to ${newStatus}`);
            
            // Simulate status change
            const statusElement = row.querySelector('.status');
            statusElement.textContent = newStatus;
            statusElement.className = `status status-${newStatus.toLowerCase()}`;
            
            // Update the icon
            const icon = row.querySelector('.fa-user-slash, .fa-user-check');
            if (icon) {
                icon.className = newStatus === 'Activo' 
                    ? 'fas fa-user-slash action-icon' 
                    : 'fas fa-user-check action-icon';
                icon.title = newStatus === 'Activo' ? 'Desactivar' : 'Activar';
            }
            
            // Show feedback
            alert(`Estado cambiado a ${newStatus}`);
        }
    }

    function openDeleteModal(clientId) {
        if (!confirm('¿Está seguro de eliminar este cliente?')) return;
        
        // In a real app, make an AJAX call to your Flask endpoint
        console.log('Deleting client:', clientId);
        
        // Simulate deletion
        const clientToRemove = config.clients.find(c => c.id === clientId);
        if (clientToRemove) {
            clientToRemove.element.remove();
            config.clients = config.clients.filter(c => c.id !== clientId);
            config.filteredClients = config.filteredClients.filter(c => c.id !== clientId);
            updateTable();
        }
        
        alert('Cliente eliminado con éxito');
    }

    // Add new client form handling
    const addClientForm = document.getElementById('addClientForm');
    if (addClientForm) {
        addClientForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate form
            let isValid = true;
            this.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#e74c3c';
                }
            });
            
            if (isValid) {
                // In a real app, submit via AJAX or form action
                console.log('Adding new client:', {
                    nombre: this.nombre.value,
                    apellido_p: this.apellido_p.value,
                    // ... other fields
                });
                
                alert('Cliente agregado con éxito (simulación)');
                this.reset();
                elements.addClientModal.style.display = 'none';
                // location.reload(); // In a real app, you might reload or update the table
            } else {
                alert('Por favor complete todos los campos requeridos');
            }
        });
    }
});