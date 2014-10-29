var map, data;
var markers = [];
var ZOOM_THRESH = 5;


function initialize() {
	var mapOptions = {
		zoom: 5,
		center: new google.maps.LatLng(0, 0),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	setFusionTableLayer();

	google.maps.event.addListener(map, 'idle', resetMap);

	function resetMap() {
		sendMapBounds();
		zoom = map.getZoom();

		if(zoom <= ZOOM_THRESH) {
			clearPoints();
		}
	}

  function sendMapBounds() {
  	var bounds = map.getBounds().toUrlValue().split(",");  // lat_min,long_min,lat_max,long_max
  	console.log(bounds);
  	var lat_min = bounds[0];
  	var long_min = bounds[1];
  	var lat_max = bounds[2];
  	var long_max = bounds[3];

  	var request = new XMLHttpRequest();
  	var requestString = "/get_earthquakes" + "?lat_min=" + lat_min + "&long_min=" + long_min + "&lat_max=" + lat_max + "&long_max=" + long_max;
		request.open("get", requestString);
		request.send();

  	request.onreadystatechange = function() {
  		if (request.readyState == 4) {
  			earthquakes = JSON.parse(request.responseText);
  			if(zoom > ZOOM_THRESH) {
  				plotPoints();
  			}
    	}
  	}
  }

	function plotPoints() {
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);

			var markerSize = .04 * Math.pow(eq[6], 4);

			var eventName = eq[1];
			var icon = {
				url: '/static/beachballs2/' + eventName + '.svg',
				scaledSize: new google.maps.Size(markerSize, markerSize),
				anchor: new google.maps.Point(markerSize / 2, markerSize / 2)
			};

	    var marker = new google.maps.Marker({
	      position: latLng,
	      map: map,
	      icon: icon
	    });

	    markers.push(marker);
		})
	}

	function clearPoints() {
		for (var i = 0; i < markers.length; i++) {
    	markers[i].setMap(null);
  	}
	}

	function setFusionTableLayer() {
		layer = new google.maps.FusionTablesLayer({
			query: {
      	select: 'Location',
      	from: '1cWhh3dEaejEtV4TqnV0djQaepkAJ-ASmWDAZuuTt'
    	},
			styles: [{
			  markerOptions: {
			    iconName: 'small_yellow'
			  }
			}, 
			{
			 	where: 'Depth < 70',
			  markerOptions: {
			    iconName: 'small_red'
			  }
			}, 
			{
			 	where: 'Depth > 300',
			    markerOptions: {
			      iconName: 'small_blue'
			    }
			}]
		});
  	layer.setMap(map);
	}

	function setHeatMap() {
		var heatmapData = [];
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);
			heatmapData.push(latLng);
		})

  	var heatmap = new google.maps.visualization.HeatmapLayer({
    	data: heatmapData
  	});

  	heatmap.setMap(map);
	}
}

google.maps.event.addDomListener(window, 'load', initialize);