import modules.prime as p


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


def parsing(inpt):
    padded = preprocess(inpt)
    N = len(padded)//512

    parsed = []

    for block in range(N):
        parsed.append([])
        block_i = padded[512*block:512*(block+1)]
        for bit_word in range(int(len(block_i)/32)):
            parsed[block].append([])
            parsed[block][bit_word] = block_i[32*bit_word:32*(bit_word+1)]
    return parsed

def set_hash(hashes_no=8, root=2):
    primes = p.find_primes(hashes_no)
    sqr_root_primes_wo_int = [prime**(1/root) -
                              round((prime**(1/root))-0.5) for prime in primes]
    bin_fracs = []
    for i, prime in enumerate(sqr_root_primes_wo_int):
        bin_fracs.append('')
        multiplier = prime
        for _ in range(32):
            multiplier = float(str(multiplier)[1:])
            multiplier = multiplier * 2
            bin_fracs[i] += str(multiplier)[0]
    return [hex(int(bin, 2)) for bin in bin_fracs]
    return bin_fracs
