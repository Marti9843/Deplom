document.addEventListener('DOMContentLoaded', function() {
    // Елементи меню
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const body = document.body;

    // Перемикання меню
    function toggleMenu() {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        body.classList.toggle('menu-open');
    }

    // Ініціалізація меню
    function initMenu() {
        // Відкриття/закриття меню
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleMenu();
        });

        // Закриття меню при кліку на оверлей
        overlay.addEventListener('click', function() {
            toggleMenu();
        });

        // Закриття меню при кліку на пункт (для мобільних)
        document.querySelectorAll('.nav-link, .service-link').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    toggleMenu();
                }
            });
        });
    }

    // Підсвітка активного пункту
    function highlightActiveMenu() {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-link, .service-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    // Ініціалізація
    initMenu();
    highlightActiveMenu();

    // Адаптація при зміні розміру
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
            body.classList.remove('menu-open');
        }
    });
});