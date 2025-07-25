document.addEventListener('DOMContentLoaded', function() {
    // Configuración del teléfono
    const codigoPais = document.getElementById('codigo_pais');
    const telefonoInput = document.getElementById('telefono');
    const telefonoCompleto = document.getElementById('telefono_completo');
    
    // Configuración de moneda
    const tipoMoneda = document.getElementById('tipo_moneda');
    const simboloMoneda = document.getElementById('simbolo_moneda');
    const formulario = document.querySelector('.formulario');
    
    // Mapeo de símbolos de moneda (código ISO => símbolo)
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
    
    // Mapeo de patrones de teléfono por país (código => patrón)
    const patronesTelefono = {
        '1': '[0-9]{10}', // EEUU/Canadá
        '52': '[0-9]{10}', // México
        '54': '[0-9]{10,11}', // Argentina
        '55': '[0-9]{10,11}', // Brasil
        '56': '[0-9]{9,10}', // Chile
        '57': '[0-9]{10}', // Colombia
        '58': '[0-9]{10}', // Venezuela
        '51': '[0-9]{9}', // Perú
        '593': '[0-9]{9}', // Ecuador
        '502': '[0-9]{8}', // Guatemala
        '34': '[0-9]{9}', // España
        '33': '[0-9]{9}', // Francia
        '49': '[0-9]{10,11}', // Alemania
        '39': '[0-9]{9,10}', // Italia
        '44': '[0-9]{10,11}', // Reino Unido
        '86': '[0-9]{10,11}', // China
        '81': '[0-9]{9,10}', // Japón
        '82': '[0-9]{9,10}' // Corea del Sur
    };
    
    // Actualizar teléfono completo y patrón de validación
    function actualizarTelefono() {
        const codigo = codigoPais.value;
        const prefijo = codigoPais.options[codigoPais.selectedIndex].dataset.prefix;
        
        if (codigo && patronesTelefono[codigo]) {
            telefonoInput.pattern = patronesTelefono[codigo];
            telefonoInput.placeholder = getPlaceholderPorPais(codigo);
            telefonoInput.title = `Formato requerido: ${getPlaceholderPorPais(codigo)}`;
        }
        
        telefonoCompleto.value = prefijo + telefonoInput.value;
    }
    
    // Obtener placeholder según país
    function getPlaceholderPorPais(codigoPais) {
        const ejemplos = {
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
        return ejemplos[codigoPais] || 'Número local';
    }
    
    // Actualizar símbolo de moneda
    function actualizarMoneda() {
        const moneda = tipoMoneda.value;
        simboloMoneda.value = moneda ? simbolosMonedas[moneda] || '' : '';
    }
    
    // Validar horarios
    function validarHorarios() {
        const apertura = document.getElementById('Horario_Apertura').value;
        const cierre = document.getElementById('Horario_Cierre').value;
        
        if (apertura && cierre && apertura >= cierre) {
            alert('El horario de cierre debe ser posterior al de apertura');
            return false;
        }
        return true;
    }
    
    // Validar formulario completo
    function validarFormulario() {
        let valido = true;
        
        // Validar campos requeridos
        formulario.querySelectorAll('[required]').forEach(campo => {
            if (!campo.value.trim()) {
                campo.style.borderColor = '#e74c3c';
                campo.focus();
                alert(`El campo ${campo.labels[0].textContent} es obligatorio`);
                valido = false;
                return false;
            }
            campo.style.borderColor = '';
        });
        
        if (!valido) return false;
        
        // Validar teléfono
        if (!telefonoInput.value.match(telefonoInput.pattern)) {
            alert(`Número de teléfono inválido. Formato requerido: ${getPlaceholderPorPais(codigoPais.value)}`);
            telefonoInput.focus();
            return false;
        }
        
        // Validar moneda
        if (!tipoMoneda.value) {
            alert('Por favor seleccione un tipo de moneda');
            tipoMoneda.focus();
            return false;
        }
        
        // Validar horarios
        if (!validarHorarios()) {
            return false;
        }
        
        // Validar impuesto (0-100)
        const impuesto = parseFloat(document.getElementById('Impuesto').value);
        if (isNaN(impuesto) || impuesto < 0 || impuesto > 100) {
            alert('El impuesto debe ser un valor entre 0 y 100');
            document.getElementById('Impuesto').focus();
            return false;
        }
        
        return true;
    }
    
    // Event listeners
    codigoPais.addEventListener('change', actualizarTelefono);
    telefonoInput.addEventListener('input', actualizarTelefono);
    tipoMoneda.addEventListener('change', actualizarMoneda);
    
    // Validación del formulario al enviar
    formulario.addEventListener('submit', function(e) {
        actualizarTelefono();
        
        if (!validarFormulario()) {
            e.preventDefault();
            return false;
        }
        
        // Mostrar loader o feedback de envío
        const submitBtn = formulario.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Enviando...';
    });
    
    // Validación en tiempo real para campos numéricos
    document.getElementById('Impuesto').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9.]/g, '');
    });
    
    document.getElementById('Tiempo_Reserva_Min').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
    
    // Inicialización
    actualizarTelefono();
    actualizarMoneda();
    
    // Configurar tooltips para campos
    formulario.querySelectorAll('input, select, textarea').forEach(campo => {
        if (campo.required) {
            campo.title = 'Este campo es obligatorio';
        }
    });
});