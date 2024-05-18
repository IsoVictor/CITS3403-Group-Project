document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: studyGroupEvents,
        dateClick: function (info) {
            // Redirect to the study groups page when a date is clicked
            window.location.href = "/study-groups";
        },
        eventClick: function (info) {
            var event = info.event;
            var eventDetails = `
                <h3>${event.title}</h3>
                <p><strong>Date:</strong> ${event.start.toISOString().slice(0, 10)}</p>
                <p><strong>Location:</strong> ${event.extendedProps.location}</p>
                <p><strong>Time:</strong> ${event.extendedProps.time}</p>
            `;
            document.getElementById('event-details').innerHTML = eventDetails;
            document.getElementById('delete-event').dataset.eventId = event.id;
            openModal();
        },
        eventMouseEnter: function (info) {
            var event = info.event;
            var tooltip = `
                <div class="event-tooltip">
                    <h3>${event.title}</h3>
                    <p><strong>Date:</strong> ${event.start.toISOString().slice(0, 10)}</p>
                    <p><strong>Location:</strong> ${event.extendedProps.location}</p>
                    <p><strong>Time:</strong> ${event.extendedProps.time}</p>
                </div>
            `;
            var tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.innerHTML = tooltip;
            document.body.appendChild(tooltipEl);

            var eventEl = info.el;
            var rect = eventEl.getBoundingClientRect();
            var tooltipWidth = tooltipEl.offsetWidth;
            var tooltipHeight = tooltipEl.offsetHeight;
            var tooltipTop = rect.top - tooltipHeight - 10;
            var tooltipLeft = rect.left + (rect.width - tooltipWidth) / 2;

            tooltipEl.style.position = 'absolute';
            tooltipEl.style.top = tooltipTop + 'px';
            tooltipEl.style.left = tooltipLeft + 'px';
            tooltipEl.style.zIndex = '1000';
        },
        eventMouseLeave: function () {
            var tooltipEl = document.querySelector('.tooltip');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        }
    });
    calendar.render();

    var modal = document.getElementById('event-modal');
    var closeBtn = document.getElementsByClassName('close')[0];

    function openModal() {
        modal.style.display = 'block';
    }

    closeBtn.onclick = function () {
        modal.style.display = 'none';
    };

    var eventForm = document.getElementById('event-form');
    var deleteEventBtn = document.getElementById('delete-event');

    eventForm.onsubmit = function (e) {
        e.preventDefault();
        var title = document.getElementById('event-title').value;
        var date = document.getElementById('event-date').value;
        var eventId = e.target.dataset.eventId;

        if (eventId) {
            // Update existing event
            fetch(`/edit-event/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: title, date: date })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        calendar.refetchEvents();
                        modal.style.display = 'none';
                    } else {
                        alert('Failed to update event. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        } else {
            // Add new event
            fetch('/add-event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: title, date: date })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        calendar.refetchEvents();
                        modal.style.display = 'none';
                    } else {
                        alert('Failed to add event. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        }
    };

    deleteEventBtn.onclick = function () {
        var eventId = deleteEventBtn.dataset.eventId;
        if (eventId) {
            fetch('/delete-event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ eventId: eventId })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        calendar.refetchEvents();
                        modal.style.display = 'none';
                    } else {
                        alert('Failed to delete event. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        }
    };
});
