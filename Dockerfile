FROM arm32v7/python:3.8-buster

RUN ln -sf /usr/share/zoneinfo/CET /etc/localtime
WORKDIR /usr/src/app

# Install Python dependecies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Adafruit_DHT==1.4.0 --install-option="--force-pi2" && \
    pip install RPi.GPIO && \
    pip install -r requirements.txt

RUN wget https://nodejs.org/dist/v10.16.1/node-v10.16.1-linux-armv7l.tar.xz && \
    tar -xJf node-v10.16.1-linux-armv7l.tar.xz && \
    cd node-v10.16.1-linux-armv7l/ && \
    cp -R * /usr/local/ && \
    npm config set unsafe-perm true

RUN npm install -g @ionic/cli

COPY . ./
RUN cd green-pi-frontend/ && npm install

CMD [ "python", "./green-pi.py" ]
