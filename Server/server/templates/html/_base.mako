<html>
	<head>
		<title>TrackMyBus</title>

		<!-- Le styles -->
		<link href="/static/ext/css/bootstrap.min.css" rel="stylesheet">
		<link href="/static/ext/css/bootstrap-theme.min.css" rel="stylesheet">
		<!-- <link href="/static/ext/css/bootstrap-responsive.min.css" rel="stylesheet"> -->

		<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.css" />
		<!--[if lte IE 8]>
		<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.ie.css" />
		<![endif]-->

		<!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
		<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
	</head>
	<body>
<nav class="navbar navbar-default" role="navigation">
  <!-- Brand and toggle get grouped for better mobile display -->
  <div class="navbar-header">
    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
      <span class="sr-only">Toggle navigation</span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    <a class="navbar-brand" href="#"><%def name="title()">TrackMyBus</%def>${title()}</a>
  </div>

  <!-- Collect the nav links, forms, and other content for toggling -->
  <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
<%
links = [
	('/position_get.json?bus_id=1', "position_get"),
	('/position_update.json?bus_id=1&lon=0.76&lat=52.0&route_id=1', "position_update"),
	('/near_stops.json?bbox=0,51,1,52', "near_stops"),
	('/near_bus.json?bbox=0,51,1,52', "near_bus"),
]
%>

    <ul class="nav navbar-nav">
		% for link in links:
			<li><a href="${link[0]}">${link[1]}</a></li>
		% endfor
    </ul>
	<!--
    <ul class="nav navbar-nav">
      <li class="active"><a href="#">Link</a></li>
      <li><a href="#">Link</a></li>
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li><a href="#">Action</a></li>
          <li><a href="#">Another action</a></li>
          <li><a href="#">Something else here</a></li>
          <li class="divider"></li>
          <li><a href="#">Separated link</a></li>
          <li class="divider"></li>
          <li><a href="#">One more separated link</a></li>
        </ul>
      </li>
    </ul>
    <form class="navbar-form navbar-left" role="search">
      <div class="form-group">
        <input type="text" class="form-control" placeholder="Search">
      </div>
      <button type="submit" class="btn btn-default">Submit</button>
    </form>
    <ul class="nav navbar-nav navbar-right">
      <li><a href="#">Link</a></li>
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li><a href="#">Action</a></li>
          <li><a href="#">Another action</a></li>
          <li><a href="#">Something else here</a></li>
          <li class="divider"></li>
          <li><a href="#">Separated link</a></li>
        </ul>
      </li>
    </ul>
	-->
  </div><!-- /.navbar-collapse -->
</nav>

<div class="container">
	<div class="row">
		${next.body()}
	</div>
</div>

		<script src="/static/ext/js/jquery.min.js"></script>
		<script src="/static/ext/js/bootstrap.min.js"></script>

		<script src="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.js"></script>
		<!--<script src="https://maps.googleapis.com/maps/api/js?sensor=false&libraries=places" type="text/javascript"></script>-->
		<script src="/static/js/tmb.js"></script>
	</body>
</html>


