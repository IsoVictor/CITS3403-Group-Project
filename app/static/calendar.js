var studyGroupEvents = [];

fetch('/api/study-group-events')
    .then(response => response.json())
    .then(data => {
        studyGroupEvents = data;
        initializeCalendar();
    })
    .catch(error => {
        console.error('Error fetching study group events:', error);
    });

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
});
