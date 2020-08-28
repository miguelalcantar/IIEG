class MapService{

    urlBase = `http://127.0.0.1:5000`;

    constructor(){}

    mapCoordinates(heatMap){
        $.ajax({
            type: `GET`,
            url: `${this.urlBase}/maps`,
            success: function(response){
                let points  = response.data.points;
                let latlon  = new Array(2);
                let total   = new Array();
                let counts  = new Array();
                let data    = new Array();
                //Convert proyections to geografic
                points = points.map(function(point){               
                    const TOTAL_DECIMAL = 1000;

                    UTMXYToLatLon(point[0], point[1], latlon);
                    
                    let lat  = RadToDeg(latlon[0]);
                    let long = RadToDeg(latlon[1]);

                    lat  = Math.round(lat  * TOTAL_DECIMAL) / TOTAL_DECIMAL;
                    long = Math.round(long * TOTAL_DECIMAL) / TOTAL_DECIMAL;

                    return [lat, long];
                });
                //Count rep coordinates
                for (let element in points){     
                    counts[points[element]] = 1 + (counts[points[element]] || 0);       
                }
                //Create new array with data to set on heatmap.js and remove keys to count max on array
                for (let element in counts){    
                    let coord = element.split(',');

                    data.push({  
                        'lat' : coord[0],
                        'lng' : coord[1],
                        'count' : counts[element]
                    });  
                    total.push(counts[element]);        
                }
                heatMap.setData({max: Math.max(...total),data: data})
            }
        });
    }
}