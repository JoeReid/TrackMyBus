function tmb_init(div_name) {
	// initialize the map on the "map" div with a given center and zoom
	if($("#"+div_name).length == 0) return;

	var map = new L.Map(div_name, {
		center: new L.LatLng(51.5, -0.1),
		zoom: 10
	});

	// create a CloudMade tile layer
	//var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/YOUR-API-KEY/997/256/{z}/{x}/{y}.png',
	var cloudmade = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18});

	map.addLayer(cloudmade);

	setTimeout(function() {
		loadReviews(map.getBounds());
		map.locate({setView: true});
	}, 1000);

	map.on('load', function(e) {            loadReviews(map.getBounds()); });
	map.on('dragend', function(e) {         loadReviews(map.getBounds()); });
	map.on('zoomend', function(e) {         loadReviews(map.getBounds()); });
	map.on('locationfound', function(e) {   loadReviews(map.getBounds()); });

	var FaceIcon = L.Icon.extend({
		iconUrl: "/static/img/happy.png",
		//shadowUrl: '../docs/images/leaf-shadow.png',
		shadowUrl: null,
		iconSize: new L.Point(32, 32),
		//shadowSize: new L.Point(68, 95),
		iconAnchor: new L.Point(16, 16),
		popupAnchor: new L.Point(0, -16)
	});
	var happyIcon = new FaceIcon("/static/img/happy.png");
	var sadIcon = new FaceIcon("/static/img/sad.png");

	var oldMarkers = [];
	var newMarkers = [];
	var markers = new L.LayerGroup();
	map.addLayer(markers);

	var lastBBox;
	var stop_layer = L.geoJson([], {
		style: function (feature) {
	        return {color: "red"};
		},
		onEachFeature: function (feature, layer) {
			layer.bindPopup(feature.properties.name);
		}
	}).addTo(map);
	var bus_layer = L.geoJson([], {
		style: function (feature) {
	        return {color: "red"};
		},
		onEachFeature: function (feature, layer) {
			layer.bindPopup("Route " + feature.properties.route_id);
		}
	}).addTo(map);
	var timer = null;

	function loadReviews(bbox) {
		if(bbox.toBBoxString() == lastBBox) return;
		lastBBox = bbox.toBBoxString();


		console.log("Loading stops for "+bbox.toBBoxString());
		jQuery.getJSON("/near_stops.json", {"bbox": bbox.toBBoxString()}, function(e) {
			console.log("Adding geojson stops");
			stop_layer.addData(e.data);
		});

		console.log("Loading busses for "+bbox.toBBoxString());
		jQuery.getJSON("/near_bus.json", {"bbox": bbox.toBBoxString()}, function(e) {
			console.log("Adding geojson busses");
			bus_layer.addData(e.data);
		});
	}

	function refreshMap() {
		lastBBox = null;
		loadReviews(map.getBounds());
	}

	function feq(a, b) {
		if(a == null || b == null) return false;
		return Math.abs(a-b) < 0.001;
	}

	function setView(lat, lon) {
		map.setView(new L.LatLng(lat, lon), 16);
		refreshMap();
	}

	window.setView = setView;
	window.refreshMap = refreshMap;
}

$(function() {
	/* main map init */
	tmb_init('map');
});
