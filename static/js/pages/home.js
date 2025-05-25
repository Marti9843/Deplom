document.addEventListener('DOMContentLoaded', function() {
    // Слайдер відгуків
    const testimonials = document.querySelector('.testimonials-slider');
    if (testimonials && window.innerWidth <= 768) {
        let currentIndex = 0;
        const items = testimonials.children;

        function showTestimonial(index) {
            for (let i = 0; i < items.length; i++) {
                items[i].style.display = i === index ? 'flex' : 'none';
            }
        }

        showTestimonial(currentIndex);

        setInterval(() => {
            currentIndex = (currentIndex + 1) % items.length;
            showTestimonial(currentIndex);
        }, 5000);
    }

    // Модальне вікно для відгуку
    const openModalBtn = document.getElementById('openFeedbackModal');
    const modal = document.getElementById('feedbackModal');
    const closeModalBtn = document.querySelector('.close-modal');

    if (openModalBtn) {
        openModalBtn.addEventListener('click', function() {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    }

    closeModalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Обробка рейтингу
    const stars = document.querySelectorAll('.rating-selector .material-icons');
    let selectedRating = 0;

    stars.forEach(star => {
        star.addEventListener('click', function() {
            selectedRating = parseInt(this.getAttribute('data-rating'));
            updateStars(selectedRating);
        });

        star.addEventListener('mouseover', function() {
            const hoverRating = parseInt(this.getAttribute('data-rating'));
            updateStars(hoverRating);
        });

        star.addEventListener('mouseout', function() {
            updateStars(selectedRating);
        });
    });

    function updateStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
                star.textContent = 'star';
            } else {
                star.classList.remove('active');
                star.textContent = 'star_outline';
            }
        });
    }

    // Відправка форми
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const feedbackText = this.querySelector('textarea').value;

            if (!selectedRating) {
                alert('Будь ласка, оберіть рейтинг');
                return;
            }

            if (!feedbackText.trim()) {
                alert('Будь ласка, напишіть ваш відгук');
                return;
            }

            // Тут можна додати AJAX-запит для відправки на сервер
            console.log('Відгук відправлено:', {
                rating: selectedRating,
                text: feedbackText
            });

            alert('Дякуємо за ваш відгук!');
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            this.reset();
            selectedRating = 0;
            updateStars(0);
        });
    }
});