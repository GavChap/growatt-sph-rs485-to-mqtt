
import os
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from pprint import pprint
from sph import SPH

port = '/dev/ttyUSB0'
client = ModbusClient(method='rtu', port=port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
client.connect()
print('Done!')

row = client.read_holding_registers(88, unit=0)

print("Modbus Version: " + str(row.registers[0]))

if type(row) is ModbusIOException:
    raise row
modbusVersion = row.registers[0]

print("Modbus Version: " + str(modbusVersion))

while True:
    inv_row = client.read_input_registers(0, 100, unit=0)
    bat_row = client.read_input_registers(1000, 100, unit=0)
    inverter = SPH(inv_row, bat_row)

    print(inverter.inverterStats())

