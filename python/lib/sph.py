import lib.registers 

class SPH:
    def __init__(self, inverter_registers, battery_registers):
        self.battery_registers = battery_registers.registers
        self.inverter_registers = inverter_registers.registers

    def inverterStats(self):
        return {
            "gridFreq": registers.get_single(self.inverter_registers, 37, 0.01),
            "gridVolt": registers.get_single(self.inverter_registers, 38, 0.1),
            "gridPower": registers.get_double(self.inverter_registers, 40, 0.1),
            "pvPower": registers.get_double(self.inverter_registers, 1, 0.1),
            "pv1Power": registers.get_double(self.inverter_registers, 5, 0.1),
            "pv2Power": registers.get_double(self.inverter_registers, 9, 0.1),
            "inverterOutput": registers.get_double(self.inverter_registers, 35, 0.1)

        }
    def batteryStats(self):
        return {
            "battSOC": registers.get_single(self.battery_registers, 14, 1),
            "Pactogrid": registers.get_double(self.battery_registers, 29, 0.1),
            "Pactouser": registers.get_double(self.battery_registers, 21, 0.1),
            "Pcharge": registers.get_double(self.battery_registers, 11, 0.1),
            "Plocalload": registers.get_double(self.battery_registers, 37, 0.1),
            "Pdischarge": registers.get_double(self.battery_registers, 9, 0.1)

        }
