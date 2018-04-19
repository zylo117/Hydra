#! /usr/bin/env python32

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import ctypes
import time

# Note: DWORD = ctypes.c_ulong
# BYTE = unsigned char (ctypes.c_ubyte)

t_wait = 0.1

class HyVision(object):

    def __init__(self, m_board_index=0, control_dll='../dlls/USB30(270A)DLL_MV121.dll', comm_dll='../dlls/usb-frm11.dll'):

        self.m_board_index = m_board_index

        #############
        # Load DLLs #
        #############
        
        # for some reason, order DLLs are being loaded is critical !
        self.HVS_comm_dll = ctypes.CDLL(comm_dll)
        self.HVS_control_dll = ctypes.WinDLL(control_dll)
        # alternative DLL loading (not fully tested):
        #self.HVS_comm_dll = ctypes.WinDLL("Z:\\HYVISION\\PyVision\\usb-frm11.dll")
        # other possible dll load functions (not sure what the differences are):
        #self.HVS_control_dll = ctypes.cdll.LoadLibrary("Z:\\HYVISION\\PyVision\\USB30(270A)DLL_MV121.dll")
        #self.HVS_comm_dll = ctypes.cdll.LoadLibrary("Z:\\HYVISION\\PyVision\\usb-frm11.dll")
        #self.HVS_control_dll = ctypes.CDLL('Z:\\HYVISION\\PyVision\\USB30(270A)DLL_MV121.dll')

        self.open_USB_comm()


    def open_USB_comm(self):

        #####################################################
        # Open & Initialize USB communication with HyVision #
        #####################################################

        self.Nboards = self.HVS_comm_dll.OpenDAQDevice()
        if self.Nboards>0: 
            print("Successful connection to %i HyVision board(s)"%self.Nboards)
        else:
            print("ERROR: Failed to connect to any HyVision board: Nboards = %i"%self.Nboards)

        bcomm_init = self.HVS_comm_dll.LVDS_Init_Mul(self.m_board_index)
        #bcomm_init = self.HVS_comm_dll.LVDS_Init_Mul # works in WinDLL
        #bcomm_init = self.HVS_comm_dll.LVDS_Start_Mul(self.m_board_index)
        if bcomm_init:
            print("USB communication initialized")
        else:
            print("Failed to initialize USB communication")


    def close_USB_comm(self):

        bClose = self.HVS_comm_dll.CloseDAQDevice()
        if bClose: 
            print("Successfully closed USB connections")
        else:
            print("ERROR: Failed to close USB connections")


    def set_HVS_PS(self):

        ######################
        # Set power supplies #
        ######################

        HVS_PPIN_1  = 0
        HVS_PPIN_2  = 1
        HVS_PPIN_3  = 2
        HVS_PPIN_4  = 3 
        HVS_PPIN_35 = 4
        HVS_PPIN_36 = 5
        HVS_PPIN_IO = 6

        HW_PowerPin1_Volt  = 0.0
        HW_PowerPin2_Volt  = 0.0
        HW_PowerPin3_Volt  = 0.0
        HW_PowerPin4_Volt  = 0.0
        HW_PowerPin35_Volt = 0.0
        HW_PowerPin36_Volt = 0.0
        HW_PowerPinIO_Volt = 2.8

        #HVS_control_dll.Program_PowerOffAllM(self.m_board_index)
        bpow1  = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_1, self.m_board_index)
        bpow2  = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_2, self.m_board_index)
        bpow3  = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_3, self.m_board_index)
        bpow4  = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_4, self.m_board_index)
        bpow35 = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_35, self.m_board_index)
        bpow36 = self.HVS_control_dll.Program_PowerOffM(HVS_PPIN_36, self.m_board_index)
        bpowIO = self.HVS_control_dll.IOlevel_SetM(ctypes.c_float(HW_PowerPinIO_Volt), self.m_board_index)

        if bpow1 and bpow2 and bpow3 and bpow4 and bpow35 and bpow36 and bpowIO:
            print("Power supplies successfully set")


    def set_GPIO_pin(self, GPIO_pin):

        print("\n################################################ Switching to GPIO bus %i..."%GPIO_pin)

        #print "GPIO pins:"
        #print self.HVS_control_dll.GPIO_Read(0,0)
        #print self.HVS_control_dll.GPIO_Read(1,0)
        #print self.HVS_control_dll.GPIO_Read(2,0)
        #print self.HVS_control_dll.GPIO_Read(3,0)

        self.HVS_control_dll.GPIOWrite_Low(0,self.m_board_index)
        self.HVS_control_dll.GPIOWrite_Low(1,self.m_board_index)
        self.HVS_control_dll.GPIOWrite_Low(2,self.m_board_index)
        self.HVS_control_dll.GPIOWrite_Low(3,self.m_board_index)

        time.sleep(t_wait)

        self.HVS_control_dll.GPIOWrite_High(GPIO_pin,self.m_board_index)

        #print "GPIO pins:"
        #print self.HVS_control_dll.GPIO_Read(0,0)
        #print self.HVS_control_dll.GPIO_Read(1,0)
        #print self.HVS_control_dll.GPIO_Read(2,0)
        #print self.HVS_control_dll.GPIO_Read(3,0)


    def convert_to_ctypes(self, slave_address, length_register_address, register_address, data_length):

        slave = ctypes.c_ubyte(slave_address<<1)
        addr_len = ctypes.c_ulong(length_register_address)
        addr = ctypes.c_ulong(register_address)
        length = ctypes.c_ulong(data_length)

        #print '\nm_board_index=',self.m_board_index,'\nslave=',hex(slave_address),'\naddr_len=',length_register_address,'\naddr=',hex(register_address),'\nlength=',data_length

        return slave, addr_len, addr, length

    def I2C_read(self, slave_address, length_register_address, register_address, data_length):

        print("Reading:",hex(slave_address),hex(register_address),'...')

        self.HVS_comm_dll.I2C_SYS_Reset_Mul(self.m_board_index)

        slave, addr_len, addr, length = self.convert_to_ctypes(slave_address, length_register_address, register_address, data_length)

        data_rd = (ctypes.c_ubyte*4)()

        #print "Data buffer before read: ",hex(data_rd[0]),':',hex(data_rd[1]),':',hex(data_rd[2]),':',hex(data_rd[3])
        #bread = self.HVS_comm_dll.I2C_SYS_Read_Mul(self.m_board_index, slave, addr_len, addr, length, ctypes.byref(data_rd))
        bread = self.HVS_comm_dll.I2C_SYS_Read_Mul(self.m_board_index, slave, addr_len, addr, length, ctypes.addressof(data_rd))
        if bread:
            print("Successful read from slave,address = %i,%i"%(slave.value,addr.value))
        else:
            print("ERROR: read failed")
        print("Data buffer after read:  ",hex(data_rd[0]),':',hex(data_rd[1]),':',hex(data_rd[2]),':',hex(data_rd[3]))

        return data_rd


    def I2C_write(self, slave_address, length_register_address, register_address, data_length, data_value):

        #print "Writing:",hex(slave_address),hex(register_address),hex(data_value),'...'

        self.HVS_comm_dll.I2C_SYS_Reset_Mul(self.m_board_index)

        slave, addr_len, addr, length = self.convert_to_ctypes(slave_address, length_register_address, register_address, data_length)

        #data_wr = ctypes.create_string_buffer(2)
        #data_wr[0],data_wr[1] = '4','5'
        data_wr = (ctypes.c_ubyte*4)()
        #data_wr[0],data_wr[1],data_wr[2],data_wr[3] = ctypes.c_ubyte(11),ctypes.c_ubyte(22),ctypes.c_ubyte(33),ctypes.c_ubyte(44)
        if length.value==1:
            #print "length = 1 byte"
            data_wr[0] = ctypes.c_ubyte(data_value & 0xFF)
        elif length.value==2:
            #print "length = 2 bytes"
            data_wr[0] = ctypes.c_ubyte((data_value>>8) & 0xFF)
            data_wr[1] = ctypes.c_ubyte(data_value & 0xFF)

        #print "Data buffer before write:  ",hex(data_wr[0]),':',hex(data_wr[1]),':',hex(data_wr[2]),':',hex(data_wr[3])
        #bwrite = self.HVS_comm_dll.I2C_SYS_Write_Mul(self.m_board_index, slave, addr_len, addr, length, ctypes.byref(data_wr))
        bwrite = self.HVS_comm_dll.I2C_SYS_Write_Mul(self.m_board_index, slave, addr_len, addr, length, ctypes.addressof(data_wr))
        #print 'write: ',bwrite!=False
        #print "Data buffer after write:  ",hex(data_wr[0]),':',hex(data_wr[1]),':',hex(data_wr[2]),':',hex(data_wr[3])


    def initialize_headboard(self):

        self.set_GPIO_pin(3)

        self.I2C_write(0x2A, 1, 0x13, 1, 0x8F)
        self.I2C_write(0x49, 1, 0x05, 2, 0x8F5C)
        self.I2C_write(0x49, 1, 0x06, 2, 0x4CCD)
        self.I2C_write(0x49, 1, 0x07, 2, 0x4CCD)
        time.sleep(t_wait)

        self.set_GPIO_pin(2)

        self.I2C_write(0x20, 1, 0x00, 2, 0x0000)
        self.I2C_write(0x20, 1, 0x02, 2, 0x0002)
        time.sleep(t_wait)

        self.set_GPIO_pin(3)

        #self.I2C_write(0x48, 1, 0x07, 2, 0x8F5C)
        #self.I2C_write(0x2A, 1, 0x12, 1, 0x8F)
        #self.I2C_write(0x49, 1, 0x00, 2, 0x8F5C)
        #self.I2C_write(0x2B, 1, 0x12, 1, 0x8F)
        #self.I2C_write(0x2B, 1, 0x13, 1, 0x8F)
        self.I2C_write(0x49, 1, 0x01, 2, 0x8F5C) # DAC9   = VDDHA_pll
        #self.I2C_write(0x49, 1, 0x02, 2, 0x8F5C)
        time.sleep(t_wait)

        self.I2C_write(0x2A, 1, 0x10, 1, 0x4D) # PWRD1  = VDIG
        #self.I2C_write(0x2A, 1, 0x11, 1, 0x4D)
        #self.I2C_write(0x2B, 1, 0x10, 1, 0x5D)
        #self.I2C_write(0x2B, 1, 0x11, 1, 0x5D)
        time.sleep(t_wait)

        #self.I2C_write(0x48, 1, 0x04, 2, 0x8F5C)
        #self.I2C_write(0x48, 1, 0x05, 2, 0x0000)
        #self.I2C_write(0x49, 1, 0x03, 2, 0x6666)
        #self.I2C_write(0x48, 1, 0x06, 2, 0x6666)
        #self.I2C_write(0x48, 1, 0x00, 2, 0x8000)
        #self.I2C_write(0x48, 1, 0x01, 2, 0x8000)
        #time.sleep(0.2)

        #self.I2C_write(0x49, 1, 0x04, 2, 0x8000)
        #time.sleep(t_wait)


    def initialize_sensor(self, clock=27000000):

        print("\nInitializing sensor...")

        freq = ctypes.c_ulong(clock)

        self.HVS_comm_dll.CLK_Set_Mul(self.m_board_index, freq)
        time.sleep(t_wait)
        self.HVS_comm_dll.CLK_Select_Mul(self.m_board_index, 1)
        time.sleep(t_wait)

        self.HVS_comm_dll.SEN_Reset_Mul(self.m_board_index, 1)
        time.sleep(0.01)
        self.HVS_comm_dll.SEN_Reset_Mul(self.m_board_index, 0)
        time.sleep(0.05)
        self.HVS_comm_dll.SEN_Reset_Mul(self.m_board_index, 1)
        time.sleep(0.01)
        #self.HVS_comm_dll.SEN_Enable_Mul(self.m_board_index, 1)



if __name__ == '__main__':

    GPIO_pin = 0

    '''
    slave_address = 0x49
    length_register_address = 1 # byte(s)
    register_address = 0x07
    data_length = 2 # byte(s)
    data_value = 0x8030
    '''
    slave_address = 0x10
    length_register_address = 2 # byte(s)
    register_address = 0x3006
    data_length = 2 # byte(s)
    data_value = 0x6789

    hyviz = HyVision()
    hyviz.set_HVS_PS()

    hyviz.initialize_headboard()
    hyviz.initialize_sensor()

    hyviz.set_GPIO_pin(GPIO_pin)
    hyviz.I2C_read(slave_address, length_register_address, register_address, data_length)
    hyviz.I2C_write(slave_address, length_register_address, register_address, data_length, data_value)
    hyviz.I2C_read(slave_address, length_register_address, register_address, data_length)

    hyviz.close_USB_comm()
