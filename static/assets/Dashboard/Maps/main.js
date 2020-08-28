let map = L.map('mapid', {
    center: [20.727859, -103.404007],
    zoom: 11
});

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

let mapServ = new MapService();
mapServ.mapCoordinates(map);