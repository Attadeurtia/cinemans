// Exemple d'intégration de Google Maps
function initMap() {
    var mapOptions = {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

// Charger la carte Google Maps
window.onload = function() {
    initMap();
};
