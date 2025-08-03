function cargarSubcategorias(categoriaId) {
    fetch(`/subcategorias_por_categoria/${categoriaId}`)
        .then(response => response.json())
        .then(data => {
            const subSelect = document.getElementById('subcategoria');
            subSelect.innerHTML = '<option value="">Selecciona una subcategoría</option>';
            data.forEach(sub => {
                const option = document.createElement('option');
                option.value = sub.ID;
                option.textContent = sub.Nombre;
                subSelect.appendChild(option);
            });
        });
}