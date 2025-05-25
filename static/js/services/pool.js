document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const scheduleContents = document.querySelectorAll('.schedule-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));

            // Add active class to clicked tab
            this.classList.add('active');

            // Get day from data attribute
            const day = this.getAttribute('data-day');

            // Hide all schedule contents
            scheduleContents.forEach(content => {
                content.classList.remove('active');
            });

            // Show selected day's schedule
            document.getElementById(day).classList.add('active');
        });
    });
});