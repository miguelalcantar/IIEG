const HEAT_MAP_CONF = {
    "radius": 40,
    // "maxOpacity": 1,
    "useLocalExtrema": true,
    latField: 'lat',
    lngField: 'lng',
    valueField: 'count'
};
const TITLE_LAYER    = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18});
const HEAT_MAP_LAYER = new HeatmapOverlay(HEAT_MAP_CONF);

const MAP = L.map('mapid', {
    center: [20.701628,-103.3983813],
    zoom: 12,
    layers: [TITLE_LAYER, HEAT_MAP_LAYER]
});

let mapServ = new MapService();
mapServ.mapCoordinates(HEAT_MAP_LAYER);

