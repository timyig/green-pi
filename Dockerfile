FROM arm32v7/python:3.8-buster

WORKDIR /usr/src/app

# Install Python dependecies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Adafruit_DHT==1.4.0 --install-option="--force-pi2" && \
    pip install RPi.GPIO

# Clone Relay Box Repository
RUN git clone --branch master --single-branch --depth 1 https://github.com/t-xigit/pyt-8-Way-Relay-Board.git && \
    cd pyt-8-Way-Relay-Board && \
    pip install -r requirements.txt

RUN wget https://nodejs.org/dist/v10.16.1/node-v10.16.1-linux-armv7l.tar.xz && \
    tar -xJf node-v10.16.1-linux-armv7l.tar.xz && \
    cd node-v10.16.1-linux-armv7l/ && \
    cp -R * /usr/local/ && \
    npm config set unsafe-perm true

RUN npm install -g @ionic/cli
RUN cp green-pi-frontend/env.pi green-pi-frontend/.env
CMD [ "python", "./green-pi.py" ]
