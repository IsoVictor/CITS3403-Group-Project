document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profile-form');
    const profileName = document.getElementById('profile-name');
    const profileEmail = document.getElementById('profile-email'); 
    const profileUsername = document.getElementById('profile-username'); 

    profileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(profileForm);

        fetch(profileForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                profileName.textContent = `${data.firstname} ${data.lastname}`;
                profileEmail.textContent = data.email;
                profileUsername.textContent = data.username;
                const sessionUsername = "{{ session.get('username') }}"; // Get current session username
                if (data.username !== sessionUsername) {
                    const greetingListItem = document.getElementById('greeting-list-item');
                    const greetingLink = document.getElementById('greeting');
                    greetingLink.textContent = "Hello, " + data.username;
                    greetingListItem.removeChild(greetingLink);
                    greetingListItem.innerHTML += greetingLink.outerHTML;
            } 
        }else {
                console.error('Failed to update profile');
                if (data.errors) {
                    alert(JSON.stringify(data.errors));
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
