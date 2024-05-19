// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  // Get the calendar element by its ID
  var calendarEl = document.getElementById('calendar');

  // Create a new FullCalendar instance
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth', // Set the initial view to display a month grid
    events: studyGroupEvents, // Set the array of study group events

    // Function to handle date click event
    dateClick: function (info) {
      // Redirect to the study groups page when a date is clicked
      window.location.href = "/study-groups";
    },

    // Function to handle event click event
    eventClick: function (info) {
      var event = info.event;
      // Create HTML markup for displaying event details
      var eventDetails = `
        <h3>${event.title}</h3>
        <p><strong>Date:</strong> ${event.start.toISOString().slice(0, 10)}</p>
        <p><strong>Location:</strong> ${event.extendedProps.location}</p>
        <p><strong>Time:</strong> ${event.extendedProps.time}</p>
      `;
      // Display the event details in the modal
      document.getElementById('event-details').innerHTML = eventDetails;
      openModal(); // Open the modal
    },

    // Function to handle event mouse enter event
    eventMouseEnter: function (info) {
      var event = info.event;
      // Create HTML markup for the tooltip
      var tooltip = `
        <div class="event-tooltip">
          <h3>${event.title}</h3>
          <p><strong>Date:</strong> ${event.start.toISOString().slice(0, 10)}</p>
          <p><strong>Location:</strong> ${event.extendedProps.location}</p>
          <p><strong>Time:</strong> ${event.extendedProps.time}</p>
        </div>
      `;
      // Create a new div element for the tooltip
      var tooltipEl = document.createElement('div');
      tooltipEl.className = 'tooltip';
      tooltipEl.innerHTML = tooltip;
      // Append the tooltip to the document body
      document.body.appendChild(tooltipEl);

      // Get the position of the event element
      var eventEl = info.el;
      var rect = eventEl.getBoundingClientRect();
      var tooltipWidth = tooltipEl.offsetWidth;
      var tooltipHeight = tooltipEl.offsetHeight;
      // Calculate the position of the tooltip
      var tooltipTop = rect.top - tooltipHeight - 10;
      var tooltipLeft = rect.left + (rect.width - tooltipWidth) / 2;
      // Set the position and style of the tooltip
      tooltipEl.style.position = 'absolute';
      tooltipEl.style.top = tooltipTop + 'px';
      tooltipEl.style.left = tooltipLeft + 'px';
      tooltipEl.style.zIndex = '1000';
    },

    // Function to handle event mouse leave event
    eventMouseLeave: function () {
      // Remove the tooltip element when the mouse leaves the event
      var tooltipEl = document.querySelector('.tooltip');
      if (tooltipEl) {
        tooltipEl.remove();
      }
    }
  });

  // Render the calendar
  calendar.render();

  // Get the modal and close button elements
  var modal = document.getElementById('event-modal');
  var closeBtn = document.getElementsByClassName('close')[0];

  // Function to open the modal
  function openModal() {
    modal.style.display = 'block';
  }

  // Function to close the modal when the close button is clicked
  closeBtn.onclick = function () {
    modal.style.display = 'none';
  };
});
