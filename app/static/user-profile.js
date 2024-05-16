
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const profilePicture = document.getElementById('profile-picture');
    const defaultProfileImg = document.getElementById('default-profile-img');

    uploadBtn.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        const file = this.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload-profile-picture', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                profilePicture.src = data.file_url;
                defaultProfileImg.style.display = 'none';
            } else {
                console.error('Failed to upload profile picture');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
