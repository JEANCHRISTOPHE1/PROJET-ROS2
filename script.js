function updateValues() {
	fetch('/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temp').innerText = data.temperature !== null ? data.temperature + " °C" : "-- °C";
                    document.getElementById('humi').innerText = data.humidite !== null ? data.humidite + " %" : "-- %";
                })
                .catch(error => console.error('Erreur:', error));
}

document.getElementById("portail-btn").addEventListener("click", function() {
	fetch('/portail', { method: "POST" })
                .then(response => response.json())
                .then(data => alert(data.message))
                .catch(error => console.error('Erreur:', error));
});
setInterval(updateValues, 1000);

//TYRANNOSAURE
