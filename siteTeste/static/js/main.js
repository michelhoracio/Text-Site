document.getElementById('tts-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const text = document.getElementById('text').value;
    const voice = document.getElementById('voice').value;
    const rate = document.getElementById('rate').value;
    const pitch = document.getElementById('pitch').value;
    const formData = new FormData();
    formData.append('text', text);
    formData.append('voice', voice);
    formData.append('rate', rate);
    formData.append('pitch', pitch);

    const response = await fetch('/synthesize', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        const audio = document.getElementById('audio');
        audio.src = audioUrl;
        audio.style.display = 'block';
        audio.play();
    } else {
        console.error('Error:', response.statusText);
    }
});

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
            console.log('Service Worker registrado com sucesso:', registration);
        }, function(error) {
            console.log('Falha ao registrar o Service Worker:', error);
        });
    });
}
