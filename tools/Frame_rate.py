line_length_pck = '0x11BC' # 0x0342 (16 bits)
frame_length_lines = '0x0BFA' # 0x0340 (16 bits)

EXTCLK = 27. * 10**6
pll_multiplier = '0x0064' # 0x0306 (16 bits)
pre_pll_clk_div = '0x03' # 0x0305 (8 bits)
vt_pix_clk_div = '0x02' # 0x0301 (8 bits)

# 1 FPS
#vt_sys_clk_div = '0x40' # 0x0303 (8 bits)
#coarse_integration_time = '0x0500' # 0x0202 (16 bits)
#coarse_integration_time = '0x0100' # 0x0202 (16 bits)

# 4 FPS
vt_sys_clk_div = '0x10' # 0x0303 (8 bits)
#coarse_integration_time = '0x0100' # 0x0202 (16 bits)
#coarse_integration_time = '0x03A0' # 0x0202 (16 bits)
coarse_integration_time = '0x0400' # 0x0202 (16 bits)

# 8 FPS
#vt_sys_clk_div = '0x08' # 0x0303 (8 bits)
#coarse_integration_time = '0x0800' # 0x0202 (16 bits)

'''
# DarkPy DACQ with frame rate > 1000ms
line_length_pck = '0x1803' # 0x0342 (16 bits)
frame_length_lines = '0x0968' # 0x0340 (16 bits)

EXTCLK = 27. * 10**6
pll_multiplier = '0x0001' # 0x0306 (16 bits)
pre_pll_clk_div = '0x01' # 0x0305 (8 bits)
vt_sys_clk_div = '0x01' # 0x0303 (8 bits)
vt_pix_clk_div = '0x01' # 0x0301 (8 bits)

coarse_integration_time = '0x0BEA' # 0x0202 (16 bits)
'''

line_length_pck = float(int(line_length_pck,16))
frame_length_lines = float(int(frame_length_lines,16))

pll_multiplier = float(int(pll_multiplier,16))
pre_pll_clk_div = float(int(pre_pll_clk_div,16))
vt_sys_clk_div = float(int(vt_sys_clk_div,16))
vt_pix_clk_div = float(int(vt_pix_clk_div,16))

coarse_integration_time = int(coarse_integration_time,16)

'''
line_length_pck = 4540
frame_length_lines = 3066

EXTCLK = 130. * 10**6
pll_multiplier = 100
pre_pll_clk_div = 3
vt_sys_clk_div = 64
vt_pix_clk_div = 2
'''

print("EXTCLK = %.3f MHz"%(EXTCLK/10**6))

digital_clk_freq = EXTCLK * (pll_multiplier/pre_pll_clk_div) / (vt_sys_clk_div*vt_pix_clk_div)

print("Digital clock frequency = %.3f MHz"%(digital_clk_freq/10**6))

pixel_rate = 2* digital_clk_freq

print("Pixel rate = %.3f MHz"%(pixel_rate/10**6))

frame_size = line_length_pck * frame_length_lines

print("Frame size = %.3f Mpx"%(frame_size/10**6))

frame_rate = pixel_rate / frame_size

print("Frame Rate = %.3f FPS"%frame_rate)

integration_time = coarse_integration_time / (frame_rate*frame_length_lines)

print("Integration Time = %.3f ms"%(integration_time*1000))
