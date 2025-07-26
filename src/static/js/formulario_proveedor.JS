document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(event) {
        let isValid = true;
        
        // Validar empresa
        const empresa = document.getElementById('Nombre_Empresa');
        if (empresa.value.trim().length < 3) {
            document.getElementById('error-empresa').textContent = 'Mínimo 3 caracteres';
            isValid = false;
        } else {
            document.getElementById('error-empresa').textContent = '';
        }
        
        // Validar contacto
        const contacto = document.getElementById('Contacto_Principal');
        if (contacto.value.trim().length < 5) {
            document.getElementById('error-contacto').textContent = 'Mínimo 5 caracteres';
            isValid = false;
        } else {
            document.getElementById('error-contacto').textContent = '';
        }
        
        // Validar teléfono
        const telefono = document.getElementById('Telefono');
        if (!/^\d{10}$/.test(telefono.value)) {
            document.getElementById('error-telefono').textContent = 'Debe tener 10 dígitos';
            isValid = false;
        } else {
            document.getElementById('error-telefono').textContent = '';
        }
        
        // Validar email
        const email = document.getElementById('Email');
        if (!/^[\w.-]+@[\w.-]+\.\w+$/.test(email.value)) {
            document.getElementById('error-email').textContent = 'Ingrese un email válido';
            isValid = false;
        } else {
            document.getElementById('error-email').textContent = '';
        }
        
        // Validar dirección
        const direccion = document.getElementById('Direccion');
        if (direccion.value.trim().length < 10) {
            document.getElementById('error-direccion').textContent = 'Mínimo 10 caracteres';
            isValid = false;
        } else {
            document.getElementById('error-direccion').textContent = '';
        }
        
        // Validar tipo
        const tipo = document.getElementById('Tipo_Proveedor');
        if (tipo.value === '') {
            document.getElementById('error-tipo').textContent = 'Seleccione un tipo';
            isValid = false;
        } else {
            document.getElementById('error-tipo').textContent = '';
        }
        
        if (!isValid) {
            event.preventDefault();
        }
    });
    
    // Validación en tiempo real
    const fields = ['Nombre_Empresa', 'Contacto_Principal', 'Telefono', 'Email', 'Direccion'];
    fields.forEach(field => {
        document.getElementById(field).addEventListener('input', function() {
            document.getElementById(`error-${field.toLowerCase()}`).textContent = '';
        });
    });
});