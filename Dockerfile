FROM resin/raspberry-pi-python:latest
# Enable systemd
ENV INITSYSTEM on
# howto RESIN_SUPERVISOR_RESTART_POLICY on


# Install Python packages
RUN pip install --upgrade pip
RUN pip install pyserial pychromecast python-twitter
RUN pip install --upgrade git+https://github.com/plamere/spotipy/
RUN pip install python-telegram-bot --upgrade

# copy current directory into /app
COPY . /app
WORKDIR /app

# run python script when container lands on device
CMD ["python", "/app/metro_main.py"]
