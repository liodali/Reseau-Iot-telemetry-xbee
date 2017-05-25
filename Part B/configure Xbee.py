from xbee import XBee, ZigBee
import serial
ser = serial.Serial('COM21', 9600)
def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    """
    print(data)
xbee = ZigBee(ser)
#xbee.at(command='ND', parameter='\x05') # Pin 1 high
xbee.at(frame_id='A', command='MY')
reply = xbee.wait_read_frame()
print(reply)

# Getting the integer value out of reply
import struct
print(struct.unpack('>h', reply['parameter'])[0])



xbee.halt()
ser.close()
# Set remote DIO pin 2 to low (mode 4)
#xbee.remote_at(
#    dest_addr=b'\x56\x78',
#    command='D2',
#    parameter=b'\x04')

#xbee.remote_at(
#    dest_addr=b'\x56\x78',
#    command='WR')