dictionary = {
    '0': 1,
    '1': 2,
    '2': 3,
    '3': 4,
    '4': 5,
    '5': 6,
    '6': 7,
    '7': 8,
    '8': 9,
    '9': 10,
    '.': 11,
    '&': 12,
    ':': 13,
    ',': 14,
    'x': 0
}

inverseDictionary = {v: k for k, v in dictionary.items()}

def decode(m):
    array = m.split(',')

    s = ''
    for element in array:
        b = format(int(element, 10), '08b')
        n1 = int(b[0:4],2)
        n2 = int(b[4:8],2)

        s += inverseDictionary[n1]
        if (n2 != 0):
            s += inverseDictionary[n2]

    return s
