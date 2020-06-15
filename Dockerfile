FROM arm32v7/python:3.8-buster

WORKDIR /usr/src/app

# Install Python dependecies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Adafruit_DHT==1.4.0 --install-option="--force-pi2" && \
    pip install RPi.GPIO

# Clone Relay Box Repository
RUN git clone https://github.com/t-xigit/pyt-8-Way-Relay-Board.git && \
    cd pyt-8-Way-Relay-Board && \
    pip install -r requirements.txt


CMD [ "python", "./green-pi.py" ]
