class MapService{

    // urlBase = `http://192.168.43.208:5000`;
    urlBase = 'http://127.0.0.1:5000';

    constructor(){}

    mapCoordinates(map){
        $.ajax({
            type: `GET`,
            url: `${this.urlBase}/maps`,

            success: function(response){
                let locations = response.data.points;
                let latlon   = new Array(2);

                locations.forEach(element => {
                    UTMXYToLatLon(element[0],element[1],latlon);
                    L.circle([RadToDeg(latlon[0]),RadToDeg(latlon[1])], 10, {
                        color: 'red',
                        fillColor: '#f03',
                        fillOpacity: 0.5
                    }).addTo(map);
                });
            }
        });
    }
}