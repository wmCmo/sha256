def is_prime(num:int) -> bool:
    if num <= 1:
        return False
    for i in range(2, num):
        if num%i == 0:
            return False
    return True

def find_primes(no:int) -> list:
    primes = []
    runner = 1
    while len(primes) < no:
        if is_prime(runner):
            primes.append(runner)
        runner += 1
    return primes
