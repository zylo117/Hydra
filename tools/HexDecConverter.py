import numpy

if __name__ == '__main__':

    bsym = False
    bqTest = False
    #stab = '\t'
    stab = ''

    #conv_type = '%i'
    #conv_type = '%.1f'
    conv_type = '%.2f'
    
    #register_bits = 16
    register_bits = 8
    #register_bits = 7
    #register_bits = 5

    #regstart = 0.
    #regstop = 5.0
    #xref = 2.8
    #regstart = 0
    #regstop = 5.
    #xref = 0.75
    #regstart = 0.
    #regstop = 255.
    #xref = 0
    #regstart = 0.45
    #regstop = 0.45+31*0.11#4.0
    regstart = 0.9938
    regstop = 2.1178
    xref = 0

    b2 = False
    regstart2 = -5.
    regstop2 = 5.
    xref2 = -1.0

    #dX = numpy.arange(0,5.1,0.1)
    #dX = numpy.arange(-2.8,2.3,0.2)
    #dX = numpy.arange(-1.0,2.1,0.1)
    #dX = numpy.arange(-1.5,1.6,0.1)
    #dX = numpy.arange(-1.5,1.6,0.1)
    #dX = numpy.arange(0.6,-1.8,-0.1)
    #dX = numpy.arange(-0.8,0.9,0.1)
    #dX = numpy.arange(0.45,4.0,0.22)
    dX = numpy.arange(1.0,2.01,0.05)
    #dX = numpy.arange(1.5,-1.6,-0.1)
    #dX = numpy.arange(-0.5,1.3,0.1)
    #dX = numpy.arange(0.5,-1.3,-0.1)
    #dX = numpy.arange(0,35,2)
    #dX = numpy.arange(94,129,2)
    #dX = numpy.arange(88,129,2)
    #dX = numpy.arange(104,155,2)
    #dx1 = int('0x64',16)
    #dx2 = int('0x94',16)
    #dX = numpy.arange(dx1,dx2,2)
    #dX = numpy.arange(0,3.1,0.2)
    #dX = numpy.arange(1.5,2.81,0.05)
    #dX = numpy.arange(0.5,1.81,0.05)
    #dX = numpy.arange(0.5,1.81,0.01)
    #dX = numpy.arange(0.6,2.41,0.05)
    #dX = numpy.arange(1.5,2.81,0.01)
    #dX = numpy.arange(1.7,2.11,0.01)
    #dX = numpy.arange(1.7,2.41,0.05)
    #dX = numpy.arange(1.8,2.301,0.02)
    #dX = numpy.arange(1.85,2.301,0.01)
    #dX = numpy.arange(2.0,2.801,0.01)
    #dX = [1.3,1.5,1.8]
    #dX = numpy.arange(0,5.0,0.2)

    Xstart = []
    Xstop = []
    Vhexstart = []
    Vhexstop = []

    Xstart2 = []
    Xstop2 = []
    Vhexstart2 = []
    Vhexstop2 = []

    print('dx xstart xstop vhexstart vhexstop')

    for dx in dX:

        if bsym:
            xstart = xref - dx/2.
            xstop = xref + dx/2.
            if b2:
                xstart2 = xref2 - dx/2.
                xstop2 = xref2 + dx/2.
        else:
            xstart = xref
            xstop = xref + dx
            if b2:
                xstart2 = xref2
                xstop2 = xref2 + dx

        #assert(xstart>=regstart and xstart<=regstop)
        #assert(xstop>=regstart and xstop<=regstop)

        Xstart.append(xstart)
        Xstop.append(xstop)
        if b2:
            Xstart2.append(xstart2)
            Xstop2.append(xstop2)

        vdecstart = int((xstart-regstart)/float(regstop-regstart) * (2**register_bits-1))
        vhexstart = hex(vdecstart).split('0x')[1]
        Vhexstart.append(vhexstart)

        vdecstop = int((xstop-regstart)/float(regstop-regstart) * (2**register_bits-1))
        vhexstop = hex(vdecstop).split('0x')[1]
        Vhexstop.append(vhexstop)

        if b2:
            vdecstart2 = int((xstart2-regstart2)/float(regstop2-regstart2) * (2**register_bits-1))
            vhexstart2 = hex(vdecstart2).split('0x')[1]
            Vhexstart2.append(vhexstart2)
            
            vdecstop2 = int((xstop2-regstart2)/float(regstop2-regstart2) * (2**register_bits-1))
            vhexstop2 = hex(vdecstop2).split('0x')[1]
            Vhexstop2.append(vhexstop2)

        print("%.2f %.2f %.2f %s %s"%(dx,xstart,xstop,vhexstart,vhexstop))

    assert(len(Vhexstart)==len(Vhexstop))

    f_output = open('output_hexdecconverter.out','w')

    print('dX:', end=' ')
    f_output.write('dX: ')
    for dx in dX:
        out = conv_type%(dx)+','
        print(out, end=' ')
        f_output.write(out)
    print()

    print('X:', end=' ')
    f_output.write('\nX: ')
    for dx in dX:
        out = conv_type%(dx)+','
        print(out, end=' ')
        f_output.write(out)
    print()

    print('Vhexstart: ', end=' ')
    f_output.write('\nVhexstart:')
    for i in range(len(Vhexstart)):
        out = "%s,"%(Vhexstart[i])
        print(out, end=' ')
        f_output.write(out)
    print()

    print('Vhexstop: ', end=' ')
    f_output.write('\nVhexstop:')
    for i in range(len(Vhexstop)):
        out = "%s,"%(Vhexstop[i])
        print(out, end=' ')
        f_output.write(out)
    print()

    f_output.close()

    if bqTest:

        f_qTest = open('script_qTest.cmd','w')

        for i in range(len(dX)):

            '''
            f_qTest.write('%s# RR pulse width = %s \n'%(stab,dX[i]))

            f_qTest.write('%siwr16i2c 10 3026 %s\n'%(stab,Vhexstart[i]))
            f_qTest.write('%siwr16i2c 10 3027 %s\n'%(stab,Vhexstop[i]))
            f_qTest.write('%siwr16i2c 10 3084 %s\n'%(stab,Vhexstart[i]))
            f_qTest.write('%siwr16i2c 10 3085 %s\n'%(stab,Vhexstop[i]))
            f_qTest.write('%s\n'%stab)

            f_qTest.write('%sconst_adv 0\n'%stab)
            f_qTest.write('%swait_ms 1500\n'%stab)
            f_qTest.write('%scap 25 0 RawImages\Dark_%i\image\n'%(stab,dX[i]))
            f_qTest.write('%swait_ms 500\n'%stab)
            f_qTest.write('%s\n'%stab)
            f_qTest.write('%sconst_adv 20\n'%stab)
            f_qTest.write('%swait_ms 1500\n'%stab)
            f_qTest.write('%scap 25 0 RawImages\Bright_%i\image\n'%(stab,dX[i]))
            f_qTest.write('%swait_ms 500\n'%stab)
            f_qTest.write('%s\n'%stab)
            f_qTest.write('%s\n'%stab)
            '''

            f_qTest.write('%s# Vrst_high = Vdd_pix = %s V\n'%(stab,Xstop[i]))
            
            f_qTest.write('%siwr8i2c 48 04 %s\n'%(stab,Vhexstop[i]))
            f_qTest.write('%siwr8i2c 49 02 %s\n'%(stab,Vhexstop[i]))
            
            f_qTest.write('%s\n'%stab)
            
            f_qTest.write('%siwr8i2c 48 00 %s\n'%(stab,Vhexstop2[i]))
            f_qTest.write('%siwr8i2c 48 01 %s\n'%(stab,Vhexstop2[i]))
            
            f_qTest.write('%s\n'%stab)
            
            #f_qTest.write('%sconst_adv 0\n'%stab)
            f_qTest.write('%swait_ms 1500\n'%stab)
            #f_qTest.write('%scap 2 0 RawImages\Dark_%.1f\image\n'%(stab,Xstop[i]))
            f_qTest.write('%scap 2 0 RawImages_noise\image_%.1f\n'%(stab,Xstop[i]))
            f_qTest.write('%swait_ms 500\n'%stab)
            #f_qTest.write('%s\n'%stab)
            #f_qTest.write('%sconst_adv 20\n'%stab)
            #f_qTest.write('%swait_ms 1500\n'%stab)
            #f_qTest.write('%scap 25 0 RawImages\Bright_%.1f\image\n'%(stab,Xstop[i]))
            #f_qTest.write('%swait_ms 500\n'%stab)
            f_qTest.write('%s\n'%stab)
            f_qTest.write('%s\n'%stab)

        f_qTest.close()
