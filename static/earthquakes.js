var map, data;
var MIN_BEACHBALL_ZOOM = 5;

function initialize() {
	var mapOptions = {
		zoom: 2,
		center: new google.maps.LatLng(0, 0),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);

	var zoomLevel = map.getZoom();
	if(zoomLevel < MIN_BEACHBALL_ZOOM) {
		setHeatMap(earthquakes);
	} else {
		plotPoints(earthquakes);
	}

	google.maps.event.addListener(map, 'zoom_changed', function() {
		var oldZoomLevel = zoomLevel;
		zoomLevel = map.getZoom();
		sendBounds();

		if(oldZoomLevel < MIN_BEACHBALL_ZOOM && zoomLevel >= MIN_BEACHBALL_ZOOM) {
			plotPoints(earthquakes);
		}

		if(oldZoomLevel >= MIN_BEACHBALL_ZOOM && zoomLevel < MIN_BEACHBALL_ZOOM) {
			setHeatMap(earthquakes);
		}
  });

  google.maps.event.addListener(map, 'idle', queryEvents);

  function sendBounds() {
  	var request = new XMLHttpRequest();
		request.open("get", "/" + "?bounds=" + map.getBounds());
		request.send();
  }

  function queryEvents() {
  	var bounds = map.getBounds();
  }

	function plotPoints(earthquakes) {
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);
			var eventName = eq[1];
			var icon = {
				url: '/static/beachballs/' + eventName + '.png',
				scaledSize: new google.maps.Size(30, 30) 
			};

	    var marker = new google.maps.Marker({
	      position: latLng,
	      map: map,
	      icon: icon
	    });
		})
	}

	function setHeatMap(earthquakes) {
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