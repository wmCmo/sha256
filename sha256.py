def bin_string(inpt):
    outpt = ''
    for i in inpt:
        outpt += bin(ord(i))[2:]
    return outpt


def preprocess(inpt):
    bin_str = bin_string(inpt)
    bin_length = len(bin_str)

    zeroes = 512 - ((bin_length+64+1) % 512)
    l_zeroes = 64 - len(bin(bin_length)[2:])

    return bin_str + '1' + ('0'*zeroes) + ('0' * l_zeroes) + str(bin(bin_length)[2:])
