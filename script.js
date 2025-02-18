var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('temperature_update', function(data) {
    document.getElementById('temperature').innerText = data.temperature.toFixed(2);
});

socket.on('humidity_update', function(data) {
    document.getElementById('humidity').innerText = data.humidity.toFixed(2);
});

