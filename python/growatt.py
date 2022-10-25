
import os
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from pprint import pprint
from sph import SPH
from influxdb import InfluxDBClient

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
        "fields": inv_stats
    }], time_precision='s')

    influx.write_points([{
        "measurement": "battery",
        "fields": bat_stats
    }], time_precision='s')
    
    time.sleep(1)
