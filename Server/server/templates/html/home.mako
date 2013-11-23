<%inherit file="_base.mako"/>

<%
links = [
	'/position_get?bus_id=1',
	'/position_get.json?bus_id=1',
	'/position_update.json?bus_id=1&lon=0.76&lat=52.0&route_id=1',
	'/near_stops?lon=1.4&lat=51.2',
	'/near_stops.json?lon=1.4&lat=51.2&threshold=0.01',
	'/near_bus?lon=0.761&lat=52.001&threshold=0.01'
]
%>

% for link in links:
<p><a href="${link}">${link}</a></p>
% endfor
