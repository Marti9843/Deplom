document.addEventListener('DOMContentLoaded', function() {
    console.log('Password reset page initialized');

    // Обробка відправки форми
    const form = document.querySelector('.password-reset-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.password-reset-button');
            if (submitBtn) {
                submitBtn.disabled = true;
                const buttonText = submitBtn.querySelector('span');
                if (buttonText) {
                    buttonText.textContent = 'Відправка...';
                }

                submitBtn.classList.add('loading');
                const loader = document.createElement('span');
                loader.className = 'button-loader';
                submitBtn.appendChild(loader);
            }
        });
    }

    // Анімація для помилок
    const errorElement = document.querySelector('.password-reset-error');
    if (errorElement) {
        errorElement.style.animation = 'shake 0.5s ease-in-out';
    }
});