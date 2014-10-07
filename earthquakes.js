var map, data;

function initialize() {
	var mapOptions = {
		zoom: 2,
		center: new google.maps.LatLng(0, 0),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);

	readFile('1976.txt');

	function readFile(filename) {
		var request = new XMLHttpRequest();
		request.open("get", filename, true);
		request.onreadystatechange = function() {
			data = request.responseText;
      parseData(data);
    }
		request.send();
	}

	function parseData(results) {
		var lines = results.split("\n");

		var i = 1
		var earthquakes = [];
		var currentEq = [];
		
		lines.forEach(function(line) {
			currentEq.push(line);
			if(i % 5 == 0) {
				earthquakes.push(currentEq);
				currentEq = [];
			}
			i++;
		})

		plotPoints(earthquakes);
	}

	function plotPoints(earthquakes) {
		earthquakes.forEach(function(eq) {
			var latitude = parseFloat(eq[0].substring(27, 32));
			var longitude = parseFloat(eq[0].substring(34, 40));
			var latLng = new google.maps.LatLng(latitude, longitude);
	    var marker = new google.maps.Marker({
	      position: latLng,
	      map: map
	    });
		})
	}

	window.eqfeed_callback = function(results) {
	  for (var i = 0; i < results.features.length; i++) {
	    var earthquake = results.features[i];
	    var coords = earthquake.geometry.coordinates;
	    var latLng = new google.maps.LatLng(coords[1],coords[0]);
	    var marker = new google.maps.Marker({
	      position: latLng,
	      map: map,
	      icon: getCircle(earthquake.properties.mag)
	    });
	  }
	}

	function getCircle(magnitude) {
  		var circle = {
    		path: google.maps.SymbolPath.CIRCLE,
    		scale: magnitude
  		};
  		return circle;
	}
}

google.maps.event.addDomListener(window, 'load', initialize);