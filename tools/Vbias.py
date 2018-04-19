# TC2
# Vfilm register for specific Vbias

import numpy

def bias_code(v):
    code = int(((v - 7.2330) / (-39.22e-3)) + 0.5)
    return min(255, max(0, code))

Vbias = numpy.arange(1.5,3.1,0.1)

for v in Vbias:
    val_dec = bias_code(v)
    val_hex = hex(val_dec)

    print("Vbias = %.2f V"%v)
    print("Decimal value:",val_dec)
    print("Hexadecimal value:",val_hex)
