import struct

def int_to_byte(n: int) -> bytes:
    return struct.pack('<B', n & 0xff)

input_array = [0, 0, -5, 5, 0]

print(b''.join([*map(int_to_byte, input_array)]))