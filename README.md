# Growatt SPH-XXXX series to MQTT and Grafana

Requirements: 

- Machine running Linux and Python3 connected to the internet. Raspberry Pi 2 or above would suffice, though an old laptop/desktop running Ubuntu or similar would do.

- USB to RS485 device to connect to the inverter. Please check the inverter's manual for wiring the RJ45 cable to the USB-RS458 correctly, or purchase the correct cable.

To use:

Change config.toml to the right USB adapter for your inverter. Usually /dev/ttyUSB0. Optionally change the mapper to the JSON file for your inverter. 

`docker-compose up -d`

Then go to `<ip of raspberry pi>:3000` in a browser, and import the dashboard from grafana/dashboard.json

Home assistant discovery is supported with the MQTT integration.
  
Currently only Growatt SPH-XXXX inverters are supported, or inverters that support Growatt ModBus Version 2. You can add more modbus mappings in the `python/mapping` folder.

Tested with a recent Growatt SPH-3600 inverter and battery pack.
