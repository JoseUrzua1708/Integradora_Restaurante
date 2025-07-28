document.addEventListener('DOMContentLoaded', () => {
    const contenedorProductos = document.querySelector('.row-productos');
    let pedido = [];
    let descuento = 0;

    function agregarProducto(id, nombre, precio) {
        pedido.push({ id, nombre, precio, cantidad: 1 });
        actualizarVista();
    }

    function actualizarVista() {
        const lista = document.getElementById('lista-pedido');
        const inputItems = document.getElementById('input-items');
        const totalElem = document.getElementById('total');
        const ivaElem = document.getElementById('iva');
        const subtotalElem = document.getElementById('subtotal');
        lista.innerHTML = '';
        let subtotal = 0;

        pedido.forEach((item, index) => {
            subtotal += item.precio * item.cantidad;
            lista.innerHTML += `
                <li class="list-group-item">
                    ${item.nombre} x ${item.cantidad}
                    <span>
                        $${(item.precio * item.cantidad).toFixed(2)}
                        <button class="btn btn-xs btn-danger" type="button" aria-label="Eliminar ${item.nombre}" onclick="eliminarProducto(${index})">&times;</button>
                    </span>
                </li>
            `;
        });

        let subtotalConDescuento = subtotal - descuento;
        if (subtotalConDescuento < 0) subtotalConDescuento = 0;

        const iva = subtotalConDescuento * 0.16;
        const totalConIVA = subtotalConDescuento + iva;

        subtotalElem.innerText = subtotal.toFixed(2);
        ivaElem.innerText = iva.toFixed(2);
        totalElem.innerText = totalConIVA.toFixed(2);
        inputItems.value = JSON.stringify(pedido);
        document.getElementById('descuento-aplicado').innerText = descuento > 0 ? `Descuento aplicado: $${descuento.toFixed(2)}` : '';
    }

    window.eliminarProducto = function(index) {
        pedido.splice(index, 1);
        descuento = 0;
        document.getElementById('descuento-aplicado').innerText = '';
        document.getElementById('codigo-promocion').value = '';
        actualizarVista();
    };

    contenedorProductos.addEventListener('click', e => {
        const target = e.target;
        if (target.classList.contains('agregar-producto')) {
            e.preventDefault();

            const id = parseInt(target.dataset.id);
            let itemExistente = pedido.find(i => i.id === id);
            if (itemExistente) {
                itemExistente.cantidad++;
            } else {
                const precio = parseFloat(target.dataset.precio);
                if (isNaN(precio)) {
                    alert("Error: el precio del producto no es válido");
                    return;
                }
                agregarProducto(id, target.dataset.nombre, precio);
            }
            actualizarVista();
        }
    });

    window.cancelarVenta = function() {
        if (confirm("¿Seguro que deseas cancelar la venta?")) {
            pedido = [];
            descuento = 0;
            document.getElementById('descuento-aplicado').innerText = '';
            document.getElementById('codigo-promocion').value = '';
            document.getElementById('mensaje-error').style.display = 'none';
            actualizarVista();
        }
    };

    window.validarVenta = function() {
        if (pedido.length === 0) {
            alert("Debe agregar al menos un producto antes de finalizar la venta");
            return false;
        }
        const tipo = document.getElementById('tipo-pedido').value;
        const metodo = document.getElementById('metodo-pago').value;

        if (!tipo) {
            alert("Seleccione un tipo de pedido");
            return false;
        }
        if (!metodo) {
            alert("Seleccione un método de pago");
            return false;
        }
        if (tipo === 'Domicilio') {
            const direccion = document.getElementById('direccion').value.trim();
            const telefono = document.getElementById('telefono').value.trim();
            if (!direccion) {
                alert("Ingrese la dirección de entrega");
                return false;
            }
            if (!telefono || !/^\d{7,15}$/.test(telefono)) {
                alert("Ingrese un teléfono válido (7 a 15 dígitos)");
                return false;
            }
        }
        if (tipo === 'Presencial') {
            const mesa = document.getElementById('mesa').value;
            if (!mesa) {
                alert("Seleccione una mesa");
                return false;
            }
        }
        return true;
    };

    window.aplicarPromocion = async function() {
        const codigoRaw = document.getElementById('codigo-promocion').value.trim();
        const codigo = codigoRaw.toUpperCase().replace(/\s+/g, '');
        const mensajeError = document.getElementById('mensaje-error');
        const descuentoElem = document.getElementById('descuento-aplicado');

        if (!codigo) {
            descuento = 0;
            descuentoElem.innerText = '';
            mensajeError.style.display = 'none';
            actualizarVista();
            return;
        }

        if (pedido.length === 0) {
            alert("Agregue productos al pedido antes de aplicar una promoción.");
            document.getElementById('codigo-promocion').value = '';
            return;
        }

        try {
            const response = await fetch('/ventas/aplicar_promocion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    codigo: codigo,
                    pedido: pedido
                })
            });

            if (!response.ok) throw new Error('Error en la respuesta del servidor');

            const data = await response.json();

            if (data.exito) {
                descuento = data.descuento;
                descuentoElem.innerText = `Descuento aplicado: $${descuento.toFixed(2)}`;
                mensajeError.style.display = 'none';
            } else {
                descuento = 0;
                descuentoElem.innerText = '';
                mensajeError.style.display = 'block';
                setTimeout(() => {
                    mensajeError.style.display = 'none';
                }, 3000);
            }
            actualizarVista();
        } catch (error) {
            console.error(error);
            alert('Error al aplicar la promoción, vuelve a intentarlo.');
        }
    };

    window.mostrarCamposAdicionales = function() {
        const tipo = document.getElementById('tipo-pedido').value;
        document.getElementById('campo-direccion').style.display = tipo === 'Domicilio' ? 'block' : 'none';
        document.getElementById('campo-mesa').style.display = tipo === 'Presencial' ? 'block' : 'none';
    };

    window.filtrarCategoria = function() {
        const seleccion = document.getElementById('filtro-categoria').value;
        document.querySelectorAll('.producto-card').forEach(card => {
            const claseCategoria = card.className.split(' ').find(c => c.startsWith('categoria-'));
            if (seleccion === 'todos') {
                card.style.display = 'block';
            } else if (claseCategoria === 'categoria-' + seleccion) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    };

    actualizarVista();
});
