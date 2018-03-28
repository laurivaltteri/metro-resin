# Metrotaulu Python on ResinOS
This is metro display control on the Rasperry Pi using Python with ResinOS

The serial device should be mounted to "/dev/ttyUSB0"

Some guides:
https://resinos.io/docs/raspberry-pi/gettingstarted/
but get the image for RPI0W from https://dashboard.resin.io/
https://runnable.com/docker/python/dockerize-your-python-application

Image for the development machine:
https://hub.docker.com/r/resin/raspberry-pi-python/

Systemd is somehow related to relaunch of the app:
https://en.wikipedia.org/wiki/Systemd

All you need to do is :

* clone this repo locally
* connect 'serial converted to USB on RPI0W with ResinOS' in cardslot
* add the resin to development machine
* `sudo resin local push resin.local --source .`
* enjoy the timely info on the display...
