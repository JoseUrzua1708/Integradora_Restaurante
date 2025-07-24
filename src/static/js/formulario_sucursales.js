document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sucursalForm');
    const telefonoInput = document.getElementById('Telefono');
    const horarioApertura = document.getElementById('Horario_Apertura');
    const horarioCierre = document.getElementById('Horario_Cierre');
    
    // Validación de teléfono
    telefonoInput.addEventListener('input', function(e) {
        this.value = this.value.replace(/\D/g, '').slice(0, 10);
    });
    
    // Validación de horarios
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Limpiar mensajes de error previos
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        
        // Validar teléfono
        if(telefonoInput.value.length !== 10) {
            showError(telefonoInput, 'El teléfono debe tener 10 dígitos');
            isValid = false;
        }
        
        // Validar horarios
        if(horarioApertura.value && horarioCierre.value) {
            if(horarioApertura.value >= horarioCierre.value) {
                showError(horarioCierre, 'El horario de cierre debe ser posterior al de apertura');
                isValid = false;
            }
        }
        
        if(!isValid) {
            e.preventDefault();
            // Mostrar mensaje general de error
            const errorAlert = document.createElement('div');
            errorAlert.className = 'error-message';
            errorAlert.style.marginBottom = '15px';
            errorAlert.style.color = '#e74c3c';
            errorAlert.style.fontWeight = '500';
            errorAlert.innerHTML = '<i class="fas fa-exclamation-circle"></i> Por favor corrija los errores en el formulario';
            form.prepend(errorAlert);
        }
    });
    
    function showError(input, message) {
        const error = document.createElement('span');
        error.className = 'error-message';
        error.textContent = message;
        input.parentNode.appendChild(error);
        input.style.borderColor = '#e74c3c';
        
        input.addEventListener('input', function clearError() {
            error.remove();
            input.style.borderColor = '#d5c4a1';
            input.removeEventListener('input', clearError);
        });
    }
    
    // Establecer fecha mínima (hoy) para fecha de apertura
    const fechaApertura = document.getElementById('Fecha_Apertura');
    const today = new Date().toISOString().split('T')[0];
    fechaApertura.min = today;
});