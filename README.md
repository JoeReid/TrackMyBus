TrackMyBus
==========

A smartphone viewable GPS and 3g bus tracking system

	git clone https://github.com/JoeReid/TrackMyBus.git


Overview
--------

The idea of this system is to allow users to track where their next bus is in real time.
This will be achived by having the bus carry a lightweight GPS receiver and 3g transmiter.
These will be controled using a raspbery Pi.

The Tracker will comunicate with the server relaying a lat/long every set time interval.
The server can then serve a web app to the smartphones making use of google maps api


Folder Structure
----------------
In the root directory there are two sub folders, these are Server and Tracker.
Server currently holds a blank pyramid scafold for the web server
Tracker currently contains nothing


Setup
-----

To setup the server from the repo's root directory run the comands
	
	cd Server
	make setup


