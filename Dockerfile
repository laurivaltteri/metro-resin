FROM resin/raspberry-pi-python:2.7.14
# Enable systemd
ENV INITSYSTEM on

# Install Python packages
RUN pip install --upgrade pip
RUN pip install pyserial
RUN pip install --upgrade pychromecast==0.7.6
RUN pip install python-twitter
RUN pip install --upgrade git+https://github.com/plamere/spotipy/
RUN pip install python-telegram-bot --upgrade
RUN pip install --upgrade pip enum34
RUN pip install --upgrade zeroconf==0.19.1
RUN pip install feedparser

# copy current directory into /app
WORKDIR /app
COPY . ./

# run python script when container lands on device
CMD ["python", "/app/metro_runner.py"]
