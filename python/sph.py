import registers 

class SPH:
    def __init__(self, inverter_registers, battery_registers):
        self.battery_registers = battery_registers.registers
        self.inverter_registers = inverter_registers.registers

    def inverterStats(self):
        return {
            "gridFreq": registers.get_single(self.inverter_registers, 37, 0.01),
            "gridVolt": registers.get_single(self.inverter_registers, 38, 0.1),
            "pvPower": registers.get_double(self.inverter_registers, 1, 0.1),
            "pv1Power": registers.get_double(self.inverter_registers, 5, 0.1),
            "pv2Power": registers.get_double(self.inverter_registers, 9, 0.1),
            "battSOC": registers.get_single(self.battery_registers, 14, 1)
        }
        
