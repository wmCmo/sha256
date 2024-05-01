import modules.prime as p


def bin_string(inpt: str) -> str:
    outpt = ''
    for i in inpt:
        outpt += bin(ord(i))[2:]
    return outpt


def preprocess(inpt: str) -> str:
    bin_str = bin_string(inpt)
    bin_length = len(bin_str)

    zeroes = 512 - ((bin_length+64+1) % 512)
    l_zeroes = 64 - len(bin(bin_length)[2:])

    return bin_str + '1' + ('0'*zeroes) + ('0' * l_zeroes) + str(bin(bin_length)[2:])


def parsing(inpt: str) -> list[list[str]]:
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


def set_hash(hashes_no=8, root=2) -> list[str]:
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


def loop(x: str, round: int) -> str:
    for _ in range(round):
        x = x[-1] + x[:len(x)-1]
    return x


def wrap_result(x: str, y: str) -> str:
    return extend(bin((int(x, 2) + int(y, 2)) % (2**32))[2:])


def extend(result: str) -> str:
    return (32-len(result)) * '0' + result


def shift(x: str, zeroes: int) -> str:
    result = bin(int(x, 2) >> zeroes)[2:]
    return (32-len(result))*'0' + result


def add_mod(m1: str, m2: str, m3: str) -> str:
    added = []
    for i in range(len(m1)):
        added.append(
            str((int(m1[i]) + int(m2[i]) + int(m3[i])) % 2))
    return ''.join(added)


def sigma_0(M: str):
    loop7 = loop(M, 7)
    loop18 = loop(M, 18)
    shift3 = shift(M, 3)

    return add_mod(loop7, loop18, shift3)


def sigma_1(M: str):
    loop17 = loop(M, 17)
    loop19 = loop(M, 19)
    shift10 = shift(M, 10)
    return add_mod(loop17, loop19, shift10)


def schedule_W(scheduled: list[str], t: int):
    result = bin((int(sigma_1(scheduled[t-2]), 2) + int(scheduled[t-7], 2) + int(
        sigma_0(scheduled[t-15]), 2) + int(scheduled[t-16], 2)) % (2**32))[2:]
    return extend(result)


def schedule(inpt: str) -> list[list[str]]:
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


def Sigma0(x: str):
    loop2 = loop(x, 2)
    loop13 = loop(x, 13)
    loop22 = loop(x, 22)

    return add_mod(loop2, loop13, loop22)


def Sigma1(x: str):
    loop6 = loop(x, 6)
    loop11 = loop(x, 11)
    loop25 = loop(x, 25)

    return add_mod(loop6, loop11, loop25)


def Ch(e: str, f: str, g: str) -> str:
    result = ''
    for i, selector in enumerate(e):
        if selector == 1:
            result += f[i]
        else:
            result += g[i]
    return result


def Maj(a: str, b: str, c: str):
    groups = ['1' if sum([int(a[i]), int(b[i]), int(c[i])])
              > 1 else '0' for i in range(len(a))]
    return ''.join(groups)


def t1(e: str, f: str, g: str, h: str, K: str, w: str):
    Sigma_0 = Sigma0(e)
    choose = Ch(e, f, g)

    result = bin(sum([int(x, 2)
                 for x in [h, Sigma_0, choose, K, w]]) % (2*32))[2:]
    return extend(result)


def t2(a: str, b: str, c: str):
    Sigma_0 = Sigma0(a)
    Majority = Maj(a, b, c)
    result = bin((int(Sigma_0, 2) + int(Majority, 2)) % (2**32))[2:]
    return extend(result)


def compute(inpt:str) -> list[str]:
    scheduled = schedule(inpt)
    h0, h1, h2, h3, h4, h5, h6, h7 = set_hash()
    K = set_hash(64, 3)
    for block in scheduled:
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for i, t in enumerate(block):
            t_1 = t1(e, f, g, h, K[i], t)
            t_2 = t2(a, b, c)

            h = g
            g = f
            f = e
            e = extend(bin((int(d, 2) + int(t_1, 2)) % (2**32))[2:])
            d = c
            c = b
            b = a
            a = extend(bin((int(t_1, 2) + int(t_2, 2)) % (2**32))[2:])
        # update
    return [a, b, c, d, e, f, g, h]


# print(compute('A'))
print(compute('RedBlockBlue'))
