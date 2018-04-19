
file = "Z:\\PC6\\Sensor_scripts\\scripts_aurel\\test\\analog\\adft\\pc6_12M4p65_adft_inject_afe.cfg"

f = open(file)

reg_addr = []
reg_data = []

for l in f.readlines():

    #print l
    if l.split(' ')[0]=='sensor':
        reg_addr.append(l.split(' ')[1])
        reg_data.append(l.split(' ')[2])

print('REGISTER ADDRESSES:')
for s in reg_addr:
    print(s,',', end=' ')
print()
print('REGISTER DATA:')
for s in reg_data:
    print(s,',', end=' ')
