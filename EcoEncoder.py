dictionary = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '.': 10,
    '&': 11,
    ':': 12,
    ',': 13,
}

inverseDictionary = {v: k for k, v in dictionary.items()}

def encode(m):
    return ''.join([format(dictionary[c], '04b') for c in m])

def byteRepresentation(m):
    return ''.join('{:08b}'.format(ord(c)) for c in m)

def decode(m):
    if (len(m)%4 != 0):
        print('error, message bytes wrong')
    s = ''
    for i in range(int(len(m)/4)):
        j = i*4
        s += inverseDictionary[int(m[j:j+4], 2)]
    return s
