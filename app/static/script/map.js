var map = L.map('map').fitWorld();

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
// map.locate({setView: true, maxZoom: 8}); 
// map.panTo(new L.LatLng(40.737, -73.923));

map.setView(new L.LatLng(38.44,-96.56), 4);