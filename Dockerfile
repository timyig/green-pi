FROM arm32v7/python:3.8-buster

WORKDIR /usr/src/app

# Install Python dependecies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Clone Relay Box Repository
RUN git clone https://github.com/t-xigit/pyt-8-Way-Relay-Board.git && \
    cd pyt-8-Way-Relay-Board && \
    pip install -r requirements.txt

COPY . .
CMD [ "python", "./green-pi.py" ]
