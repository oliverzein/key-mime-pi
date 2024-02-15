import struct, js_to_hid

release_key = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00'

def int_to_byte(n: int) -> bytes:
    return struct.pack('<B', n & 0xff)
  
def hidBuffersFromString(string):
    hidBuffer = []
    
    for char in string:
        ascval = ord(char)
        print('Char: %s = %d', char, ascval)
        control_keys, hid_keycode = js_to_hid.convert2(ascval)
        print(hid_keycode)
        byteArray = [2, 0, 0, hid_keycode, 0, 0, 0, 0, 0]
        bytes = b''.join([*map(int_to_byte, byteArray)])
        hidBuffer.append(bytes)
        
    return hidBuffer

def sendHIDBuffer(hidBuffer):
    with open('/dev/hidg0', 'rb+') as fd:
        for bytes in hidBuffer:
            fd.write(bytes)
            fd.flush()
        
def sendChar(char):
    ascval = ord(char)
    print('Char: %s = %d', char, ascval)
    control_keys, hid_keycode = js_to_hid.convert2(ascval)
    print(hid_keycode)

    bytebuffer = [2, 0, 0, hid_keycode, 0, 0, 0, 0, 0]
    bytes = b''.join([*map(int_to_byte, bytebuffer)])
    with open('/dev/hidg0', 'rb+') as fd:
            fd.write(bytes)
            fd.flush()
            fd.write(release_key)

hidBuffer = hidBuffersFromString("Hallo")
sendHIDBuffer(hidBuffer=hidBuffer)