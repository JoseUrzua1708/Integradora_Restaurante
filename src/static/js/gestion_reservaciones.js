function mostrarTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

document.getElementById('tipo').addEventListener('change', function () {
    const mesa = document.getElementById('campos-mesa');
    const evento = document.getElementById('campos-evento');

    if (this.value === 'mesa') {
        mesa.style.display = 'block';
        evento.style.display = 'none';
    } else {
        mesa.style.display = 'none';
        evento.style.display = 'block';
    }
});