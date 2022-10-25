
import os
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from pprint import pprint
from sph import SPH

port = '/dev/ttyUSB0'
client = ModbusClient(method='rtu', port=port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
client.connect()

row = client.read_holding_registers(88, unit=0)

while True:
    inv_row = client.read_input_registers(0, 100, unit=0)
    bat_row = client.read_input_registers(1000, 100, unit=0)
    inverter = SPH(inv_row, bat_row)

    print(inverter.inverterStats())
    time.sleep(1)
