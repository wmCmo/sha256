def bin_string(inpt):
    outpt = ''
    for i in inpt:
        outpt += bin(ord(i))[2:]
    return outpt


#preprocessing
def preprocess(inpt):
    bin_str = bin_string(inpt)
    bin_length = len(bin_str)
    zeroes = bin_length%512 if bin_length > 512 else 512%bin_length

    bin_str += '1'

    l_zero = 64 - len(bin(bin_length))
    
    
    return bin_str + '1' + ('0'*zeroes) + (l_zero * '0') + str(bin(bin_length)[2:])





print(preprocess('Hello'))