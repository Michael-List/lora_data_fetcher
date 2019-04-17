
# Setup
* Clone this repo
* Copy .env-example to .env
* Modify .env so that id fits your needs
* Create grafana, influxdb and chronograf folders in volumes folder
* chmod 777 -R grafana/
* docker-compose -f docker-compose_armv7l.yml up -d 