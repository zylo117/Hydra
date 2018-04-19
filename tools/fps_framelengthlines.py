fps_ref = 8.
#fps_ref = 12.
#fll_ref = 3070
fll_ref = int('0xbfe',16)
print("fll_ref: %i"%fll_ref)

period_ref = 1/fps_ref

row_time = period_ref / fll_ref

#FPS = range(1,13)
FPS = list(range(1,9))

FLL = []
FLL_hex = []

for fps in FPS:

    period = 1/float(fps)

    fll = int(period / row_time)
    
    FLL.append(fll)
    FLL_hex.append(hex(fll).split('0x')[1])

print("FPS:", end=' ')
for i in range(len(FPS)):
    print('%i,'%FPS[i], end=' ')
print()

print("FLL dec:", end=' ')
for i in range(len(FLL)):
    print('%i,'%FLL[i], end=' ')
print()

print("FLL hex:", end=' ')
for i in range(len(FLL_hex)):
    print('%s,'%FLL_hex[i], end=' ')
