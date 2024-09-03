document.querySelector('.btn-reset').addEventListener('click', function() {
    var audio = new Audio(src='{{result}}');
    audio.play();
});

// ../static/voice/voice_8.mp3