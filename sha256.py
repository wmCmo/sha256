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
    # return [hex(int(bin, 2)) for bin in bin_fracs]
    return bin_fracs


def loop(x, round):
    for _ in range(round):
        x = x[-1] + x[:len(x)-1]
    return x


def shift(x, zeroes: int):
    result = bin(int(x, 2) >> zeroes)[2:]
    return (32-len(result))*'0' + result


def add_mod(m1, m2, m3):
    added = []
    for i in range(len(m1)-1):
        added.append(
            str((int(m1[i]) + int(m2[i]) + int(m3[i])) % 2))
    return ''.join(added)


def sigma_0(M):
    loop7 = loop(M, 7)
    loop18 = loop(M, 18)
    shift3 = shift(M, 3)

    return add_mod(loop7, loop18, shift3)


def sigma_1(M):
    loop17 = loop(M, 17)
    loop19 = loop(M, 19)
    shift10 = shift(M, 10)
    return add_mod(loop17, loop19, shift10)


def schedule_W(scheduled, t):
    result = bin((int(sigma_1(scheduled[t-2]), 2) + int(scheduled[t-7], 2) + int(
        sigma_0(scheduled[t-15]), 2) + int(scheduled[t-16], 2)) % (2**32))[2:]
    return (32-len(result)) * '0' + result


def compute(inpt):
    parsed = parsing(inpt)
    scheduled = []
    for i, block in enumerate(parsed):
        scheduled.append([])
        for t in range(64):
            if t < 16:
                scheduled[i].append(block[t])
            else:
                scheduled[i].append(schedule_W(scheduled[i], t))
    return scheduled
