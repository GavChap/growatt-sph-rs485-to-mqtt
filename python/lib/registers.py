def get_single(registers, index, unit):
    print(registers)
    print(index)
    return round(float(registers[index]) * unit, 1)

def get_double(registers, index, unit):
    return round(float((registers[index] << 16) + registers[index+1])*unit, 1)
