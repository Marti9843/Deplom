document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація перемикання видимості пароля
    function initPasswordToggle() {
        const toggleBtns = document.querySelectorAll('.toggle-password');

        toggleBtns.forEach(btn => {
            const targetIds = btn.getAttribute('data-targets').split(',');

            btn.addEventListener('click', function() {
                const isPressed = this.getAttribute('aria-pressed') === 'true';
                const newState = !isPressed;

                targetIds.forEach(id => {
                    const input = document.getElementById(id);
                    if (input) {
                        input.type = newState ? 'text' : 'password';
                    }
                });

                this.setAttribute('aria-pressed', newState);
                this.setAttribute('aria-label', newState ? 'Приховати пароль' : 'Показати пароль');

                const icon = this.querySelector('.material-icons');
                if (icon) {
                    icon.textContent = newState ? 'visibility_off' : 'visibility';
                }
            });
        });
    }

    // Обробка відправки форми
    function initFormSubmit() {
        const form = document.querySelector('.profile-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.profile-button');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                const buttonText = submitBtn.querySelector('span:first-child');
                if (buttonText) {
                    buttonText.textContent = 'Збереження...';
                }
            }
        });
    }

    // Закриття повідомлень
    function initMessageClose() {
        document.querySelectorAll('.message-close').forEach(btn => {
            btn.addEventListener('click', function() {
                this.closest('.message').style.opacity = '0';
                setTimeout(() => this.closest('.message').remove(), 300);
            });
        });
    }

    // Автоматичне закриття повідомлень через 5 секунд
    function autoCloseMessages() {
        document.querySelectorAll('.message').forEach(msg => {
            setTimeout(() => {
                msg.style.transition = 'opacity 0.3s ease';
                msg.style.opacity = '0';
                setTimeout(() => msg.remove(), 300);
            }, 5000);
        });
    }

    // Валідація паролів
    function initPasswordValidation() {
        const newPassword1 = document.getElementById('id_new_password1');
        const newPassword2 = document.getElementById('id_new_password2');

        if (newPassword1 && newPassword2) {
            newPassword2.addEventListener('input', function() {
                if (newPassword1.value !== newPassword2.value) {
                    newPassword2.setCustomValidity('Паролі не співпадають');
                } else {
                    newPassword2.setCustomValidity('');
                }
            });
        }
    }

    // Ініціалізація всіх функцій
    initPasswordToggle();
    initFormSubmit();
    initMessageClose();
    autoCloseMessages();
    initPasswordValidation();
});