document.addEventListener('DOMContentLoaded', function() {
    console.log('Password reset confirm page initialized');

    // Перемикання видимості пароля для обох полів
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        const targetIds = togglePassword.getAttribute('data-target').split(',');

        togglePassword.addEventListener('click', function() {
            let allPassword = true;

            // Перевіряємо, чи всі поля є password
            targetIds.forEach(id => {
                const field = document.getElementById(id.trim());
                if (field && field.type !== 'password') {
                    allPassword = false;
                }
            });

            // Змінюємо тип для всіх полів
            targetIds.forEach(id => {
                const field = document.getElementById(id.trim());
                if (field) {
                    field.type = allPassword ? 'text' : 'password';
                }
            });

            // Оновлюємо іконку
            const icon = this.querySelector('.material-icons');
            if (icon) {
                icon.textContent = allPassword ? 'visibility_off' : 'visibility';
            }

            // Оновлюємо підказку
            this.setAttribute('aria-label',
                allPassword ? 'Приховати пароль' : 'Показати пароль');
        });
    }

    // Обробка відправки форми
    const form = document.querySelector('.password-reset-confirm-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.password-reset-confirm-button');
            if (submitBtn) {
                submitBtn.disabled = true;
                const buttonText = submitBtn.querySelector('span');
                if (buttonText) {
                    buttonText.textContent = 'Зміна...';
                }

                submitBtn.classList.add('loading');
                const loader = document.createElement('span');
                loader.className = 'button-loader';
                submitBtn.appendChild(loader);
            }
        });
    }

    // Анімація для помилок
    const errorElement = document.querySelector('.password-reset-confirm-error');
    if (errorElement) {
        errorElement.style.animation = 'shake 0.5s ease-in-out';
    }
});