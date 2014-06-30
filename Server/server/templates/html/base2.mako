<html>
	<head>
		<title>TrackMyBus</title>

		<!-- Le styles -->
		<link href="/static/ext/css/bootstrap.min.css" rel="stylesheet">
		<link href="/static/ext/css/bootstrap-theme.min.css" rel="stylesheet">
		<link href="/static/ext/css/bootstrap-responsive.min.css" rel="stylesheet">

		<link rel="stylesheet" href="http://code.leafletjs.com/leaflet-0.3.1/leaflet.css" />
		<!--[if lte IE 8]>
		<link rel="stylesheet" href="http://code.leafletjs.com/leaflet-0.3.1/leaflet.ie.css" />
		<![endif]-->

		<!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
		<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
	</head>
	<body>
		<h1><%def name="title()">TrackMyBus</%def>${title()}</h1>
		${next.body()}

		<script src="/static/ext/js/jquery.min.js"></script>
		<script src="/static/ext/js/bootstrap.min.js"></script>

		<script src="http://code.leafletjs.com/leaflet-0.3.1/leaflet.js"></script>
		<script src="https://maps.googleapis.com/maps/api/js?sensor=false&libraries=places" type="text/javascript"></script>
		<script src="/static/js/rhrn.js"></script>
	</body>
</html>
