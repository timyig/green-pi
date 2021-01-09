![Docker Build/Publish Image](https://github.com/t-xigit/green-pi/workflows/Docker%20Build/Publish%20Image/badge.svg)

![Check formating](https://github.com/t-xigit/green-pi/workflows/Check%20formating/badge.svg)

# green-pi
Raspberry Pi - Caretaker for plants

## Setting up a new pi

`ansible-playbook playbook.yml -i hosts`


## Running on rpi

`docker-compose -f docker-compose.yml -d run`

## Testing on the Pi without DB feature

You have to set the env MY_ENV to TEST.  
`export MY_ENV=TEST`

## Accesing Grafana
[Dashboard](green-pi:3000)

### Initalizing Grafan image
[Tutorial](https://ops.tips/blog/initialize-grafana-with-preconfigured-dashboards/)


## Moister Sensor

[Datasheet](https://cdn.shopify.com/s/files/1/1509/1638/files/Bodenfeuchte_Sensor_Modul_Datenblatt.pdf?3297654870633402394)

