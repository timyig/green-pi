FROM arm32v7/python:3.8-buster

RUN ln -sf /usr/share/zoneinfo/CET /etc/localtime
WORKDIR /usr/src/app

# Install Python dependecies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://nodejs.org/dist/v10.16.1/node-v10.16.1-linux-armv7l.tar.xz && \
    tar -xJf node-v10.16.1-linux-armv7l.tar.xz && \
    cd node-v10.16.1-linux-armv7l/ && \
    cp -R * /usr/local/ && \
    npm config set unsafe-perm true

COPY . ./
RUN cd green-pi-frontend/ && npm install && cp .env.pi .env
RUN ionic build

RUN chmod +x run_api.sh
