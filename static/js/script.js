document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const videoFile = document.getElementById('videoFile').files[0];
    const language = document.getElementById('language').value;

    formData.append('video', videoFile);
    formData.append('language', language);

    // Show loading shimmer
    const transcriptionResult = document.getElementById('transcriptionResult');
    transcriptionResult.classList.add('loading');
    transcriptionResult.innerText = '';

    fetch('/transcribe', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          // Hide loading shimmer
          transcriptionResult.classList.remove('loading');
          transcriptionResult.innerText = data.transcription;
      })
      .catch(error => {
          console.error('Error:', error);
          // Hide loading shimmer
          transcriptionResult.classList.remove('loading');
          transcriptionResult.innerText = 'An error occurred while transcribing the video.';
      });
});

document.getElementById('toggleDarkMode').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    const icon = document.getElementById('toggleDarkMode');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
});
