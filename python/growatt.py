
import os
import time
import json
import lib.registers as registers
from configparser import ConfigParser
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from pprint import pprint
from lib.sph import SPH
from influxdb import InfluxDBClient

config = ConfigParser()
config.read("config.toml")
print(config)
mapper = config['DEFAULT']['mapper']
with open("mapping/" + mapper) as f:
    mapping = json.load(f)

print(mapping)

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

port = config['DEFAULT']['port'] 

client = ModbusClient(method='rtu', port=port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
client.connect()
influx = InfluxDBClient(host='influxdb', port=8086)
influx.create_database('inverter')
influx.switch_database('inverter')

while True:
    regs = {}
    for reg in mapping['registerGroups']:
        row = client.read_input_registers(reg['start'], reg['length'], unit=0).registers
        regMap = reg['registerMap']
        for map in regMap:
            if regMap[map]['words'] == 2:
                regs[map] = registers.get_double(row, regMap[map]['id'] - reg['start'], regMap[map]['unit'])
            else:
                regs[map] = registers.get_single(row, regMap[map]['id'] - reg['start'], regMap[map]['unit'])


    influx.write_points([{
        "measurement": "inverter",
        "fields": regs 
    }], time_precision='s')
  
    for key, value in regs.items():
        mqtt_client.publish("inverter/growattmqtt/" + key, payload=value)
    time.sleep(5)
