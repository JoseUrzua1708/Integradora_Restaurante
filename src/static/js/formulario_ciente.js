document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('clienteForm');
    const passwordInput = document.getElementById('contrasena');
    const confirmPasswordInput = document.getElementById('confirmar_contrasena');
    const passwordError = document.getElementById('password-error');
    const emailInput = document.getElementById('correo');
    const emailError = document.getElementById('email-error');
    const fechaNacimientoInput = document.getElementById('fecha_nacimiento');

    // Mostrar/ocultar contraseña
    if (document.querySelectorAll('.toggle-password')) {
        document.querySelectorAll('.toggle-password').forEach(icon => {
            icon.addEventListener('click', function() {
                const fieldId = this.getAttribute('onclick').match(/'([^']+)'/)[1];
                togglePassword(fieldId);
            });
        });
    }

    // Validación de contraseña
    if (passwordInput && confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', validatePassword);
        passwordInput.addEventListener('input', validatePassword);
    }

    // Validación de email
    if (emailInput) {
        emailInput.addEventListener('input', validateEmail);
    }

    // Validación de fecha de nacimiento
    if (fechaNacimientoInput) {
        fechaNacimientoInput.addEventListener('change', validateBirthDate);
    }

    // Envío del formulario
    form.addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault();
            showFormErrors();
        } else {
            showLoadingState();
        }
    });

    // Función para mostrar/ocultar contraseña
    function togglePassword(fieldId) {
        const field = document.getElementById(fieldId);
        const icon = field.nextElementSibling;
        
        if (field.type === 'password') {
            field.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            field.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

    // Validar contraseña
    function validatePassword() {
        if (!passwordInput || !confirmPasswordInput) return;

        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordError.textContent = 'Las contraseñas no coinciden';
            passwordError.style.display = 'block';
            confirmPasswordInput.classList.add('is-invalid');
            confirmPasswordInput.nextElementSibling.style.color = '#e74c3c';
            return false;
        } else if (passwordInput.value.length < 6) {
            passwordError.textContent = 'La contraseña debe tener al menos 6 caracteres';
            passwordError.style.display = 'block';
            passwordInput.classList.add('is-invalid');
            passwordInput.nextElementSibling.style.color = '#e74c3c';
            return false;
        } else if (!/(?=.*[A-Za-z])(?=.*\d)/.test(passwordInput.value)) {
            passwordError.textContent = 'La contraseña debe contener letras y números';
            passwordError.style.display = 'block';
            passwordInput.classList.add('is-invalid');
            passwordInput.nextElementSibling.style.color = '#e74c3c';
            return false;
        } else {
            passwordError.style.display = 'none';
            passwordInput.classList.remove('is-invalid');
            confirmPasswordInput.classList.remove('is-invalid');
            passwordInput.nextElementSibling.style.color = '';
            confirmPasswordInput.nextElementSibling.style.color = '';
            return true;
        }
    }

    // Validar email
    function validateEmail() {
        if (!emailInput) return true;

        const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
        
        if (emailInput.value && !emailRegex.test(emailInput.value)) {
            emailError.textContent = 'Por favor ingresa un correo electrónico válido';
            emailError.style.display = 'block';
            emailInput.classList.add('is-invalid');
            return false;
        } else {
            emailError.style.display = 'none';
            emailInput.classList.remove('is-invalid');
            return true;
        }
    }

    // Validar fecha de nacimiento (mayor de 18 años)
    function validateBirthDate() {
        if (!fechaNacimientoInput || !fechaNacimientoInput.value) return true;

        const hoy = new Date();
        const fechaNac = new Date(fechaNacimientoInput.value);
        let edad = hoy.getFullYear() - fechaNac.getFullYear();
        const mes = hoy.getMonth() - fechaNac.getMonth();
        
        if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
            edad--;
        }
        
        if (edad < 18) {
            fechaNacimientoInput.setCustomValidity('El cliente debe ser mayor de 18 años');
            fechaNacimientoInput.classList.add('is-invalid');
            return false;
        } else {
            fechaNacimientoInput.setCustomValidity('');
            fechaNacimientoInput.classList.remove('is-invalid');
            return true;
        }
    }

    // Validar todo el formulario
    function validateForm() {
        let isValid = true;
        
        // Validar campos requeridos
        form.querySelectorAll('[required]').forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        });

        // Validaciones específicas
        if (passwordInput && confirmPasswordInput) {
            isValid = validatePassword() && isValid;
        }
        
        isValid = validateEmail() && isValid;
        isValid = validateBirthDate() && isValid;

        return isValid;
    }

    // Mostrar errores del formulario
    function showFormErrors() {
        form.classList.add('shake');
        setTimeout(() => form.classList.remove('shake'), 500);
        
        // Desplazarse al primer error
        const firstError = form.querySelector('.is-invalid');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstError.focus();
        }
    }

    // Mostrar estado de carga
    function showLoadingState() {
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
        submitBtn.disabled = true;
    }

    // Validación en tiempo real para campos de texto (solo letras)
    document.querySelectorAll('input[pattern="[A-Za-záéíóúÁÉÍÓÚñÑ ]+"]').forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ ]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
        });
    });
});