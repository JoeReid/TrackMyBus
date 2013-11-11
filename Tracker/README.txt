This is were all the code for the tracker unit will go

To setup:
	run make setup
	this will pull in gpsd to deal with getting NMEA data strings ect
	gpsd dumps JSON data on localhost:2947
	you must ?WATCH={"enable":true,"json":true

To Do:
	script for listening on localhost:2947
	script for sending data to server

Possible:
	encryption/authentication between tracker/server?

