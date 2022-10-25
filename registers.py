def get_single(registers, index, unit):
    return float(registers[index]) * unit

def get_double(registers, index, unit):
    return float((registers[index] << 16) + registers[index+1])*unit
