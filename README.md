![Docker Build/Publish Image](https://github.com/t-xigit/green-pi/workflows/Docker%20Build/Publish%20Image/badge.svg)

![Check formating](https://github.com/t-xigit/green-pi/workflows/Check%20formating/badge.svg)

# green-pi
Raspberry Pi - Caretaker for plants

## Setting up a new pi

`ansible-playbook playbook.yml -i hosts`


## Running on rpi

`docker-compose -f docker-compose.yml -d run`

## Running on your PC

`docker-compose -f docker-compose.dev.yml -d run`

Please note that this is using an environment var `GPIOZERO_PIN_FACTORY: mock` to mock the functionality of the RPiGPIO lib to be able to run on a PC

This is also using a different requirements file (`requirements.dev.txt`) to be able install python dependencies successfully, since some of the depencencies are only possible to install on in the Pi.

## Running backend tests (on PC)

`docker-compose -f docker-compose.test.yml -d run`

this tests setup uses a difference database to run the tests (`GREEN_PI_TEST_DB_CONNECTION: postgresql://green-pi:green-pi@db:5432/green-pi-db-test`), once you finish running the tests and you wanna run the app, please bring the test containers down by running:

`docker-compose down`

## Testing on the Pi without DB feature

You have to set the env MY_ENV to TEST.  
`export MY_ENV=TEST`

## Accesing Grafana
[Dashboard](green-pi:3000)

### Initalizing Grafan image
[Tutorial](https://ops.tips/blog/initialize-grafana-with-preconfigured-dashboards/)


## Moister Sensor

[Datasheet](https://cdn.shopify.com/s/files/1/1509/1638/files/Bodenfeuchte_Sensor_Modul_Datenblatt.pdf?3297654870633402394)

## 4 Relay Module

[Wiki](http://wiki.sunfounder.cc/index.php?title=4_Channel_5V_Relay_Module)

### Pin assignment

* GPIO20 - Relay 3 - Heating
* GPIO16 - Relay 2 - Carbon Filter
* GPIO21 - Relay 4 - Pump
* GPIO12 - Relay 1 - Lamp
* GPIO2 - Temp sensor

#### Raspberry PI conficurat

On boot up the 4 pins for the relays are set to output and driven high.
This turns the relays off.

This is done by editing the /boot/config.txt file:  
`gpio=12,16,20,21=op,dh`