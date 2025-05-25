document.addEventListener('DOMContentLoaded', function() {
    // Обробка відправки форми
    const form = document.querySelector('.verify-email-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.verify-email-button');
            if (submitBtn) {
                submitBtn.disabled = true;
                const buttonText = submitBtn.querySelector('span');
                if (buttonText) {
                    buttonText.textContent = 'Відправка...';
                }

                // Додаємо індикатор завантаження
                const loader = document.createElement('span');
                loader.className = 'button-loader';
                submitBtn.appendChild(loader);
            }
        });
    }

    // Анімація для повідомлень про помилки
    const errorMessages = document.querySelectorAll('.message.error');
    errorMessages.forEach(msg => {
        msg.style.animation = 'shake 0.5s ease-in-out';
    });
});