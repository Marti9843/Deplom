document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('id_service');
    const activitySelect = document.getElementById('id_activity');

    // Динамічне завантаження занять при зміні послуги
    serviceSelect.addEventListener('change', function() {
        const serviceId = this.value;
        fetch(`/load-activities/?service_id=${serviceId}`)
            .then(response => response.json())
            .then(data => {
                activitySelect.innerHTML = '';
                data.forEach(activity => {
                    const option = document.createElement('option');
                    option.value = activity.id;
                    option.textContent = activity.name;
                    activitySelect.appendChild(option);
                });
            });
    });

    // Обробка форми
    document.getElementById('booking-form').addEventListener('submit', function(e) {
        e.preventDefault();
        // Тут код для відправки даних на сервер
    });
});