document.addEventListener('DOMContentLoaded', () => {
    const hamburgerBtn = document.querySelector('.hamburger-btn');
    const mainNav = document.getElementById('main-nav');

    if (hamburgerBtn && mainNav) {
        hamburgerBtn.addEventListener('click', () => {
            mainNav.classList.toggle('active');

            const expanded = hamburgerBtn.getAttribute('aria-expanded') === 'true';
            hamburgerBtn.setAttribute('aria-expanded', String(!expanded));

            // Alternar clase para bloquear scroll en body
            document.body.classList.toggle('menu-open', mainNav.classList.contains('active'));
        });

        // Opcional: cerrar menú si clicas fuera del menú (en el fondo oscuro)
        mainNav.addEventListener('click', (e) => {
            if (e.target === mainNav && mainNav.classList.contains('active')) {
                mainNav.classList.remove('active');
                hamburgerBtn.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('menu-open');
            }
        });
    }
});
