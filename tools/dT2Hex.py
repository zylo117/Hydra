import numpy

frame_rate = 1.0
frame_length_lines = '0x0BFA' # 0x0340 (16 bits)
frame_length_lines = int(frame_length_lines,16)
print("frame lines = %i"%frame_length_lines)

dt_min = 0.
dt_max = 0.900

#dT = numpy.linspace(dt_min,dt_max,10)
dT = numpy.linspace(dt_min,dt_max,18)

CIT_dec = []
CIT_hex = []

for dt in dT:
    val_dec = dt * frame_rate * frame_length_lines
    val_hex = hex(val_dec)
    CIT_dec.append(val_dec)
    CIT_hex.append(val_hex)

for i in range(len(CIT_dec)):
    print("%.3f %s"%(dT[i],CIT_hex[i]))

for i in range(len(dT)):
    print("%.3f,"%(dT[i]), end=' ')
print()

for i in range(len(CIT_dec)):
    print("%.3f"%(CIT_dec[i]), end=' ')
print()

for i in range(len(CIT_hex)):
    print("%s,"%(CIT_hex[i][2:-1]), end=' ')
print()
