Description
===========

easy-geoip is an easy-to-install and easy-to-use IP geolocation engine. It
can be used either as server or as a stand-alone command-line tool. If you want
to get an IP geolocation server running in a matter of seconds, you are at the
right place!


License
=======

All code from this project is licensed under the GPLv3. See 'LICENSE' for more.


Installation instructions
=========================

Installing easy-geoip is super easy. You can either do the steps below directly
on the server on which easy-geoip will be hosted or locally on your machine.
The instructions below assume you are taking the first approach, but if you
wish to work locally, just copy all the files to the server at the end.

First, create and enter the directory where easy-geoip must be placed, then
clone this repository with the following command:

	git clone https://github.com/dassencio/easy-geoip.git .

The only thing left to do is generating the IP geolocation database. For that,
just run the following command:

	./generatedb

This script will automatically download, extract and segment the GeoLite2
database from MaxMind (available at http://dev.maxmind.com/geoip/geoip2/geolite2/).
Running this script again will remove the currently existing database and
generate a fresh one; I recommend you do this at least once every month (or every
few months) to make sure the geolocation data remains accurate as it changes
over time.

If you use Apache as a web server, easy-geoip should already be working.
Try opening the root page where you are hosting easy-geoip (e.g.
``http://mygeoip.org``); if everything is working, you will see the
geolocation data for you own IP address. This is the type of output you
should see:

	{
	  "subdivision1": {
	    "code": "CA",
	    "name": "California"
	  },
	  "city": "Mountain View",
	  "time_zone": "America/Los_Angeles",
	  "subdivision2": {
	    "code": "Unknown",
	    "name": "Unknown"
	  },
	  "country": {
	    "code": "US",
	    "name": "United States"
	  },
	  "ip": "8.8.8.8",
	  "continent": {
	    "code": "NA",
	    "name": "North America"
	  },
	  "metro_code": "807"
	}

To select an IP address other than yours, just specify it directly on the
URL through a query string using the format ``http://mygeoip.org/?q=<IP>``.
For example, to get the geolocation data for IP ``1.2.3.4``, open this URL:

	http://mygeoip.org/?q=1.2.3.4

By default, easy-geoip yields JSON output. If you wish to get output in
plain text format, specify it directly on the URL as in the example below:

	http://mygeoip.org/?q=1.2.3.4&format=plain


Using easy-geoip as a stand-alone command-line tool
==================================================

You don't need to use easy-geoip as a server. After you generate the database,
you can get IP geolocation data directly on your terminal. For that, just run
``ipinfo.py`` as in the example below:

	./ipinfo.py -i 8.8.8.8

You can specify the output format too. For instance, to output plain text
instead of JSON, run:

	./ipinfo.py -f plain -i 8.8.8.8


Contributors & contact information
==================================

Diego Assencio / diego@assencio.com

