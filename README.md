# Lora data fetcher
Processes incoming lora data. More Features and cleanup coming soon!  
Uses the pipe from this project: https://github.com/mruijter/lora_transceiver

# Setup without lora pipe
If you would like to try this setup but don't want to use the software from https://github.com/mruijter/lora_transceiver, you can use it for testing with our own pipe.
* Execute ./test_pipe.sh
* Make below setup

# Setup
* Clone this repo
* Copy .env-example to .env
* Modify .env so that id fits your needs
* Create grafana, grafana_nginx, influxdb and chronograf folders in volumes folder
* Copy nginx.conf from nginx_conf to volume folder/grafana_nginx
    * Change yourdomain.com in nginx.conf to your domain
    * Copy ssl certificate files into volume folder/grafana_nginx -> See nginx.conf for paths
* chmod 777 -R grafana/
* docker-compose -f docker-compose_armv7l.yml up -d

# Example data
For example data please look at this repo: https://github.com/Michael-List/arduino_lora_weatherstation