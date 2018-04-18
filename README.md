# Metrotaulu Python on ResinOS
This is metro display control on the Rasperry Pi using Python with ResinOS

The serial device should be mounted to "/dev/ttyUSB0"
Please see http://sooda.dy.fi/2013/3/29/omaa-tekstia-metronayttoihin/
and https://github.com/sooda/metro_station_display for more info on circuit design.
And for me only working adapter was: http://www.aten.com/global/en/products/usb-&-thunderbolt/usb-converters/uc232a/

Some guides:
https://resinos.io/docs/raspberry-pi/gettingstarted/

Some info:
https://runnable.com/docker/python/dockerize-your-python-application

Image for the development machine:
https://hub.docker.com/r/resin/raspberry-pi-python/

Systemd is somehow related to relaunch of the app:
https://en.wikipedia.org/wiki/Systemd
http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/
But all you need is (in Dockerfile):
ENV INITSYSTEM on

All you need to do is :

* clone this repo locally
* get .cache-«username» -file by running spotipy.util.prompt_for_user_token with computer using browser for the first time
* connect 'serial converted to USB on RPI0W with ResinOS' in cardslot
* add the resin to development machine
* `sudo resin local push «devname».local --source .`
  * debugging: `ssh root@«devname».local -p22222`
* enjoy the timely info on the display...
