document.addEventListener('DOMContentLoaded', function() {
    // Element references
    const codigoPais = document.getElementById('codigo_pais');
    const telefonoInput = document.getElementById('telefono');
    const telefonoCompleto = document.getElementById('Telefono'); // Changed to match hidden field
    const tipoMoneda = document.getElementById('Moneda'); // Changed to match select ID
    const simboloMoneda = document.getElementById('simbolo_moneda');
    const formulario = document.querySelector('.formulario');
    
    // Currency symbol mapping (ISO code => symbol)
    const simbolosMonedas = {
        'USD': 'US$',
        'EUR': '€',
        'JPY': '¥',
        'GBP': '£',
        'MXN': '$',
        'BRL': 'R$',
        'COP': 'COL$',
        'CLP': 'CLP$',
        'PEN': 'S/',
        'ARS': 'AR$',
        'CAD': 'CA$',
        'AUD': 'AU$',
        'CNY': 'CN¥'
    };
    
    // Phone patterns by country (code => pattern)
    const patronesTelefono = {
        '1': '[0-9]{10}',     // US/Canada
        '52': '[0-9]{10}',    // Mexico
        '54': '[0-9]{10,11}', // Argentina
        '55': '[0-9]{10,11}', // Brazil
        '56': '[0-9]{9,10}',  // Chile
        '57': '[0-9]{10}',    // Colombia
        '58': '[0-9]{10}',    // Venezuela
        '51': '[0-9]{9}',     // Peru
        '593': '[0-9]{9}',    // Ecuador
        '502': '[0-9]{8}',    // Guatemala
        '34': '[0-9]{9}',     // Spain
        '33': '[0-9]{9}',     // France
        '49': '[0-9]{10,11}', // Germany
        '39': '[0-9]{9,10}',  // Italy
        '44': '[0-9]{10,11}', // UK
        '86': '[0-9]{10,11}', // China
        '81': '[0-9]{9,10}',  // Japan
        '82': '[0-9]{9,10}'   // South Korea
    };
    
    // Initialize phone field if editing
    function initializePhone() {
        if (telefonoCompleto.value) {
            const phoneParts = telefonoCompleto.value.split(' ');
            if (phoneParts.length > 1) {
                telefonoInput.value = phoneParts.slice(1).join(' ');
            }
        }
    }
    
    // Update complete phone number and validation pattern
    function updatePhone() {
        const codigo = codigoPais.value;
        const prefijo = codigoPais.options[codigoPais.selectedIndex].dataset.prefix || '';
        const numero = telefonoInput.value.trim();
        
        // Update validation pattern
        if (codigo && patronesTelefono[codigo]) {
            telefonoInput.pattern = patronesTelefono[codigo];
            telefonoInput.placeholder = getPhonePlaceholder(codigo);
            telefonoInput.title = `Formato requerido: ${getPhonePlaceholder(codigo)}`;
        }
        
        // Update complete phone (hidden field)
        telefonoCompleto.value = numero ? `${prefijo} ${numero}` : '';
    }
    
    // Get phone placeholder by country
    function getPhonePlaceholder(countryCode) {
        const examples = {
            '1': 'ej. 5551234567',
            '52': 'ej. 5512345678',
            '54': 'ej. 91123456789',
            '55': 'ej. 21987654321',
            '56': 'ej. 221234567',
            '57': 'ej. 6012345678',
            '58': 'ej. 4121234567',
            '51': 'ej. 987654321',
            '593': 'ej. 991234567',
            '502': 'ej. 51234567',
            '34': 'ej. 612345678',
            '33': 'ej. 612345678',
            '49': 'ej. 1711234567',
            '39': 'ej. 3123456789',
            '44': 'ej. 7912345678',
            '86': 'ej. 13123456789',
            '81': 'ej. 9012345678',
            '82': 'ej. 1023456789'
        };
        return examples[countryCode] || 'Número local';
    }
    
    // Update currency symbol
    function updateCurrency() {
        const currency = tipoMoneda.value;
        simboloMoneda.value = currency ? simbolosMonedas[currency] || '' : '';
    }
    
    // Validate business hours
    function validateHours() {
        const opening = document.getElementById('Horario_Apertura').value;
        const closing = document.getElementById('Horario_Cierre').value;
        
        if (opening && closing && opening >= closing) {
            showError('El horario de cierre debe ser posterior al de apertura');
            return false;
        }
        return true;
    }
    
    // Show error message
    function showError(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        // Remove existing error if any
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
        
        // Insert after the form title
        const title = document.querySelector('h1');
        title.insertAdjacentElement('afterend', errorElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => errorElement.remove(), 5000);
    }
    
    // Validate complete form
    function validateForm() {
        // Validate required fields
        const requiredFields = formulario.querySelectorAll('[required]');
        for (const field of requiredFields) {
            if (!field.value.trim()) { // Empty value
                field.focus();
                showError(`El campo ${field.labels[0].textContent} es obligatorio`);
                return false;


            }
        }
        
        // Validate phone format
        if (telefonoInput.value && !telefonoInput.value.match(telefonoInput.pattern)) {
            showError(`Número de teléfono inválido. Formato requerido: ${getPhonePlaceholder(codigoPais.value)}`);
            telefonoInput.focus();
            return false;
        }
        
        // Validate currency
        if (!tipoMoneda.value) {
            showError('Por favor seleccione un tipo de moneda');
            tipoMoneda.focus();
            return false;
        }
        
        // Validate hours
        if (!validateHours()) {
            return false;
        }
        
        // Validate tax (0-100)
        const tax = parseFloat(document.getElementById('Impuesto').value);
        if (isNaN(tax)) {
            showError('El impuesto debe ser un número válido');
            document.getElementById('Impuesto').focus();
            return false;
        }
        
        if (tax < 0 || tax > 100) {
            showError('El impuesto debe ser un valor entre 0 y 100');
            document.getElementById('Impuesto').focus();
            return false;
        }
        
        // Validate reservation time (minimum 1 minute)
        const reservationTime = parseInt(document.getElementById('Tiempo_Reserva_Min').value);
        if (isNaN(reservationTime)) {
            showError('El tiempo de reserva debe ser un número válido');
            document.getElementById('Tiempo_Reserva_Min').focus();
            return false;
        }
        
        if (reservationTime < 1) {
            showError('El tiempo mínimo de reserva debe ser al menos 1 minuto');
            document.getElementById('Tiempo_Reserva_Min').focus();
            return false;
        }
        
        return true;
    }
    
    // Format numeric inputs
    function formatNumericInput(input) {
        input.value = input.value.replace(/[^0-9]/g, '');
    }
    
    // Event listeners
    codigoPais.addEventListener('change', updatePhone);
    telefonoInput.addEventListener('input', updatePhone);
    tipoMoneda.addEventListener('change', updateCurrency);
    
    // Form submission
    formulario.addEventListener('submit', function(e) {
        updatePhone(); // Ensure phone is properly formatted
        
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        const submitBtn = formulario.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    });
    
    // Numeric input validation
    document.getElementById('Impuesto').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9.]/g, '');
    });
    
    document.getElementById('Tiempo_Reserva_Min').addEventListener('input', function() {
        formatNumericInput(this);
    });
    
    // Initialize
    initializePhone();
    updatePhone();
    updateCurrency();
});