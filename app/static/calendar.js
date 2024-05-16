// calendar.js
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar-container');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [],
        eventClick: function(info) {
            // Handle event click if needed
        }
    });
    calendar.render();

    var eventForm = document.getElementById('event-form');
    var eventList = document.getElementById('event-list');

    // Load events from the server
    loadEvents();

    eventForm.addEventListener('submit', function(e) {
        e.preventDefault();
        var title = document.getElementById('event-title').value;
        var date = document.getElementById('event-date').value;

        // Send event data to the server
        saveEvent(title, date);
    });

    function loadEvents() {
        // Make an AJAX request to load events from the server
        fetch('/events')
            .then(response => response.json())
            .then(data => {
                // Clear the event list
                eventList.innerHTML = '';

                // Add events to the calendar and event list
                data.events.forEach(event => {
                    calendar.addEvent({
                        title: event.title,
                        start: event.date
                    });
                    addEventToList(event);
                });
            })
            .catch(error => {
                console.error('Error loading events:', error);
            });
    }

    function saveEvent(title, date) {
        // Make an AJAX request to save the event to the server
        fetch('/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, date })
        })
            .then(response => response.json())
            .then(data => {
                // Add the event to the calendar and event list
                calendar.addEvent({
                    title: data.title,
                    start: data.date
                });
                addEventToList(data);
            })
            .catch(error => {
                console.error('Error saving event:', error);
            });
    }

    function deleteEvent(eventId) {
        // Make an AJAX request to delete the event from the server
        fetch(`/events/${eventId}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                // Remove the event from the calendar
                calendar.getEventById(eventId).remove();

                // Remove the event from the event list
                var listItem = eventList.querySelector(`li button[onclick="deleteEvent(${eventId})"]`).parentNode;
                eventList.removeChild(listItem);
            })
            .catch(error => {
                console.error('Error deleting event:', error);
            });
    }
});

    function addEventToList(event) {
        var listItem = document.createElement('li');
        listItem.textContent = event.title + ' - ' + event.date;
        eventList.appendChild(listItem);
    }
});