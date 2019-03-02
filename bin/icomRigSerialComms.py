
import serial
import logging
import config.my_config as my_config
import binascii
# import binhex
# import base64

# declare variablbes
pream_byte = bytes([0xfe])
eom_byte = bytes([0xfd])
cmd_freq = bytes([0x00])

rcvd_bytes = []

# configure logging
logging.basicConfig(format='%(levelname)s:%(message)s ', level=my_config.logLevel)

# define the serial connection
# TODO identify the right COM port with method
ser = serial.Serial(port=my_config.comport, baudrate=my_config.baud, parity=serial.PARITY_NONE, rtscts=0)
ser.reset_input_buffer # flush the buffer so we start clean
# print(ser.name)

# function to read from rig when we just listening
def read_radio_s():
    
    # breakpoint() # DEBUG Add breakpoint for debugging bytes from rig

    rbyte_in =''
    
    while rbyte_in != eom_byte:  # process bytes until ICOM end of msg byte FD
        rbyte_in = ser.read(1) # read one byte from rig
         
        # if str((binascii.hexlify(inbyte)), 'utf-8') == "fe":
        if rbyte_in == pream_byte:
            logging.debug('  Rcvd preamble byte')
            # preamble = 1  # set flag for one preamble byte received
            ser.read(1) # read one more byte, still need one more preamble byte
            
            # if str((binascii.hexlify(inbyte)), 'utf-8') == "fe":
            if rbyte_in == pream_byte:
                # preamble = 2
                logging.debug('  Rcvd Preamble code (x2)...')  # TODO remove line when method is working

                # breakpoint() # DEBUG Add breakpoint for debugging bytes from rig
                while rbyte_in != eom_byte:

                    rbyte_in = ser.read(1)
                    rcvd_bytes.append(rbyte_in)

def proc_rcvd_bytes():
    c = 0

    logging.debug('  Byte count in msg: ' + str(len(rcvd_bytes)))
    logging.debug('  Orig: ' + str(rcvd_bytes[1]) + ' Dest: ' + str(rcvd_bytes[0]) + ' Cmd: ' + str(rcvd_bytes[2]))
    logging.debug('')
    if rcvd_bytes[2] == cmd_freq:
        logging.debug('  Freq: ' + str(binascii.hexlify(rcvd_bytes[7]))+ str(binascii.hexlify(rcvd_bytes[6])) + str(binascii.hexlify(rcvd_bytes[5])) + str(binascii.hexlify(rcvd_bytes[4]))+ str(binascii.hexlify(rcvd_bytes[3])))
        logging.debug('  Freq: ' + bytesToHexStr(rcvd_bytes[7]) + 
            bytesToHexStr(rcvd_bytes[6]) + bytesToHexStr(rcvd_bytes[5]) + 
            bytesToHexStr(rcvd_bytes[4])+ bytesToHexStr(rcvd_bytes[3]))

def bytesToHexStr(tbytes):
    return str(binascii.hexlify(tbytes))


while True:

    rcvd_bytes = []
    read_radio_s()
    # breakpoint()
    logging.debug('  ' + str(rcvd_bytes))
    proc_rcvd_bytes()
   
    #val = hex(int(binascii.hexlify(ser.read(1)), base=16)+6)
    # print('CIV Bytes: ' + val)
   
    
