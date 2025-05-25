document.addEventListener('DOMContentLoaded', function() {
    console.log('Login page initialized');

    // Ініціалізація перемикання видимості пароля
    function initPasswordToggle() {
        const toggleBtn = document.querySelector('.toggle-password');
        const passwordInput = document.getElementById('password');

        if (!toggleBtn || !passwordInput) {
            console.error('Required elements not found');
            return;
        }

        // Встановлюємо початковий стан
        toggleBtn.setAttribute('aria-label', 'Показати пароль');

        toggleBtn.addEventListener('click', function() {
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';

            // Оновлюємо іконку
            const icon = this.querySelector('.material-icons');
            if (icon) {
                icon.textContent = isPassword ? 'visibility_off' : 'visibility';
            }

            // Оновлюємо підказку
            this.setAttribute('aria-label',
                isPassword ? 'Приховати пароль' : 'Показати пароль');
        });
    }

    // Обробка відправки форми
    function initFormSubmit() {
        const form = document.querySelector('.login-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.login-button');
            if (submitBtn) {
                submitBtn.disabled = true;
                const buttonText = submitBtn.querySelector('span');
                if (buttonText) {
                    buttonText.textContent = 'Вхід...';
                }

                submitBtn.classList.add('loading');
                const loader = document.createElement('span');
                loader.className = 'button-loader';
                submitBtn.appendChild(loader);
            }
        });
    }

    // Ініціалізація кнопки GitHub
    function initGitHubLogin() {
        const githubBtn = document.querySelector('.social-login.github');
        if (githubBtn) {
            githubBtn.addEventListener('click', function() {
                window.location.href = '/accounts/github/login/';
            });
        }
    }

    // Запуск всіх функцій
    initPasswordToggle();
    initFormSubmit();
    initGitHubLogin();

    // Анімація для помилок
    const errorElement = document.querySelector('.login-error');
    if (errorElement) {
        errorElement.style.animation = 'shake 0.5s ease-in-out';
    }
});