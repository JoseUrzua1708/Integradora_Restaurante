document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    const table = document.getElementById('empleadosTable');
    const tbody = document.getElementById('empleadosBody');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const prevPage = document.getElementById('prevPage');
    const nextPage = document.getElementById('nextPage');
    const currentPage = document.getElementById('currentPage');
    const paginationInfo = document.getElementById('paginationInfo');
    
    // Configuración de paginación
    let currentPageNum = 1;
    const rowsPerPage = 10;
    let allRows = Array.from(tbody.querySelectorAll('tr'));
    let filteredRows = allRows;
    
    // Funciones de utilidad
    function updatePagination() {
        const startIdx = (currentPageNum - 1) * rowsPerPage;
        const endIdx = startIdx + rowsPerPage;
        const paginatedRows = filteredRows.slice(startIdx, endIdx);
        
        // Limpiar tabla
        tbody.innerHTML = '';
        
        // Agregar filas paginadas
        paginatedRows.forEach(row => tbody.appendChild(row));
        
        // Actualizar controles de paginación
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        currentPage.textContent = currentPageNum;
        prevPage.disabled = currentPageNum === 1;
        nextPage.disabled = currentPageNum === totalPages || totalPages === 0;
        
        // Actualizar información de paginación
        const startCount = filteredRows.length > 0 ? startIdx + 1 : 0;
        const endCount = Math.min(endIdx, filteredRows.length);
        paginationInfo.textContent = `Mostrando ${startCount}-${endCount} de ${filteredRows.length} empleados`;
    }
    
    // Función de búsqueda
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        
        if (searchTerm.trim() === '') {
            filteredRows = allRows;
        } else {
            filteredRows = allRows.filter(row => {
                const rowText = row.textContent.toLowerCase();
                return rowText.includes(searchTerm);
            });
        }
        
        currentPageNum = 1;
        updatePagination();
    }
    
    // Función de ordenamiento
    function sortTable(columnIndex, sortDirection) {
        const rows = Array.from(filteredRows);
        
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex].textContent.trim().toLowerCase();
            const bValue = b.cells[columnIndex].textContent.trim().toLowerCase();
            
            // Para columnas numéricas (ID)
            if (columnIndex === 0) {
                return sortDirection === 'asc' 
                    ? parseInt(aValue) - parseInt(bValue)
                    : parseInt(bValue) - parseInt(aValue);
            }
            
            // Para columnas de texto
            return sortDirection === 'asc' 
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        });
        
        filteredRows = rows;
        updatePagination();
    }
    
    // Event Listeners
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    prevPage.addEventListener('click', function() {
        if (currentPageNum > 1) {
            currentPageNum--;
            updatePagination();
        }
    });
    
    nextPage.addEventListener('click', function() {
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        if (currentPageNum < totalPages) {
            currentPageNum++;
            updatePagination();
        }
    });
    
    // Ordenamiento por columnas
    table.querySelectorAll('th[data-column]').forEach(header => {
        header.addEventListener('click', function() {
            const columnIndex = Array.from(header.parentNode.children).indexOf(header);
            const currentSort = header.getAttribute('data-sort') || 'none';
            const newSort = currentSort === 'asc' ? 'desc' : 'asc';
            
            // Resetear todos los headers
            table.querySelectorAll('th[data-column]').forEach(h => {
                h.removeAttribute('data-sort');
                h.querySelector('.sort-icon').className = 'sort-icon fas fa-sort';
            });
            
            // Aplicar al header actual
            header.setAttribute('data-sort', newSort);
            const icon = header.querySelector('.sort-icon');
            icon.className = newSort === 'asc' 
                ? 'sort-icon fas fa-sort-up' 
                : 'sort-icon fas fa-sort-down';
            
            sortTable(columnIndex, newSort);
        });
    });
    
    // Inicializar paginación
    updatePagination();
});