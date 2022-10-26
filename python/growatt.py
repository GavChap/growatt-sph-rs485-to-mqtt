
import os
import time
import json
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from pprint import pprint
from sph import SPH
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

mqtt_client = mqtt.Client("inverter")
mqtt_client.on_connect = on_connect
mqtt_client.connect("mosquitto")
mqtt_client.loop_start()

mqtt_client.publish('homeassistant/sensor/growattmqtt/config',payload='{"name": "Growatt MQTT"}')
mqtt_client.publish('homeassistant/sensor/growattmqtt/pvPower/config',payload='{"device_class" : "power","name" : "PV Power","state_topic" : "inverter/growattmqtt/pvPower","unit_of_measurement" : "W"}', retain=True)

port = '/dev/ttyUSB0'
client = ModbusClient(method='rtu', port=port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
client.connect()
influx = InfluxDBClient(host='influxdb', port=8086)
influx.create_database('inverter')
influx.switch_database('inverter')

row = client.read_holding_registers(88, unit=0)

while True:
    inv_row = client.read_input_registers(0, 100, unit=0)
    bat_row = client.read_input_registers(1000, 100, unit=0)
    inverter = SPH(inv_row, bat_row)

    inv_stats = inverter.inverterStats()
    bat_stats = inverter.batteryStats()

    influx.write_points([{
        "measurement": "inverter",
        "fields": inv_stats | bat_stats
    }], time_precision='s')
  
    stats = inv_stats | bat_stats

    for key, value in stats.items():
        mqtt_client.publish("inverter/growattmqtt/" + key, payload=value)
    time.sleep(1)
